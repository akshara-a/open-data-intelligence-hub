import React, { useEffect } from 'react';
import { Routes, Route, Link, useLocation, useNavigate, useParams } from 'react-router-dom';
import { useSnapshot } from './context/SnapshotContext';
import { useAuth } from './context/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { RepoExplorerPage } from './pages/RepoExplorerPage';
import { KnowledgeGraphPage } from './pages/KnowledgeGraphPage';
import { AssistantPage } from './pages/AssistantPage';
import { ImpactAnalysisPage } from './pages/ImpactAnalysisPage';
import { ReportViewerPage } from './pages/ReportViewerPage';
import { EvaluationPage } from './pages/EvaluationPage';
import { SettingsPage } from './pages/SettingsPage';
import { UserManagementPage } from './pages/UserManagementPage';

export const App: React.FC = () => {
  const {
    activeRepoId,
    activeCommitSha,
    repositories,
    snapshots,
    isLoadingRepos,
    isLoadingSnapshots,
    setActiveSnapshot,
    selectRepo,
  } = useSnapshot();

  const { user, isAuthenticated, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login', { replace: true });
  };

  const handleRepoChange = async (newRepoId: string) => {
    await selectRepo(newRepoId);
    // Sync current URL if on a repository-scoped page
    const segments = location.pathname.split('/');
    if (segments.length >= 5 && segments[3] === 'snapshot') {
      const tool = segments[1];
      navigate(`/${tool}/${newRepoId}/snapshot/${activeCommitSha}`);
    }
  };

  const handleCommitChange = (newCommitSha: string) => {
    setActiveSnapshot(activeRepoId, newCommitSha);
    const segments = location.pathname.split('/');
    if (segments.length >= 5 && segments[3] === 'snapshot') {
      const tool = segments[1];
      navigate(`/${tool}/${activeRepoId}/snapshot/${newCommitSha}`);
    }
  };

  const role = user?.role?.toLowerCase() || 'viewer';
  const navLinks: { name: string; path: string }[] = [
    { name: '1. Dashboard', path: '/' },
    { name: '2. Explorer', path: `/repo/${activeRepoId}/snapshot/${activeCommitSha}` },
    { name: '3. Knowledge Graph', path: `/graph/${activeRepoId}/snapshot/${activeCommitSha}` },
  ];

  // AI Assistant is accessible to admin, reviewer, and viewer (scoped to authorized repositories)
  navLinks.push({ name: '4. AI Assistant', path: `/assistant/${activeRepoId}/snapshot/${activeCommitSha}` });

  if (role === 'admin' || role === 'reviewer') {
    navLinks.push({ name: '5. Impact Analysis', path: `/impact/${activeRepoId}/snapshot/${activeCommitSha}` });
  }

  navLinks.push({ name: '6. Reports', path: `/report/${activeRepoId}/qry_sample_01` });

  if (role === 'admin') {
    navLinks.push({ name: '7. Evaluation', path: '/evaluation' });
  }

  navLinks.push({ name: '8. Settings', path: '/settings' });

  if (role === 'admin') {
    navLinks.push({ name: '9. Users (Admin)', path: '/admin/users' });
  }

  // If on login route, render full-screen login without nav bars
  if (location.pathname === '/login') {
    return (
      <Routes>
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    );
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Header */}
      <header
        style={{
          background: '#090d16',
          padding: '10px 24px',
          borderBottom: '1px solid #1e293b',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '12px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#3b82f6' }} />
          <h1 style={{ fontSize: '17px', margin: 0, fontWeight: 600, color: '#f8fafc' }}>
            Autonomous Codebase Knowledge Graph Navigator
          </h1>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          {/* Active Snapshot Context Controller */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              background: '#1e293b',
              padding: '5px 12px',
              borderRadius: '6px',
              border: '1px solid #334155',
            }}
          >
            <span style={{ fontSize: '12px', color: '#94a3b8' }}>Active Snapshot:</span>
            {/* Dynamic Repository Selector */}
            <select
              value={activeRepoId}
              onChange={(e) => handleRepoChange(e.target.value)}
              disabled={isLoadingRepos}
              style={{
                background: '#0f172a',
                color: '#fff',
                border: '1px solid #334155',
                borderRadius: '4px',
                padding: '4px 8px',
                fontSize: '12px',
                maxWidth: '220px',
              }}
              title="Select active repository"
            >
              {repositories.length > 0 ? (
                repositories.map((r) => (
                  <option key={r.repo_id} value={r.repo_id}>
                    {r.name && r.name !== r.repo_id ? `${r.name} (${r.repo_id.substring(0, 8)})` : r.repo_id}
                  </option>
                ))
              ) : (
                <option value={activeRepoId}>{activeRepoId}</option>
              )}
            </select>

            {/* Dynamic Snapshot Commit Selector */}
            {snapshots.length > 0 ? (
              <select
                value={activeCommitSha}
                onChange={(e) => handleCommitChange(e.target.value)}
                disabled={isLoadingSnapshots}
                style={{
                  background: '#0f172a',
                  color: '#38bdf8',
                  border: '1px solid #334155',
                  borderRadius: '4px',
                  padding: '4px 8px',
                  fontSize: '12px',
                  fontFamily: 'monospace',
                  maxWidth: '220px',
                }}
                title="Select active commit snapshot"
              >
                {snapshots.map((s) => (
                  <option key={s.commit_sha} value={s.commit_sha}>
                    {s.commit_sha.substring(0, 10)} {s.created_at ? `(${s.created_at.substring(0, 10)})` : ''}
                  </option>
                ))}
              </select>
            ) : (
              <input
                type="text"
                value={activeCommitSha}
                onChange={(e) => handleCommitChange(e.target.value)}
                style={{
                  background: '#0f172a',
                  color: '#38bdf8',
                  border: '1px solid #334155',
                  borderRadius: '4px',
                  padding: '4px 8px',
                  fontSize: '12px',
                  width: '200px',
                  fontFamily: 'monospace',
                }}
                title="Active Snapshot Commit SHA"
              />
            )}
          </div>

          {/* User Profile & Logout Controls */}
          {isAuthenticated && user && (
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                paddingLeft: '12px',
                borderLeft: '1px solid #334155',
              }}
            >
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', lineHeight: '1.2' }}>
                <span style={{ fontSize: '12px', fontWeight: 600, color: '#e2e8f0' }}>{user.username}</span>
                <span
                  style={{
                    fontSize: '10px',
                    color: user.role === 'admin' ? '#38bdf8' : user.role === 'reviewer' ? '#a78bfa' : '#34d399',
                    textTransform: 'uppercase',
                    letterSpacing: '0.05em',
                  }}
                >
                  {user.role}
                </span>
              </div>
              <button
                onClick={handleLogout}
                style={{
                  background: '#1e293b',
                  border: '1px solid #ef4444',
                  color: '#f87171',
                  borderRadius: '6px',
                  padding: '5px 10px',
                  fontSize: '11px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  transition: 'background 0.2s',
                }}
                title="Sign out of active session"
              >
                Sign Out
              </button>
            </div>
          )}
        </div>
      </header>

      {/* Navigation Bar */}
      <nav
        style={{
          background: '#0f172a',
          borderBottom: '1px solid #1e293b',
          display: 'flex',
          padding: '0 24px',
          gap: '8px',
          overflowX: 'auto',
        }}
      >
        {navLinks.map((link) => {
          const isActive =
            location.pathname === link.path ||
            (link.path !== '/' && location.pathname.startsWith(link.path.split('/')[1]));
          return (
            <Link
              key={link.name}
              to={link.path}
              style={{
                padding: '12px 14px',
                fontSize: '13px',
                color: isActive ? '#38bdf8' : '#94a3b8',
                borderBottom: isActive ? '2px solid #38bdf8' : '2px solid transparent',
                textDecoration: 'none',
                fontWeight: isActive ? 600 : 400,
                whiteSpace: 'nowrap',
              }}
            >
              {link.name}
            </Link>
          );
        })}
      </nav>

      {/* Main Content View with Protected Routes */}
      <main style={{ flex: 1 }}>
        <Routes>
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/repo/:repoId/snapshot/:commitSha"
            element={
              <ProtectedRoute>
                <RepoExplorerPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/graph/:repoId/snapshot/:commitSha"
            element={
              <ProtectedRoute>
                <KnowledgeGraphPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/assistant/:repoId/snapshot/:commitSha"
            element={
              <ProtectedRoute>
                <AssistantPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/impact/:repoId/snapshot/:commitSha"
            element={
              <ProtectedRoute>
                <ImpactAnalysisPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/repo/:repoId/snapshot/:commitSha/impact"
            element={
              <ProtectedRoute>
                <ImpactAnalysisPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/report/:repoId/:queryId"
            element={
              <ProtectedRoute>
                <ReportViewerPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/repo/:repoId/snapshot/:commitSha/reports"
            element={
              <ProtectedRoute>
                <ReportViewerPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/reports/:repoId/snapshot/:commitSha"
            element={
              <ProtectedRoute>
                <ReportViewerPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/evaluation"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <EvaluationPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/settings"
            element={
              <ProtectedRoute>
                <SettingsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin/users"
            element={
              <ProtectedRoute allowedRoles={['admin']}>
                <UserManagementPage />
              </ProtectedRoute>
            }
          />
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="*"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
        </Routes>
      </main>
    </div>
  );
};
