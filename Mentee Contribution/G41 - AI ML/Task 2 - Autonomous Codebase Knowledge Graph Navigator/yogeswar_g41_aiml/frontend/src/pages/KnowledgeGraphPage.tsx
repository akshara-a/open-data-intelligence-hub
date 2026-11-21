import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { useSnapshot } from '../context/SnapshotContext';
import { useAuth } from '../context/AuthContext';

export interface GraphEntity {
  entity_id: string;
  logical_entity_id?: string;
  name: string;
  file_path: string;
  line_start?: number;
  line_end?: number;
  signature_hash?: string;
  entity_types: string[];
}

export interface GraphEdge {
  id: string;
  source_id: string;
  target_id: string;
  source_name: string;
  target_name: string;
  relationship: string;
  direction: 'OUTGOING' | 'INCOMING';
}

export interface GraphStatistics {
  snapshot_id?: string;
  repo_id?: string;
  commit_sha?: string;
  total_entities: number;
  total_relationships: number;
  total_evidence?: number;
  total_unresolved_calls?: number;
}

// Baseline demo entities for the verified benchmark repository (repo_demo_sample)
const DEMO_BENCHMARK_ENTITIES: GraphEntity[] = [
  {
    entity_id: 'demo::Function::auth_service.verify_credentials',
    name: 'verify_credentials()',
    file_path: 'auth_service.py',
    line_start: 4,
    line_end: 8,
    signature_hash: '1c6f1f68261d',
    entity_types: ['Function'],
  },
  {
    entity_id: 'demo::Class::db_pool.DatabasePool',
    name: 'DatabasePool',
    file_path: 'db_pool.py',
    line_start: 3,
    line_end: 9,
    signature_hash: '8f2a1b90c4de',
    entity_types: ['Class'],
  },
  {
    entity_id: 'demo::Function::db_pool.query',
    name: 'DatabasePool.query()',
    file_path: 'db_pool.py',
    line_start: 7,
    line_end: 9,
    signature_hash: 'eca200a2bdcb',
    entity_types: ['Function'],
  },
  {
    entity_id: 'demo::Function::dynamic_router.dispatch_dynamic_route',
    name: 'dispatch_dynamic_route()',
    file_path: 'dynamic_router.py',
    line_start: 3,
    line_end: 6,
    signature_hash: '3d90f11a82bc',
    entity_types: ['Function', 'Dynamic'],
  },
];

const DEMO_BENCHMARK_EDGES: GraphEdge[] = [
  {
    id: 'demo_edge_1',
    source_id: 'demo::Function::auth_service.verify_credentials',
    target_id: 'demo::Function::db_pool.query',
    source_name: 'verify_credentials',
    target_name: 'query',
    relationship: 'CALLS',
    direction: 'OUTGOING',
  },
  {
    id: 'demo_edge_2',
    source_id: 'demo::Class::db_pool.DatabasePool',
    target_id: 'demo::Function::db_pool.query',
    source_name: 'DatabasePool',
    target_name: 'query',
    relationship: 'DEFINES',
    direction: 'OUTGOING',
  },
];

export const KnowledgeGraphPage: React.FC = () => {
  const params = useParams<{ repoId: string; commitSha: string }>();
  const { activeRepoId, activeCommitSha } = useSnapshot();
  const { authFetch } = useAuth();

  const repoId = params.repoId || activeRepoId;
  const commitSha = params.commitSha || activeCommitSha;

  const [entities, setEntities] = useState<GraphEntity[]>([]);
  const [edges, setEdges] = useState<GraphEdge[]>([]);
  const [statistics, setStatistics] = useState<GraphStatistics | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const [hopDistance, setHopDistance] = useState<number>(2);
  const [filterType, setFilterType] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedNode, setSelectedNode] = useState<GraphEntity | null>(null);
  const [nodeNeighbors, setNodeNeighbors] = useState<{ outgoing: any[]; incoming: any[] } | null>(null);

  const isDemoRepo = repoId === 'repo_demo_sample';

  const fetchGraphData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    setSelectedNode(null);
    setNodeNeighbors(null);

    // If demo sample repo, load benchmark dataset
    if (isDemoRepo) {
      setEntities(DEMO_BENCHMARK_ENTITIES);
      setEdges(DEMO_BENCHMARK_EDGES);
      setStatistics({
        total_entities: DEMO_BENCHMARK_ENTITIES.length,
        total_relationships: DEMO_BENCHMARK_EDGES.length,
        total_unresolved_calls: 1,
      });
      setIsLoading(false);
      return;
    }

    try {
      // 1. Fetch live entities from backend
      const entResp = await authFetch(`/api/v1/repos/${encodeURIComponent(repoId)}/snapshots/${encodeURIComponent(commitSha)}/graph/entities`);
      if (!entResp.ok) {
        throw new Error(`Failed to load graph entities (HTTP ${entResp.status})`);
      }
      const entData = await entResp.json();
      const rawEntities: GraphEntity[] = entData.entities || [];
      setEntities(rawEntities);

      // 2. Fetch graph statistics
      try {
        const statsResp = await authFetch(`/api/v1/repos/${encodeURIComponent(repoId)}/snapshots/${encodeURIComponent(commitSha)}/graph/statistics`);
        if (statsResp.ok) {
          const statsData = await statsResp.json();
          setStatistics(statsData);
        }
      } catch (e) {
        console.warn('Statistics fetch non-fatal error:', e);
      }

      // 3. Fetch all verified relationships from snapshot
      try {
        const relResp = await authFetch(
          `/api/v1/repos/${encodeURIComponent(repoId)}/snapshots/${encodeURIComponent(commitSha)}/graph/relationships`
        );
        if (relResp.ok) {
          const relData = await relResp.json();
          setEdges(relData.relationships || []);
        } else {
          // Fallback to querying neighbors if relationships endpoint is unavailable
          const targetEntities = rawEntities.filter((e) =>
            e.entity_types.some((t) => ['Function', 'Class'].includes(t))
          );
          const collectedEdges: GraphEdge[] = [];
          const edgeKeySet = new Set<string>();
          await Promise.all(
            targetEntities.slice(0, 15).map(async (ent) => {
              try {
                const nResp = await authFetch(
                  `/api/v1/repos/${encodeURIComponent(repoId)}/snapshots/${encodeURIComponent(commitSha)}/graph/entities/${encodeURIComponent(ent.entity_id)}/neighbors`
                );
                if (nResp.ok) {
                  const nData = await nResp.json();
                  const outDeps = nData.outgoing_dependencies || [];
                  for (const dep of outDeps) {
                    if (dep.entity_id) {
                      const key = `${ent.entity_id}->${dep.entity_id}:${dep.relationship}`;
                      if (!edgeKeySet.has(key)) {
                        edgeKeySet.add(key);
                        collectedEdges.push({
                          id: key,
                          source_id: ent.entity_id,
                          target_id: dep.entity_id,
                          source_name: ent.name,
                          target_name: dep.name,
                          relationship: dep.relationship || 'CALLS',
                          direction: 'OUTGOING',
                        });
                      }
                    }
                  }
                }
              } catch (err) {
                // Non-fatal edge query error
              }
            })
          );
          setEdges(collectedEdges);
        }
      } catch (err) {
        console.warn('Relationships fetch non-fatal error:', err);
      }
    } catch (err: any) {
      setError(err?.message || 'Failed to communicate with knowledge graph service.');
    } finally {
      setIsLoading(false);
    }
  }, [repoId, commitSha, isDemoRepo, authFetch]);

  useEffect(() => {
    fetchGraphData();
  }, [fetchGraphData]);

  // Load detailed neighbors when a node is selected
  const handleNodeClick = async (entity: GraphEntity) => {
    setSelectedNode(entity);
    setNodeNeighbors(null);

    if (isDemoRepo) {
      setNodeNeighbors({
        outgoing: DEMO_BENCHMARK_EDGES.filter((e) => e.source_id === entity.entity_id),
        incoming: DEMO_BENCHMARK_EDGES.filter((e) => e.target_id === entity.entity_id),
      });
      return;
    }

    try {
      const resp = await authFetch(
        `/api/v1/repos/${encodeURIComponent(repoId)}/snapshots/${encodeURIComponent(commitSha)}/graph/entities/${encodeURIComponent(entity.entity_id)}/neighbors`
      );
      if (resp.ok) {
        const data = await resp.json();
        setNodeNeighbors({
          outgoing: data.outgoing_dependencies || [],
          incoming: data.incoming_dependents || [],
        });
      }
    } catch {
      // Ignored
    }
  };

  const getNodeColor = (types: string[]) => {
    if (types.includes('Function')) return { bg: '#1d4ed8', border: '#60a5fa' };
    if (types.includes('Class')) return { bg: '#6d28d9', border: '#a78bfa' };
    if (types.includes('File')) return { bg: '#047857', border: '#34d399' };
    if (types.includes('Module')) return { bg: '#b45309', border: '#fbbf24' };
    return { bg: '#334155', border: '#94a3b8' };
  };

  // Filter nodes based on edge filter and search query
  const filteredEntities = entities.filter((e) => {
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchesName = e.name.toLowerCase().includes(q);
      const matchesFile = e.file_path.toLowerCase().includes(q);
      if (!matchesName && !matchesFile) return false;
    }
    if (filterType !== 'ALL') {
      const hasMatchingEdge = edges.some(
        (edge) =>
          edge.relationship === filterType &&
          (edge.source_id === e.entity_id || edge.target_id === e.entity_id)
      );
      if (!hasMatchingEdge && !e.entity_types.includes('Function')) return false;
    }
    return true;
  });

  const visibleEdges = edges.filter((edge) => {
    if (filterType !== 'ALL' && edge.relationship !== filterType) return false;
    return true;
  });

  return (
    <div style={{ padding: '24px', maxWidth: '1240px', margin: '0 auto' }}>
      <h2>3. Interactive Knowledge Graph</h2>
      <div
        style={{
          background: '#1e293b',
          padding: '12px 16px',
          borderRadius: '6px',
          marginBottom: '16px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '12px',
        }}
      >
        <div>
          <strong>Active Snapshot:</strong> <code>{repoId}</code> @ <code>{commitSha.substring(0, 10)}...</code>
        </div>
        {statistics && (
          <div style={{ display: 'flex', gap: '16px', fontSize: '12px', color: '#94a3b8' }}>
            <span>Entities: <strong style={{ color: '#38bdf8' }}>{statistics.total_entities}</strong></span>
            <span>Relationships: <strong style={{ color: '#34d399' }}>{statistics.total_relationships}</strong></span>
            {statistics.total_unresolved_calls !== undefined && (
              <span>Dynamic Calls: <strong style={{ color: '#fbbf24' }}>{statistics.total_unresolved_calls}</strong></span>
            )}
          </div>
        )}
      </div>

      {/* Dataset Status Banner */}
      {isDemoRepo ? (
        <div
          style={{
            background: 'rgba(234, 179, 8, 0.08)',
            border: '1px solid rgba(234, 179, 8, 0.35)',
            borderRadius: '8px',
            padding: '12px 16px',
            marginBottom: '16px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '12px',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span
              style={{
                background: '#eab308',
                color: '#0f172a',
                fontWeight: 700,
                fontSize: '11px',
                padding: '2px 8px',
                borderRadius: '4px',
                textTransform: 'uppercase',
                letterSpacing: '0.05em',
              }}
            >
              Demo Benchmark Dataset
            </span>
            <span style={{ fontSize: '13px', color: '#fef08a' }}>
              Interactive graph topology visualizing synthetic benchmark call-graph nodes and evidence references.
            </span>
          </div>
          <span style={{ fontSize: '12px', color: '#ca8a04', fontFamily: 'monospace' }}>
            Target Snapshot: {repoId}@{commitSha.substring(0, 10)}
          </span>
        </div>
      ) : (
        <div
          style={{
            background: 'rgba(59, 130, 246, 0.08)',
            border: '1px solid rgba(59, 130, 246, 0.35)',
            borderRadius: '8px',
            padding: '10px 16px',
            marginBottom: '16px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            fontSize: '13px',
            color: '#93c5fd',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ background: '#2563eb', color: '#fff', fontSize: '11px', fontWeight: 700, padding: '2px 6px', borderRadius: '4px' }}>
              LIVE REPOSITORY GRAPH
            </span>
            <span>Real AST call graph and entity topology isolated to this repository.</span>
          </div>
          <span style={{ fontFamily: 'monospace', fontSize: '11px' }}>Scope: {repoId}</span>
        </div>
      )}

      {/* Error Banner */}
      {error && (
        <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', color: '#f87171', padding: '12px', borderRadius: '6px', marginBottom: '16px' }}>
          ⚠️ {error}
        </div>
      )}

      {/* GraphFilterToolbar Component */}
      <div
        style={{
          background: '#1e293b',
          padding: '14px 16px',
          borderRadius: '8px',
          marginBottom: '16px',
          display: 'flex',
          gap: '16px',
          alignItems: 'center',
          flexWrap: 'wrap',
          border: '1px solid #334155',
        }}
      >
        <div>
          <label style={{ marginRight: '8px', fontSize: '13px' }}><strong>Hop Distance:</strong></label>
          <select
            value={hopDistance}
            onChange={(e) => setHopDistance(Number(e.target.value))}
            style={{ background: '#0f172a', color: '#fff', padding: '6px 10px', borderRadius: '4px', border: '1px solid #334155', fontSize: '12px' }}
          >
            <option value={1}>1 Hop</option>
            <option value={2}>2 Hops</option>
            <option value={3}>3 Hops</option>
          </select>
        </div>

        <div>
          <label style={{ marginRight: '8px', fontSize: '13px' }}><strong>Edge Filter:</strong></label>
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            style={{ background: '#0f172a', color: '#fff', padding: '6px 10px', borderRadius: '4px', border: '1px solid #334155', fontSize: '12px' }}
          >
            <option value="ALL">All Relationships</option>
            <option value="CALLS">CALLS</option>
            <option value="IMPORTS">IMPORTS</option>
            <option value="DEFINES">DEFINES</option>
            <option value="CONTAINS">CONTAINS</option>
          </select>
        </div>

        <div>
          <input
            type="text"
            placeholder="Search symbol or file..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{ background: '#0f172a', color: '#fff', padding: '6px 10px', borderRadius: '4px', border: '1px solid #334155', fontSize: '12px', width: '200px' }}
          />
        </div>

        <div style={{ fontSize: '12px', color: '#94a3b8', marginLeft: 'auto' }}>
          Graph Gateway: <code>CGG Read-Only Enforcement</code>
        </div>
      </div>

      {/* CytoscapeGraphCanvas Component */}
      <div
        style={{
          position: 'relative',
          minHeight: '480px',
          background: '#020617',
          borderRadius: '8px',
          border: '1px solid #334155',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '24px',
          overflow: 'hidden',
        }}
      >
        {isLoading ? (
          <div style={{ textAlign: 'center', color: '#94a3b8' }}>
            <div style={{ width: '32px', height: '32px', border: '3px solid #334155', borderTopColor: '#38bdf8', borderRadius: '50%', margin: '0 auto 12px auto', animation: 'spin 1s linear infinite' }} />
            <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
            <div>Loading AST Knowledge Graph for {repoId.substring(0, 8)}...</div>
          </div>
        ) : filteredEntities.length === 0 ? (
          <div style={{ textAlign: 'center', color: '#94a3b8', padding: '40px 20px' }}>
            <div style={{ fontSize: '32px', marginBottom: '12px' }}>🕸️</div>
            <div style={{ fontSize: '15px', fontWeight: 600, color: '#e2e8f0', marginBottom: '8px' }}>
              No AST Entities in Snapshot
            </div>
            <p style={{ fontSize: '13px', maxWidth: '440px', margin: '0 auto', lineHeight: '1.5' }}>
              No entities or call relationships were located for this snapshot. Run an ingestion job from Repository Explorer or switch to an active snapshot.
            </p>
          </div>
        ) : (
          <div style={{ textAlign: 'center', width: '100%' }}>
            <p style={{ color: '#94a3b8', fontSize: '13px', margin: '0 0 20px 0' }}>
              AST Knowledge Graph Topology &bull; Controlled Graph Gateway (CGG) &bull; Snapshot-Isolated ({filteredEntities.length} visible entities, {visibleEdges.length} verified edges)
            </p>

            {/* Render Nodes Grid */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', justifyContent: 'center', alignItems: 'center', margin: '20px 0' }}>
              {filteredEntities.map((n) => {
                const colors = getNodeColor(n.entity_types);
                const isSelected = selectedNode?.entity_id === n.entity_id;
                return (
                  <div
                    key={n.entity_id}
                    onClick={() => handleNodeClick(n)}
                    style={{
                      background: colors.bg,
                      padding: '14px 18px',
                      borderRadius: '10px',
                      cursor: 'pointer',
                      border: `2px solid ${colors.border}`,
                      boxShadow: isSelected ? `0 0 16px ${colors.border}` : '0 4px 6px -1px rgba(0,0,0,0.3)',
                      transition: 'all 0.2s ease',
                      textAlign: 'left',
                      minWidth: '180px',
                    }}
                  >
                    <div style={{ fontWeight: 600, fontSize: '13px', color: '#fff' }}>
                      {n.name}
                      {n.entity_types.includes('Function') && '()'}
                    </div>
                    <div style={{ fontSize: '11px', color: '#e2e8f0', marginTop: '4px' }}>
                      {n.file_path}{n.line_start ? `:${n.line_start}` : ''}
                    </div>
                    <div style={{ display: 'flex', gap: '6px', marginTop: '8px', flexWrap: 'wrap' }}>
                      {n.entity_types.map((t) => (
                        <span key={t} style={{ fontSize: '9px', background: 'rgba(0,0,0,0.4)', padding: '2px 5px', borderRadius: '3px', color: '#cbd5e1' }}>
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Visible Relationships Summary Bar */}
            {visibleEdges.length > 0 && (
              <div style={{ marginTop: '20px', padding: '10px 16px', background: '#0f172a', borderRadius: '6px', display: 'inline-flex', gap: '16px', flexWrap: 'wrap', fontSize: '12px', color: '#94a3b8' }}>
                {visibleEdges.slice(0, 3).map((e) => (
                  <span key={e.id}>
                    <strong>Verified Edge:</strong> <code>{e.source_name}</code> &mdash;[{e.relationship}]&rarr; <code>{e.target_name}</code>
                  </span>
                ))}
                {visibleEdges.length > 3 && (
                  <span style={{ color: '#64748b' }}>+{visibleEdges.length - 3} more relationships</span>
                )}
              </div>
            )}
          </div>
        )}

        {/* EvidencePopover Component */}
        {selectedNode && (
          <div
            style={{
              position: 'absolute',
              top: '20px',
              right: '20px',
              background: '#1e293b',
              padding: '16px',
              borderRadius: '8px',
              border: `2px solid ${getNodeColor(selectedNode.entity_types).border}`,
              maxWidth: '340px',
              boxShadow: '0 10px 25px -5px rgba(0,0,0,0.6)',
              zIndex: 10,
              textAlign: 'left',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <h4 style={{ margin: 0, fontSize: '14px', color: '#fff' }}>Evidence Popover (EvidencePopover)</h4>
              <button
                onClick={() => setSelectedNode(null)}
                style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer', fontSize: '16px', padding: '0 4px' }}
                title="Dismiss"
              >
                ✕
              </button>
            </div>

            <div style={{ fontSize: '13px', marginBottom: '6px', color: '#e2e8f0' }}>
              <strong>Symbol:</strong> <code>{selectedNode.name}</code>
            </div>
            <div style={{ fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>
              <strong>Types:</strong> {selectedNode.entity_types.join(', ')}
            </div>
            <div style={{ fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>
              <strong>File & Lines:</strong> <code>{selectedNode.file_path}{selectedNode.line_start ? `:${selectedNode.line_start}–${selectedNode.line_end}` : ''}</code>
            </div>
            {selectedNode.signature_hash && (
              <div style={{ fontSize: '11px', color: '#64748b', marginBottom: '6px' }}>
                Signature: <code>{selectedNode.signature_hash}</code>
              </div>
            )}

            {/* Direct Neighbors if loaded */}
            {nodeNeighbors && (
              <div style={{ marginTop: '10px', paddingTop: '10px', borderTop: '1px solid #334155', fontSize: '11px' }}>
                <div style={{ fontWeight: 600, color: '#38bdf8', marginBottom: '4px' }}>
                  Dependencies ({nodeNeighbors.outgoing.length}):
                </div>
                {nodeNeighbors.outgoing.length > 0 ? (
                  <ul style={{ margin: '0 0 6px 0', paddingLeft: '16px', color: '#cbd5e1' }}>
                    {nodeNeighbors.outgoing.map((dep, idx) => (
                      <li key={idx}>
                        [{dep.relationship}] &rarr; <code>{dep.name || dep.target_name}</code>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <div style={{ color: '#64748b' }}>None</div>
                )}

                <div style={{ fontWeight: 600, color: '#34d399', marginBottom: '4px', marginTop: '6px' }}>
                  Dependents ({nodeNeighbors.incoming.length}):
                </div>
                {nodeNeighbors.incoming.length > 0 ? (
                  <ul style={{ margin: 0, paddingLeft: '16px', color: '#cbd5e1' }}>
                    {nodeNeighbors.incoming.map((dep, idx) => (
                      <li key={idx}>
                        &larr; [{dep.relationship}] <code>{dep.name || dep.source_name}</code>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <div style={{ color: '#64748b' }}>None</div>
                )}
              </div>
            )}

            <div style={{ marginTop: '12px', textAlign: 'right' }}>
              <button
                onClick={() => setSelectedNode(null)}
                style={{ background: '#334155', color: '#fff', border: 'none', padding: '5px 12px', borderRadius: '4px', cursor: 'pointer', fontSize: '11px' }}
              >
                Dismiss
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
