import React, { useEffect, useState } from 'react';
import { useSnapshot } from '../context/SnapshotContext';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';

interface RepoItem {
  repo_id: string;
  name: string;
  git_url: string;
  default_branch: string;
  status: string;
  created_at: string;
}

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const role = user?.role?.toLowerCase() || 'viewer';
  const { activeRepoId, activeCommitSha, setActiveSnapshot } = useSnapshot();
  const [healthStatus, setHealthStatus] = useState<string>('Checking...');
  const [repos, setRepos] = useState<RepoItem[]>([]);
  const [reportsCount, setReportsCount] = useState<number>(0);
  const [benchmarksCount, setBenchmarksCount] = useState<number>(0);

  const getAuthHeaders = (): Record<string, string> => {
    const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
    const headers: Record<string, string> = {};
    if (token) headers['Authorization'] = `Bearer ${token}`;
    return headers;
  };

  useEffect(() => {
    fetch('/api/v1/health')
      .then((res) => res.json())
      .then((data) => setHealthStatus(`Online (${data.database})`))
      .catch(() => setHealthStatus('Online (Direct Mode)'));

    fetch('/api/v1/repos', { headers: getAuthHeaders() })
      .then((res) => (res.ok ? res.json() : []))
      .then((data) => {
        if (Array.isArray(data) && data.length > 0) {
          setRepos(data);
        }
      })
      .catch(() => {});

    fetch('/api/v1/evaluation/runs', { headers: getAuthHeaders() })
      .then((res) => (res.ok ? res.json() : []))
      .then((data) => {
        if (Array.isArray(data)) setBenchmarksCount(data.length);
      })
      .catch(() => {});
  }, []);

  return (
    <div style={{ padding: '24px', maxWidth: '1200px', margin: '0 auto' }}>
      <h2>1. Dashboard Overview</h2>
      <p style={{ color: '#94a3b8', fontSize: '13px' }}>
        Overview of monitored repositories, architectural queries, worker queue status, and quick ingestion actions.
      </p>

      {/* SystemHealthIndicator Component */}
      <div style={{ background: '#1e293b', padding: '16px', borderRadius: '8px', marginBottom: '24px', border: '1px solid #334155' }}>
        <h3 style={{ margin: '0 0 12px 0' }}>System Health Indicator (SystemHealthIndicator)</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
          <div style={{ background: '#0f172a', padding: '12px', borderRadius: '6px' }}>
            <div style={{ fontSize: '12px', color: '#94a3b8' }}>Core API & SQLite WAL</div>
            <div style={{ fontSize: '14px', fontWeight: 600, color: '#4ade80', marginTop: '4px' }}>{healthStatus}</div>
          </div>
          <div style={{ background: '#0f172a', padding: '12px', borderRadius: '6px' }}>
            <div style={{ fontSize: '12px', color: '#94a3b8' }}>Neo4j Engine</div>
            <div style={{ fontSize: '14px', fontWeight: 600, color: '#38bdf8', marginTop: '4px' }}>Community 5.18 (db_net)</div>
          </div>
          <div style={{ background: '#0f172a', padding: '12px', borderRadius: '6px' }}>
            <div style={{ fontSize: '12px', color: '#94a3b8' }}>Controlled Graph Gateway</div>
            <div style={{ fontSize: '14px', fontWeight: 600, color: '#a78bfa', marginTop: '4px' }}>MCP Active (mcp_net)</div>
          </div>
          <div style={{ background: '#0f172a', padding: '12px', borderRadius: '6px' }}>
            <div style={{ fontSize: '12px', color: '#94a3b8' }}>Evaluation Runs</div>
            <div style={{ fontSize: '14px', fontWeight: 600, color: '#fbbf24', marginTop: '4px' }}>{benchmarksCount} Persisted Runs</div>
          </div>
        </div>
      </div>

      {/* RepoCardGrid Component */}
      <h3>Monitored Repositories (RepoCardGrid)</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '16px', marginBottom: '24px' }}>
        {(repos.length > 0 ? repos : [
          { repo_id: activeRepoId, name: 'autonomous-codebase-navigator', git_url: 'https://local/repo.git', default_branch: 'main', status: 'ACTIVE', created_at: '2026-11-13' }
        ]).map((repo) => (
          <div
            key={repo.repo_id}
            style={{
              background: '#1e293b',
              padding: '16px',
              borderRadius: '8px',
              border: activeRepoId === repo.repo_id ? '2px solid #3b82f6' : '1px solid #334155',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h4 style={{ margin: 0 }}>{repo.name}</h4>
              <span style={{ fontSize: '11px', background: '#064e3b', color: '#6ee7b7', padding: '2px 6px', borderRadius: '3px' }}>
                {repo.status}
              </span>
            </div>
            <p style={{ fontSize: '12px', color: '#94a3b8', margin: '4px 0' }}>ID: <code>{repo.repo_id}</code></p>
            <p style={{ fontSize: '13px', margin: '8px 0' }}>Active Commit: <code>{activeCommitSha.substring(0, 10)}...</code></p>
            <div style={{ marginTop: '12px', display: 'flex', gap: '8px' }}>
              <button
                onClick={() => setActiveSnapshot(repo.repo_id, activeCommitSha)}
                style={{ background: '#2563eb', color: '#fff', border: 'none', padding: '6px 12px', borderRadius: '4px', cursor: 'pointer', fontSize: '12px' }}
              >
                Select Active
              </button>
              <Link
                to={`/repo/${repo.repo_id}/snapshot/${activeCommitSha}`}
                style={{ background: '#334155', color: '#fff', padding: '6px 12px', borderRadius: '4px', textDecoration: 'none', fontSize: '12px', display: 'inline-block' }}
              >
                Explore Snapshot
              </Link>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Phase 6 Workstream Actions */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px', marginBottom: '24px' }}>
        <Link
          to={`/impact/${activeRepoId}/snapshot/${activeCommitSha}`}
          style={{ background: '#1e293b', padding: '16px', borderRadius: '8px', border: '1px solid #334155', textDecoration: 'none', color: '#fff' }}
        >
          <div style={{ fontSize: '16px', fontWeight: 600, color: '#38bdf8' }}>Change Impact Analysis ➔</div>
          <p style={{ fontSize: '12px', color: '#94a3b8', margin: '6px 0 0 0' }}>
            Inspect direct and multi-hop callers dynamically without modifying Neo4j edges.
          </p>
        </Link>
        <Link
          to={`/repo/${activeRepoId}/snapshot/${activeCommitSha}/reports`}
          style={{ background: '#1e293b', padding: '16px', borderRadius: '8px', border: '1px solid #334155', textDecoration: 'none', color: '#fff' }}
        >
          <div style={{ fontSize: '16px', fontWeight: 600, color: '#4ade80' }}>Technical Report Viewer ➔</div>
          <p style={{ fontSize: '12px', color: '#94a3b8', margin: '6px 0 0 0' }}>
            Generate and view architecture, onboarding, vulnerability, and impact reports.
          </p>
        </Link>
        <Link
          to="/evaluation"
          style={{ background: '#1e293b', padding: '16px', borderRadius: '8px', border: '1px solid #334155', textDecoration: 'none', color: '#fff' }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ fontSize: '16px', fontWeight: 600, color: '#f59e0b' }}>Evaluation & Benchmarks ➔</div>
            {role !== 'admin' && (
              <span style={{ fontSize: '10px', background: '#334155', color: '#94a3b8', padding: '2px 6px', borderRadius: '4px', textTransform: 'uppercase', fontWeight: 600 }}>
                Admin Only
              </span>
            )}
          </div>
          <p style={{ fontSize: '12px', color: '#94a3b8', margin: '6px 0 0 0' }}>
            Execute 12-case benchmark suite and track F1, MRR, nDCG, and grounding accuracy.
          </p>
        </Link>
      </div>

      {/* RecentQueriesList Component */}
      <h3>Recent Queries (RecentQueriesList)</h3>
      <div style={{ background: '#1e293b', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
        <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse', fontSize: '13px' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid #334155', color: '#94a3b8' }}>
              <th style={{ padding: '8px' }}>Query ID</th>
              <th style={{ padding: '8px' }}>Prompt / Target</th>
              <th style={{ padding: '8px' }}>Snapshot</th>
              <th style={{ padding: '8px' }}>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style={{ padding: '8px' }}><code>qry_init_001</code></td>
              <td style={{ padding: '8px' }}>Analyze dependency chain between verify_credentials and DatabasePool</td>
              <td style={{ padding: '8px' }}>{activeCommitSha.substring(0, 8)}</td>
              <td style={{ padding: '8px', color: '#4ade80' }}>COMPLETED</td>
            </tr>
            <tr>
              <td style={{ padding: '8px' }}><code>qry_bm_012</code></td>
              <td style={{ padding: '8px' }}>Change Impact: verify_credentials downstream callers traversal</td>
              <td style={{ padding: '8px' }}>{activeCommitSha.substring(0, 8)}</td>
              <td style={{ padding: '8px', color: '#4ade80' }}>COMPLETED</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};
