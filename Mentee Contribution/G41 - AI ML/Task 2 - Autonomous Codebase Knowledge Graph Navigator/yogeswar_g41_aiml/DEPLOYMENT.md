# Production Deployment & Operations Guide
## Autonomous Codebase Knowledge Graph Navigator

This document is the authoritative engineering runbook for deploying, configuring, monitoring, and operating the Autonomous Codebase Knowledge Graph Navigator in a secure, containerized production environment.

---

## 1. System Topology & Architecture

The production architecture consists of 7 isolated services partitioned across four internal Docker networks to enforce strict least-privilege service communication:

```
[ Internet / Client Browser ]
             │
             │ HTTPS (443) / TLS Termination
             ▼
┌──────────────────────────────────────────────────────────┐
│                      Nginx Proxy                         │  (ingress_net)
└────────────┬─────────────────────────────┬───────────────┘
             │ Reverse Proxy               │ Static Assets
             ▼                             ▼
┌───────────────────────────┐ ┌────────────────────────────┐
│      FastAPI Backend      │ │      React Frontend        │  (app_net)
│   (Auth, SQLite, Agents)  │ │    (TypeScript + Vite)     │
└────────────┬──────────────┘ └────────────────────────────┘
             │
             ├─────────────────────────────┐
             │ Internal Service Auth (JWT) │ Internal Service Auth (JWT)
             ▼                             ▼
┌───────────────────────────┐ ┌────────────────────────────┐
│         MCP / CGG         │ │       GraphRAG Engine      │  (mcp_net)
│   (Controlled Gateway)    │ │ (Sentence Transformers 768)│
└────────────┬──────────────┘ └────────────┬───────────────┘
             │ Parameterized Cypher        │ SQLite Embedding Cache
             ▼                             ▼
┌───────────────────────────┐ ┌────────────────────────────┐
│   Neo4j Knowledge Graph   │ │    Git Ingestion Worker    │  (db_net)
│      (Community 5.18)     │ │   (Tree-sitter AST Parser) │
└───────────────────────────┘ └────────────────────────────┘
```

### Network Isolation Boundaries

| Network | Participating Containers | Permitted Traffic |
|---|---|---|
| `ingress_net` | `nginx` | Public client TLS traffic on port 443 |
| `app_net` | `nginx`, `backend`, `frontend` | Reverse proxy routing to API and SPA static files |
| `mcp_net` | `backend`, `mcp`, `rag` | Inter-service authenticated calls via `X-Internal-Service-Auth` |
| `db_net` | `mcp`, `rag`, `ingestion`, `neo4j` | Read-only Cypher bolt connections and shared volume mounts |

---

## 2. Infrastructure Requirements

### Minimum Production Specifications
- **CPU**: 4 vCPUs (x86_64 or ARM64)
- **RAM**: 16 GB ECC RAM minimum (32 GB recommended for large repositories > 500k LOC)
- **Disk Storage**: 100 GB NVMe SSD for Git mirrors, SQLite databases, and Neo4j graph storage
- **Operating System**: Ubuntu 22.04 LTS, Debian 12, or Windows Server with Docker Engine 24.0+
- **Docker Compose**: Version 2.20 or newer

---

## 3. Cryptographic Secrets & Identity Setup

All credentials must be generated prior to startup and mounted into `/run/secrets/`. Do not commit secrets to Git.

### 3.1 Generate Asymmetric RS256 Key Pair for User JWTs
```bash
mkdir -p secrets
# Generate 4096-bit RSA Private Key
openssl genrsa -out ./secrets/jwt_rs256.key 4096

# Extract RSA Public Key
openssl rsa -in ./secrets/jwt_rs256.key -pubout -out ./secrets/jwt_rs256.pub

# Set strict file permissions (POSIX)
chmod 600 ./secrets/jwt_rs256.key
chmod 644 ./secrets/jwt_rs256.pub
```

### 3.2 Generate Database & Service Secrets
```bash
# Generate high-entropy Neo4j passwords
openssl rand -base64 32 | tr -d '\n' > ./secrets/neo4j_admin.password
openssl rand -base64 32 | tr -d '\n' > ./secrets/neo4j_read.password
openssl rand -base64 32 | tr -d '\n' > ./secrets/neo4j_write.password

# Generate internal inter-service authentication secret
openssl rand -base64 48 | tr -d '\n' > ./secrets/internal_service.secret

chmod 600 ./secrets/*.password ./secrets/*.secret
```

---

## 4. Production Deployment Steps

### Step 1: Clone Repository and Validate Environment
```bash
git clone https://github.com/org/Autonomous_Codebase_Knowledge_Graph_Navigator.git
cd Autonomous_Codebase_Knowledge_Graph_Navigator
cp .env.production.example .env
```

### Step 2: Build Production Containers
```bash
# Build frontend production bundle and Docker images
docker compose -f docker-compose.yml build
```

### Step 3: Launch Production Topology
```bash
docker compose -f docker-compose.yml up -d
```

### Step 4: Verify Service Health
```bash
# Check all 7 services report healthy
docker compose ps
```

Expected healthy output:
```
NAME                                                       STATUS
autonomous_codebase_knowledge_graph_navigator-backend-1    Up (healthy)
autonomous_codebase_knowledge_graph_navigator-frontend-1   Up
autonomous_codebase_knowledge_graph_navigator-ingestion-1  Up (healthy)
autonomous_codebase_knowledge_graph_navigator-mcp-1        Up (healthy)
autonomous_codebase_knowledge_graph_navigator-neo4j-1      Up (healthy)
autonomous_codebase_knowledge_graph_navigator-nginx-1      Up
autonomous_codebase_knowledge_graph_navigator-rag-1        Up (healthy)
```

---

## 5. Healthcheck & Verification Probes

All core microservices expose HTTP health endpoints:

```bash
# Backend API & SQLite Status
curl -fsS http://localhost/api/v1/health | jq .

# GraphRAG Model Status (Must report active_transformer)
docker exec autonomous_codebase_knowledge_graph_navigator-rag-1 python -c \
  "import httpx; print(httpx.get('http://127.0.0.1:8000/health').json())"

# MCP / CGG Service
docker exec autonomous_codebase_knowledge_graph_navigator-mcp-1 python -c \
  "import httpx; print(httpx.get('http://127.0.0.1:8000/health').json())"
```

---

## 6. Database Maintenance & Backup Procedures

### 6.1 SQLite State Store (Zero-Downtime Hot Backup)
The SQLite database operates in **WAL mode** (`PRAGMA journal_mode = WAL;`). Never copy `app_state.db` directly without the SQLite backup API.

```bash
# Execute transactional hot snapshot
docker exec autonomous_codebase_knowledge_graph_navigator-backend-1 \
  sqlite3 /app/data/app_state.db ".backup '/app/data/backup_app_state_$(date +%Y%m%d_%H%M%S).db'"
```

### 6.2 Neo4j AST Knowledge Graph Backup
```bash
docker exec autonomous_codebase_knowledge_graph_navigator-neo4j-1 \
  neo4j-admin database dump neo4j --to-path=/data/backups/
```

---

## 7. Operational Troubleshooting & Runbook

| Symptom | Diagnostic Step | Remediating Action |
|---|---|---|
| **RAG 500 Model Unavailable** | Check RAG logs: `docker logs ...-rag-1` | Container requires internet access on first boot to fetch HuggingFace model cache. Ensure network connectivity or preload offline cache in `/app/models_cache`. |
| **Missing X-Internal-Service-Auth** | Verify internal tokens: `docker logs ...-mcp-1` | Inter-service endpoints reject calls without valid RS256 token scoped to active `repo_id` and `commit_sha`. Verify `create_internal_service_token` is called. |
| **Cross-Snapshot Mismatch (404/FORBIDDEN)** | Inspect request commit SHA vs snapshot in Neo4j | Enforce strict commit isolation: queries mentioning a foreign commit SHA are rejected by design. |
| **Database Disk I/O Lock** | Check SQLite WAL file sizes in `./data` | Run `sqlite3 ./data/app_state.db "PRAGMA wal_checkpoint(TRUNCATE);"` to flush journal frames. |
