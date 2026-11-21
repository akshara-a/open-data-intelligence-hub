import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useSnapshot } from '../context/SnapshotContext';

interface ImpactedEntity {
  entity_id: string;
  name: string;
  file_path: string;
  line_start?: number;
  line_end?: number;
  entity_type?: string;
  impact_classification: string;
  impact_level?: string;
  hop_distance: number;
  relationship_types: string[];
  traversal_path: string[];
  evidence_ids: string[];
  confidence: number;
  is_uncertain: boolean;
  rationale: string;
  suggested_verification: string;
}

interface ImpactResponse {
  repo_id: string;
  commit_sha: string;
  target_entity?: string;
  target_found: boolean;
  summary: string;
  max_depth_analyzed: number;
  direct_impacted: ImpactedEntity[];
  transitive_impacted: ImpactedEntity[];
  unresolved_impacted: ImpactedEntity[];
  total_impacted_count: number;
  all_evidence_ids: string[];
  recommendations: string[];
  execution_time_ms: number;
}

export const ImpactAnalysisPage: React.FC = () => {
  const params = useParams<{ repoId: string; commitSha: string }>();
  const { activeRepoId, activeCommitSha } = useSnapshot();

  const repoId = params.repoId || activeRepoId;
  const commitSha = params.commitSha || activeCommitSha;

  const [selectedEntity, setSelectedEntity] = useState<string>('verify_credentials');
  const [customEntity, setCustomEntity] = useState<string>('');
  const [maxDepth, setMaxDepth] = useState<number>(2);
  const [confidenceThreshold, setConfidenceThreshold] = useState<number>(0.5);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [impactData, setImpactData] = useState<ImpactResponse | null>(null);

  const getAuthHeaders = (): Record<string, string> => {
    const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;
    return headers;
  };

  const runAnalysis = async () => {
    const target = customEntity.trim() || selectedEntity;
    if (!target) return;
    setLoading(true);
    setError(null);
    try {
      const resp = await fetch(`/api/v1/repos/${repoId}/snapshots/${commitSha}/impact/analyze`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({
          target_entity: target,
          max_depth: maxDepth,
          confidence_threshold: confidenceThreshold,
        }),
      });
      if (!resp.ok) {
        const errJson = await resp.json().catch(() => ({ detail: `HTTP ${resp.status}` }));
        throw new Error(errJson.detail || `Analysis failed with HTTP ${resp.status}`);
      }
      const data = await resp.json();
      setImpactData(data);
    } catch (e: any) {
      setError(e.message || 'Change impact analysis failed.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runAnalysis();
  }, [repoId, commitSha]);

  const exportJson = () => {
    if (!impactData) return;
    const blob = new Blob([JSON.stringify(impactData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `impact_analysis_${impactData.target_entity || 'target'}_${commitSha.substring(0, 8)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const exportCsv = () => {
    if (!impactData) return;
    const all = [
      ...(impactData.direct_impacted || []),
      ...(impactData.transitive_impacted || []),
      ...(impactData.unresolved_impacted || []),
    ];
    const headers = ['Entity ID', 'Name', 'File Path', 'Classification', 'Hop Distance', 'Confidence', 'Evidence IDs', 'Rationale'];
    const rows = all.map((e) => [
      `"${e.entity_id}"`,
      `"${e.name}"`,
      `"${e.file_path}"`,
      `"${e.impact_classification || e.impact_level || 'direct_impact'}"`,
      e.hop_distance,
      e.confidence,
      `"${(e.evidence_ids || []).join(';')}"`,
      `"${(e.rationale || '').replace(/"/g, '""')}"`,
    ]);
    const csvContent = [headers.join(','), ...rows.map((r) => r.join(','))].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `impact_matrix_${impactData.target_entity || 'target'}_${commitSha.substring(0, 8)}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <div>
          <h2 style={{ margin: 0 }}>5. Change Impact Analysis</h2>
          <p style={{ color: '#94a3b8', fontSize: '13px', margin: '4px 0 0 0' }}>
            Multi-hop dependency traversal, callers discovery, and dynamic unresolvable call detection. Strictly isolated to snapshot.
          </p>
        </div>
        <div style={{ background: '#0f172a', border: '1px solid #334155', padding: '6px 12px', borderRadius: '6px', fontSize: '12px' }}>
          <strong>Snapshot:</strong> <code>{repoId}</code> @ <code>{commitSha.substring(0, 8)}</code>
        </div>
      </div>

      {/* EntitySelector & ExportActionToolbar Components */}
      <div style={{ background: '#1e293b', padding: '16px', borderRadius: '8px', marginBottom: '20px', border: '1px solid #334155' }}>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', alignItems: 'center', justifyContent: 'space-between' }}>
          {/* EntitySelector */}
          <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>
                Root Target Entity (EntitySelector)
              </label>
              <select
                value={selectedEntity}
                onChange={(e) => {
                  setSelectedEntity(e.target.value);
                  setCustomEntity('');
                }}
                style={{ background: '#0f172a', color: '#fff', border: '1px solid #475569', padding: '6px 12px', borderRadius: '4px', fontSize: '13px' }}
              >
                <option value="verify_credentials">verify_credentials (auth_service.py)</option>
                <option value="DatabasePool">DatabasePool (db_pool.py)</option>
                <option value="login_handler">login_handler (api_router.py)</option>
                <option value="query">DatabasePool.query</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>
                Or Custom Symbol:
              </label>
              <input
                type="text"
                placeholder="e.g. hash_password"
                value={customEntity}
                onChange={(e) => setCustomEntity(e.target.value)}
                style={{ background: '#0f172a', color: '#fff', border: '1px solid #475569', padding: '6px 12px', borderRadius: '4px', fontSize: '13px', width: '160px' }}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>
                Max Traversal Depth: {maxDepth}
              </label>
              <select
                value={maxDepth}
                onChange={(e) => setMaxDepth(Number(e.target.value))}
                style={{ background: '#0f172a', color: '#fff', border: '1px solid #475569', padding: '6px 12px', borderRadius: '4px', fontSize: '13px' }}
              >
                <option value={1}>1 Hop (Direct Callers)</option>
                <option value={2}>2 Hops (Transitive Callers)</option>
                <option value={3}>3 Hops (Full Impact Scope)</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '12px', color: '#94a3b8', marginBottom: '4px' }}>
                Confidence Threshold: {confidenceThreshold}
              </label>
              <input
                type="range"
                min="0.1"
                max="1.0"
                step="0.1"
                value={confidenceThreshold}
                onChange={(e) => setConfidenceThreshold(Number(e.target.value))}
                style={{ width: '100px' }}
              />
            </div>

            <button
              onClick={runAnalysis}
              disabled={loading}
              style={{
                background: loading ? '#475569' : '#2563eb',
                color: '#fff',
                border: 'none',
                padding: '8px 16px',
                borderRadius: '4px',
                cursor: loading ? 'not-allowed' : 'pointer',
                fontWeight: 600,
                marginTop: '16px',
              }}
            >
              {loading ? 'Analyzing...' : 'Run Analysis'}
            </button>
          </div>

          {/* ExportActionToolbar Component */}
          <div style={{ display: 'flex', gap: '8px', marginTop: '16px' }}>
            <button
              onClick={exportJson}
              disabled={!impactData}
              style={{ background: '#334155', color: '#fff', border: 'none', padding: '6px 12px', borderRadius: '4px', cursor: impactData ? 'pointer' : 'not-allowed', fontSize: '13px' }}
            >
              Export JSON (ExportActionToolbar)
            </button>
            <button
              onClick={exportCsv}
              disabled={!impactData}
              style={{ background: '#0ea5e9', color: '#fff', border: 'none', padding: '6px 12px', borderRadius: '4px', cursor: impactData ? 'pointer' : 'not-allowed', fontSize: '13px' }}
            >
              Export CSV
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div style={{ background: '#7f1d1d', border: '1px solid #b91c1c', color: '#fecaca', padding: '12px 16px', borderRadius: '6px', marginBottom: '16px' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {impactData && (
        <div style={{ background: '#0f172a', border: '1px solid #334155', padding: '14px 18px', borderRadius: '8px', marginBottom: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <span style={{ fontSize: '15px', fontWeight: 600 }}>{impactData.summary}</span>
              <div style={{ fontSize: '12px', color: '#94a3b8', marginTop: '4px' }}>
                Execution Time: {impactData.execution_time_ms} ms | Target Found: {impactData.target_found ? 'YES' : 'NO'} | Graph Mutated: NO (strictly dynamic)
              </div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <span style={{ fontSize: '24px', fontWeight: 700, color: '#38bdf8' }}>{impactData.total_impacted_count}</span>
              <div style={{ fontSize: '11px', color: '#94a3b8' }}>Total Impacted Entities</div>
            </div>
          </div>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* ImpactSubGraphView Component */}
        <div style={{ background: '#1e293b', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
          <h3>Verified Subgraph View (ImpactSubGraphView)</h3>
          <p style={{ fontSize: '13px', color: '#94a3b8' }}>Verified static AST dependencies (No persisted AFFECTS edges)</p>

          <div style={{ marginTop: '12px' }}>
            <h4 style={{ fontSize: '13px', color: '#4ade80', margin: '8px 0' }}>
              Direct Incoming Callers ({(impactData?.direct_impacted || []).length})
            </h4>
            {(impactData?.direct_impacted || []).length === 0 ? (
              <p style={{ fontSize: '12px', color: '#64748b' }}>No direct incoming callers identified in snapshot.</p>
            ) : (
              (impactData?.direct_impacted || []).map((d) => (
                <div key={d.entity_id} style={{ background: '#0f172a', padding: '10px 14px', borderRadius: '6px', marginBottom: '8px', fontSize: '13px', borderLeft: '3px solid #4ade80' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <strong>🟢 {d.name}</strong>
                    <span style={{ fontSize: '11px', color: '#94a3b8' }}>{d.entity_type}</span>
                  </div>
                  <div style={{ color: '#94a3b8', fontSize: '12px', marginTop: '2px' }}>
                    <code>{d.file_path}</code>
                  </div>
                  <div style={{ fontSize: '12px', color: '#cbd5e1', marginTop: '4px' }}>{d.rationale}</div>
                  {d.evidence_ids && d.evidence_ids.length > 0 && (
                    <div style={{ marginTop: '4px' }}>
                      {d.evidence_ids.map((eid) => (
                        <span key={eid} style={{ background: '#1e3a8a', color: '#93c5fd', fontSize: '11px', padding: '2px 6px', borderRadius: '3px', marginRight: '4px' }}>
                          Evidence: {eid}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))
            )}

            <h4 style={{ fontSize: '13px', color: '#38bdf8', margin: '16px 0 8px 0' }}>
              Transitive Dependents ({(impactData?.transitive_impacted || []).length})
            </h4>
            {(impactData?.transitive_impacted || []).length === 0 ? (
              <p style={{ fontSize: '12px', color: '#64748b' }}>No transitive dependents within max depth.</p>
            ) : (
              (impactData?.transitive_impacted || []).map((t) => (
                <div key={t.entity_id} style={{ background: '#0f172a', padding: '10px 14px', borderRadius: '6px', marginBottom: '8px', fontSize: '13px', borderLeft: '3px solid #38bdf8' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <strong>🔵 {t.name}</strong>
                    <span style={{ fontSize: '11px', color: '#94a3b8' }}>Hop Distance: {t.hop_distance}</span>
                  </div>
                  <div style={{ color: '#94a3b8', fontSize: '12px' }}><code>{t.file_path}</code></div>
                  <div style={{ fontSize: '12px', color: '#cbd5e1', marginTop: '4px' }}>{t.rationale}</div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* DynamicInferenceMatrix Component */}
        <div style={{ background: '#1e293b', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
          <h3>Dynamic Inference Matrix (DynamicInferenceMatrix)</h3>
          <p style={{ fontSize: '13px', color: '#94a3b8' }}>
            Dynamically computed impacts with inference rules, unresolved calls & risk score
          </p>

          <div style={{ marginTop: '12px' }}>
            <h4 style={{ fontSize: '13px', color: '#f59e0b', margin: '8px 0' }}>
              Unresolved / Dynamic Dispatch Sites ({(impactData?.unresolved_impacted || []).length})
            </h4>
            {(impactData?.unresolved_impacted || []).length === 0 ? (
              <p style={{ fontSize: '12px', color: '#64748b' }}>No unresolved dynamic calls in impact boundary.</p>
            ) : (
              (impactData?.unresolved_impacted || []).map((u) => (
                <div key={u.entity_id} style={{ background: '#0f172a', padding: '10px 14px', borderRadius: '6px', marginBottom: '8px', fontSize: '13px', borderLeft: '3px solid #f59e0b' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong>⚠️ {u.name}</strong>
                    <span style={{ background: '#78350f', color: '#fde68a', fontSize: '11px', padding: '2px 6px', borderRadius: '3px' }}>
                      potential_uncertain (conf: {u.confidence})
                    </span>
                  </div>
                  <div style={{ color: '#94a3b8', fontSize: '12px' }}><code>{u.file_path}</code></div>
                  <div style={{ fontSize: '12px', color: '#cbd5e1', marginTop: '4px' }}>{u.rationale}</div>
                  <div style={{ fontSize: '12px', color: '#fbbf24', marginTop: '4px' }}>
                    <em>Recommendation: {u.suggested_verification}</em>
                  </div>
                </div>
              ))
            )}

            {impactData?.recommendations && impactData.recommendations.length > 0 && (
              <div style={{ marginTop: '20px', borderTop: '1px solid #334155', paddingTop: '12px' }}>
                <h4 style={{ fontSize: '13px', color: '#fff', margin: '0 0 8px 0' }}>Engineering Recommendations</h4>
                <ul style={{ margin: 0, paddingLeft: '18px', fontSize: '12px', color: '#cbd5e1', lineHeight: '1.6' }}>
                  {impactData.recommendations.map((r, i) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
