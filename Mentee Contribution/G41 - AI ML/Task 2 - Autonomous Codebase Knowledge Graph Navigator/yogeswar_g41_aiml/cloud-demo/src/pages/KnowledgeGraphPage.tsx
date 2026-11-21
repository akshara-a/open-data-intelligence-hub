import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import snapshotData from '../data/graph_snapshot.json';

export interface GraphEntity {
  entity_id: string;
  logical_entity_id: string;
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
  total_entities: number;
  total_relationships: number;
  total_unresolved_calls?: number;
  total_evidence?: number;
}

export const KnowledgeGraphPage: React.FC = () => {
  const { repoId = snapshotData.repository.repo_id, commitSha = snapshotData.snapshot.commit_sha } = useParams<{ repoId: string; commitSha: string }>();

  const [entities] = useState<GraphEntity[]>(snapshotData.entities as GraphEntity[]);
  const [edges] = useState<GraphEdge[]>(snapshotData.relationships as GraphEdge[]);
  const [statistics] = useState<GraphStatistics>(snapshotData.statistics as GraphStatistics);

  const [hopDistance, setHopDistance] = useState<number>(1);
  const [filterType, setFilterType] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedNode, setSelectedNode] = useState<GraphEntity | null>(null);

  const [nodeNeighbors, setNodeNeighbors] = useState<{
    outgoing: any[];
    incoming: any[];
  } | null>(null);

  const getNodeColor = (types: string[]) => {
    if (types.includes('Function')) return { bg: '#1d4ed8', border: '#60a5fa' };
    if (types.includes('Class')) return { bg: '#6d28d9', border: '#a78bfa' };
    if (types.includes('File')) return { bg: '#047857', border: '#34d399' };
    if (types.includes('Module')) return { bg: '#b45309', border: '#fbbf24' };
    return { bg: '#334155', border: '#94a3b8' };
  };

  const handleNodeClick = (entity: GraphEntity) => {
    setSelectedNode(entity);
    const outgoing = edges.filter((e) => e.source_id === entity.entity_id);
    const incoming = edges.filter((e) => e.target_id === entity.entity_id);
    setNodeNeighbors({ outgoing, incoming });
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

      {/* Snapshot metadata & statistics bar */}
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
            {statistics.total_evidence !== undefined && (
              <span>Evidence Records: <strong style={{ color: '#a78bfa' }}>{statistics.total_evidence}</strong></span>
            )}
          </div>
        )}
      </div>

      {/* Cloud Demo Read-Only Banner */}
      <div
        style={{
          background: 'rgba(56, 189, 248, 0.1)',
          border: '1px solid #38bdf8',
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
              background: '#0284c7',
              color: '#ffffff',
              fontWeight: 700,
              fontSize: '11px',
              padding: '3px 8px',
              borderRadius: '4px',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
            }}
          >
            READ-ONLY SNAPSHOT
          </span>
          <span style={{ fontSize: '13px', color: '#e0f2fe' }}>
            Cloud Demo &bull; 100% verified Knowledge Graph snapshot rendered entirely client-side. Zero backend server or PC required.
          </span>
        </div>
        <span style={{ fontSize: '12px', color: '#38bdf8', fontFamily: 'monospace' }}>
          psf/requests ({statistics.total_entities} entities &bull; {statistics.total_relationships} edges)
        </span>
      </div>

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
            <option value="ALL">All Relationships ({edges.length})</option>
            <option value="CALLS">CALLS (412)</option>
            <option value="DEFINES">DEFINES (557)</option>
            <option value="CONTAINS">CONTAINS (377)</option>
            <option value="IMPORTS">IMPORTS (2)</option>
          </select>
        </div>

        <div>
          <input
            type="text"
            placeholder="Search symbol or file..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{ background: '#0f172a', color: '#fff', padding: '6px 10px', borderRadius: '4px', border: '1px solid #334155', fontSize: '12px', width: '220px' }}
          />
        </div>

        <div style={{ fontSize: '12px', color: '#94a3b8', marginLeft: 'auto' }}>
          Graph Gateway: <code>CGG Read-Only Static Engine</code>
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
        <div style={{ textAlign: 'center', width: '100%' }}>
          <p style={{ color: '#94a3b8', fontSize: '13px', margin: '0 0 20px 0' }}>
            AST Knowledge Graph Topology &bull; Controlled Graph Gateway (CGG) &bull; Snapshot-Isolated ({filteredEntities.length} visible entities, {visibleEdges.length} verified edges)
          </p>

          {/* Render Nodes Grid */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', justifyContent: 'center', alignItems: 'center', margin: '20px 0', maxHeight: '550px', overflowY: 'auto', padding: '10px' }}>
            {filteredEntities.map((n) => {
              const colors = getNodeColor(n.entity_types);
              const isSelected = selectedNode?.entity_id === n.entity_id;
              return (
                <div
                  key={n.entity_id}
                  onClick={() => handleNodeClick(n)}
                  style={{
                    background: colors.bg,
                    padding: '12px 16px',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    border: `2px solid ${colors.border}`,
                    boxShadow: isSelected ? `0 0 16px ${colors.border}` : '0 4px 6px -1px rgba(0,0,0,0.3)',
                    transition: 'all 0.2s ease',
                    textAlign: 'left',
                    minWidth: '180px',
                    maxWidth: '240px',
                  }}
                >
                  <div style={{ fontWeight: 600, fontSize: '13px', color: '#fff', wordBreak: 'break-word' }}>
                    {n.name}
                    {n.entity_types.includes('Function') && '()'}
                  </div>
                  <div style={{ fontSize: '11px', color: '#e2e8f0', marginTop: '4px', wordBreak: 'break-all' }}>
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
            <div style={{ marginTop: '20px', padding: '10px 16px', background: '#0f172a', borderRadius: '6px', display: 'inline-flex', gap: '16px', flexWrap: 'wrap', fontSize: '12px', color: '#94a3b8', maxWidth: '100%', justifyContent: 'center' }}>
              {visibleEdges.slice(0, 3).map((e) => (
                <span key={e.id}>
                  <strong>Verified Edge:</strong> <code>{e.source_name}</code> &mdash;[{e.relationship}]&rarr; <code>{e.target_name}</code>
                </span>
              ))}
              {visibleEdges.length > 3 && (
                <span style={{ color: '#38bdf8' }}>+{visibleEdges.length - 3} more verified relationships</span>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Selected Node Details Drawer */}
      {selectedNode && (
        <div style={{ marginTop: '20px', background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
            <h3 style={{ margin: 0, fontSize: '15px' }}>
              Selected Entity: <code style={{ color: '#38bdf8' }}>{selectedNode.name}</code>
            </h3>
            <button
              onClick={() => setSelectedNode(null)}
              style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer', fontSize: '16px' }}
            >
              &times;
            </button>
          </div>
          <p style={{ margin: '0 0 12px 0', fontSize: '12px', color: '#cbd5e1' }}>
            <strong>File:</strong> <code>{selectedNode.file_path}</code> (Lines {selectedNode.line_start}&ndash;{selectedNode.line_end})
          </p>
          {nodeNeighbors && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              <div>
                <h4 style={{ fontSize: '13px', margin: '0 0 8px 0', color: '#34d399' }}>
                  Outgoing Dependencies ({nodeNeighbors.outgoing.length})
                </h4>
                {nodeNeighbors.outgoing.length === 0 ? (
                  <p style={{ fontSize: '12px', color: '#64748b' }}>No outgoing dependencies</p>
                ) : (
                  <ul style={{ margin: 0, paddingLeft: '18px', fontSize: '12px', color: '#cbd5e1' }}>
                    {nodeNeighbors.outgoing.slice(0, 10).map((e, idx) => (
                      <li key={idx}>
                        [{e.relationship}] &rarr; <code>{e.target_name}</code>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
              <div>
                <h4 style={{ fontSize: '13px', margin: '0 0 8px 0', color: '#60a5fa' }}>
                  Incoming Dependents ({nodeNeighbors.incoming.length})
                </h4>
                {nodeNeighbors.incoming.length === 0 ? (
                  <p style={{ fontSize: '12px', color: '#64748b' }}>No incoming dependents</p>
                ) : (
                  <ul style={{ margin: 0, paddingLeft: '18px', fontSize: '12px', color: '#cbd5e1' }}>
                    {nodeNeighbors.incoming.slice(0, 10).map((e, idx) => (
                      <li key={idx}>
                        [{e.relationship}] &larr; <code>{e.source_name}</code>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
