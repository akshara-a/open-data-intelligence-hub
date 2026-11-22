"""Architectural reasoning engine analyzing coupling metrics, blast radius, debt, and refactoring."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from src.graph.base import BaseGraphClient
from src.mcp.tools import GraphToolRegistry


class RefactoringPhase(BaseModel):
    """Single step in an engineering refactoring strategy."""

    phase_number: int
    title: str
    target_components: List[str]
    actions: List[str]
    risk_level: str = Field("Medium", description="Low, Medium, or High")
    verification_criteria: str


class ArchitecturalDebtEvaluation(BaseModel):
    """Detailed evaluation of architectural debt in the codebase."""

    single_points_of_failure: List[Dict[str, Any]]
    circular_dependencies: List[List[str]]
    shared_datastores: List[Dict[str, Any]]
    deprecated_active_modules: List[str]
    overall_risk_score: str = Field("High", description="Low, Medium, High, or Critical")


class ArchitecturalReasoningEngine:
    """Evaluates graph relationships, coupling metrics, blast radius, and generates refactoring strategies."""

    def __init__(self, tool_registry: Optional[GraphToolRegistry] = None):
        """Initialize reasoning engine with graph tool registry."""
        self.tool_registry = tool_registry or GraphToolRegistry()
        self.graph_client = self.tool_registry.graph_client

    def evaluate_deprecation_impact(self, target_id: str) -> Dict[str, Any]:
        """Perform comprehensive blast-radius and architectural risk analysis for a deprecation.
        
        Args:
            target_id: Identifier of the component proposed for deprecation.
            
        Returns:
            Dictionary containing blast radius, affected services, API routes, debt, and refactoring steps.
        """
        # Step 1: Blast radius analysis via tool registry
        blast_res = self.tool_registry.call_tool("analyze_blast_radius", {"node_id": target_id})
        if not blast_res.get("success"):
            raise KeyError(blast_res.get("error", f"Node '{target_id}' could not be analyzed."))
        blast_data = blast_res["data"]

        # Step 2: Coupling metrics evaluation
        coupling_res = self.tool_registry.call_tool("analyze_coupling", {"node_id": target_id})
        coupling_data = coupling_res.get("data", {}) if coupling_res.get("success") else {}

        # Step 3: Cycle analysis
        cycle_res = self.tool_registry.call_tool("detect_dependency_cycles")
        cycles = cycle_res.get("data", {}).get("cycles", []) if cycle_res.get("success") else []

        # Step 4: Extract exact lists of affected components
        affected_services = blast_data.get("affected_services", [])
        affected_api_routes = blast_data.get("affected_api_routes", [])
        affected_frontends = blast_data.get("affected_frontend_components", [])
        direct_callers = blast_data.get("direct_dependents", [])
        indirect_callers = blast_data.get("indirect_dependents", [])
        traversal_paths = blast_data.get("traversal_paths", [])

        # Step 5: Architectural Debt Assessment
        debt_findings = self._evaluate_debt_for_target(
            target_id=target_id,
            coupling_data=coupling_data,
            affected_services=affected_services,
            cycles=cycles,
        )

        # Step 6: Step-by-step refactoring strategy
        refactoring_strategy = self._generate_refactoring_strategy(
            target_id=target_id,
            target_type=blast_data.get("target_type", "Component"),
            direct_callers=direct_callers,
            affected_services=affected_services,
            affected_api_routes=affected_api_routes,
            affected_frontends=affected_frontends,
            debt_findings=debt_findings,
        )

        return {
            "target_id": target_id,
            "target_name": blast_data.get("target_name", target_id),
            "target_type": blast_data.get("target_type", "Component"),
            "total_affected_count": blast_data.get("total_affected_count", 0),
            "starting_node_included": False,
            "affected_microservices": affected_services,
            "affected_api_routes": affected_api_routes,
            "affected_frontend_apps": affected_frontends,
            "direct_dependents": direct_callers,
            "indirect_dependents": indirect_callers,
            "traversal_paths": traversal_paths,
            "coupling_metrics": coupling_data,
            "debt_assessment": debt_findings,
            "refactoring_strategy": [phase.model_dump() for phase in refactoring_strategy],
        }

    def _evaluate_debt_for_target(
        self,
        target_id: str,
        coupling_data: Dict[str, Any],
        affected_services: List[str],
        cycles: List[List[str]],
    ) -> Dict[str, Any]:
        """Assess specific architectural debt items associated with the target."""
        ca = coupling_data.get("afferent_coupling", 0)
        is_spof = coupling_data.get("is_single_point_of_failure", False)

        # Check if target is involved in cycles
        involved_cycles = [c for c in cycles if target_id in c]

        # Check shared datastores across affected services
        all_edges = self.graph_client.get_relationships()
        db_access_map: Dict[str, List[str]] = {}
        for edge in all_edges:
            if edge.get("type") == "CONNECTS_TO":
                db_id = edge["target"]
                src_id = edge["source"]
                db_access_map.setdefault(db_id, []).append(src_id)

        shared_dbs = [
            {"store_id": db_id, "accessing_services": sorted(services)}
            for db_id, services in db_access_map.items()
            if len(services) > 1
        ]

        # Severity determination
        if ca >= 5 or len(affected_services) >= 4:
            severity = "CRITICAL"
        elif ca >= 3 or len(affected_services) >= 2:
            severity = "HIGH"
        else:
            severity = "MODERATE"

        return {
            "severity_level": severity,
            "afferent_coupling": ca,
            "is_single_point_of_failure": is_spof,
            "participating_cycles": involved_cycles,
            "shared_datastores_detected": shared_dbs,
            "total_downstream_services": len(affected_services),
            "debt_summary": (
                f"Component '{target_id}' exhibits high coupling (Ca={ca}). "
                f"Modifying it breaks {len(affected_services)} microservices and poses potential failure concentration risk (structural coupling candidate, subject to runtime redundancy)."
            ),
        }

    def _generate_refactoring_strategy(
        self,
        target_id: str,
        target_type: str,
        direct_callers: List[str],
        affected_services: List[str],
        affected_api_routes: List[str],
        affected_frontends: List[str],
        debt_findings: Dict[str, Any],
    ) -> List[RefactoringPhase]:
        """Generate actionable 4-phase refactoring strategy for senior backend engineers."""
        phases: List[RefactoringPhase] = []

        # Phase 1: Ingress Isolation & Anti-Corruption Layer
        phase1_targets = [c for c in direct_callers if "gateway" in c or "route" in c] or direct_callers[:2]
        phases.append(
            RefactoringPhase(
                phase_number=1,
                title="API Gateway & Ingress Isolation",
                target_components=phase1_targets,
                actions=[
                    f"Deploy an Anti-Corruption Layer (ACL) facade on the ingress to intercept calls destined for '{target_id}'.",
                    "Introduce feature toggles and canary routing rules to facilitate gradual traffic migration.",
                    "Implement fallback circuit breakers to isolate downstream microservices from deprecation outages.",
                ],
                risk_level="Medium",
                verification_criteria="Synthetic synthetic canary traffic can be routed between legacy and modern paths with 0% error spikes.",
            )
        )

        # Phase 2: Decouple Service Callers & Break Circular Dependencies
        phase2_targets = affected_services
        phases.append(
            RefactoringPhase(
                phase_number=2,
                title="Service-to-Service Decoupling & Asynchronous Event Extraction",
                target_components=phase2_targets,
                actions=[
                    "Migrate synchronous direct dependencies to asynchronous event-driven messaging (e.g. Kafka/RabbitMQ topics).",
                    "Break circular dependencies (e.g. order-service <-> inventory-service) using the Saga orchestration pattern.",
                    "Distribute decentralized token validation (e.g. JWKS public-key caching) to eliminate synchronous auth hops.",
                ],
                risk_level="High",
                verification_criteria="Microservices operate autonomously with independent deployability and zero synchronous circular RPC calls.",
            )
        )

        # Phase 3: Datastore & Storage Boundary Isolation
        shared_dbs = debt_findings.get("shared_datastores_detected", [])
        shared_store_names = [s["store_id"] for s in shared_dbs] or ["shared-customer-db", "shared-session-cache"]
        phases.append(
            RefactoringPhase(
                phase_number=3,
                title="Datastore Boundary Isolation & Anti-Pattern Remediation",
                target_components=shared_store_names,
                actions=[
                    "Eliminate shared database access anti-pattern by enforcing Database-per-Service boundaries.",
                    "Expose private entity data through well-defined internal gRPC/REST APIs rather than cross-service table joins.",
                    "Partition shared Redis session caches into isolated namespaces or dedicated service clusters.",
                ],
                risk_level="High",
                verification_criteria="Zero cross-service direct queries against foreign database schemas.",
            )
        )

        # Phase 4: Final Deprecation & Decommissioning
        phases.append(
            RefactoringPhase(
                phase_number=4,
                title=f"Decommissioning of '{target_id}'",
                target_components=[target_id] + affected_api_routes,
                actions=[
                    f"Monitor metrics to ensure zero inbound traffic to '{target_id}' across a 14-day bake period.",
                    f"Decommission legacy route endpoints ({', '.join(affected_api_routes[:3])}) and archive codebase modules.",
                    "Remove deprecated environment credentials, firewall rules, and container deployments.",
                ],
                risk_level="Low",
                verification_criteria="Target component fully stopped and undeployed with 100% successful health checks across all dependent systems.",
            )
        )

        return phases

