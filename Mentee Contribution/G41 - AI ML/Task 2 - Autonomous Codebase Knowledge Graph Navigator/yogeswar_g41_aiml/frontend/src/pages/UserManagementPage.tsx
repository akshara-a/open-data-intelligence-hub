import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { useSnapshot } from '../context/SnapshotContext';

interface UserItem {
  user_id: string;
  username: string;
  role: string;
  is_active: boolean;
  created_at?: string;
}

interface MemberItem {
  id: string;
  user_id: string;
  username: string;
  role: string;
  created_at?: string;
}

export const UserManagementPage: React.FC = () => {
  const { authFetch, user: currentUser } = useAuth();
  const { repositories } = useSnapshot();

  // Users state
  const [users, setUsers] = useState<UserItem[]>([]);
  const [isLoadingUsers, setIsLoadingUsers] = useState<boolean>(true);
  const [userError, setUserError] = useState<string | null>(null);
  const [userSuccess, setUserSuccess] = useState<string | null>(null);

  // New user form state
  const [newUsername, setNewUsername] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newRole, setNewRole] = useState<'admin' | 'reviewer' | 'viewer'>('reviewer');
  const [isCreatingUser, setIsCreatingUser] = useState(false);

  // Password reset modal state
  const [resetModalUserId, setResetModalUserId] = useState<string | null>(null);
  const [resetModalUsername, setResetModalUsername] = useState<string>('');
  const [resetPasswordInput, setResetPasswordInput] = useState<string>('');
  const [isResetting, setIsResetting] = useState(false);

  // Repository memberships state
  const [selectedRepoId, setSelectedRepoId] = useState<string>('');
  const [members, setMembers] = useState<MemberItem[]>([]);
  const [isLoadingMembers, setIsLoadingMembers] = useState<boolean>(false);
  const [assignUserId, setAssignUserId] = useState<string>('');
  const [assignRole, setAssignRole] = useState<'reviewer' | 'viewer'>('reviewer');
  const [isAssigning, setIsAssigning] = useState<boolean>(false);

  const fetchUsers = useCallback(async () => {
    setIsLoadingUsers(true);
    setUserError(null);
    try {
      const resp = await authFetch('/api/v1/users');
      if (!resp.ok) {
        throw new Error(`Failed to load users: ${resp.status} ${resp.statusText}`);
      }
      const data: UserItem[] = await resp.json();
      setUsers(data);
    } catch (err: any) {
      setUserError(err.message || 'Error loading user directory');
    } finally {
      setIsLoadingUsers(false);
    }
  }, [authFetch]);

  const fetchMembers = useCallback(async (repoId: string) => {
    if (!repoId) return;
    setIsLoadingMembers(true);
    try {
      const resp = await authFetch(`/api/v1/repos/${repoId}/members`);
      if (resp.ok) {
        const data: MemberItem[] = await resp.json();
        setMembers(data);
      } else {
        setMembers([]);
      }
    } catch (err) {
      setMembers([]);
    } finally {
      setIsLoadingMembers(false);
    }
  }, [authFetch]);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  useEffect(() => {
    if (repositories.length > 0 && !selectedRepoId) {
      setSelectedRepoId(repositories[0].repo_id);
    }
  }, [repositories, selectedRepoId]);

  useEffect(() => {
    if (selectedRepoId) {
      fetchMembers(selectedRepoId);
    }
  }, [selectedRepoId, fetchMembers]);

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    setUserError(null);
    setUserSuccess(null);
    if (!newUsername.trim() || !newPassword.trim()) {
      setUserError('Please provide both username and initial password.');
      return;
    }
    setIsCreatingUser(true);
    try {
      const resp = await authFetch('/api/v1/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: newUsername.trim(),
          password: newPassword,
          role: newRole,
        }),
      });
      if (!resp.ok) {
        const errData = await resp.json().catch(() => ({}));
        throw new Error(errData.detail || 'Failed to create user account');
      }
      setUserSuccess(`User account '${newUsername}' created successfully with role ${newRole.toUpperCase()}.`);
      setNewUsername('');
      setNewPassword('');
      setNewRole('reviewer');
      await fetchUsers();
    } catch (err: any) {
      setUserError(err.message || 'Failed to create user account');
    } finally {
      setIsCreatingUser(false);
    }
  };

  const handleToggleStatus = async (targetUser: UserItem) => {
    setUserError(null);
    setUserSuccess(null);
    try {
      const resp = await authFetch(`/api/v1/users/${targetUser.user_id}/status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_active: !targetUser.is_active }),
      });
      if (!resp.ok) {
        const errData = await resp.json().catch(() => ({}));
        throw new Error(errData.detail || 'Failed to update user status');
      }
      setUserSuccess(`User '${targetUser.username}' is now ${!targetUser.is_active ? 'ACTIVE' : 'DEACTIVATED'}.`);
      await fetchUsers();
    } catch (err: any) {
      setUserError(err.message || 'Error updating account status');
    }
  };

  const handleRoleChange = async (targetUserId: string, newTargetRole: string) => {
    setUserError(null);
    setUserSuccess(null);
    try {
      const resp = await authFetch(`/api/v1/users/${targetUserId}/role`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role: newTargetRole }),
      });
      if (!resp.ok) {
        const errData = await resp.json().catch(() => ({}));
        throw new Error(errData.detail || 'Failed to update user role');
      }
      setUserSuccess(`User role updated to ${newTargetRole.toUpperCase()}.`);
      await fetchUsers();
    } catch (err: any) {
      setUserError(err.message || 'Error updating user role');
    }
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!resetModalUserId || !resetPasswordInput.trim()) return;
    setIsResetting(true);
    setUserError(null);
    setUserSuccess(null);
    try {
      const resp = await authFetch(`/api/v1/users/${resetModalUserId}/password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ new_password: resetPasswordInput.trim() }),
      });
      if (!resp.ok) {
        const errData = await resp.json().catch(() => ({}));
        throw new Error(errData.detail || 'Password reset failed');
      }
      setUserSuccess(`Password for '${resetModalUsername}' reset successfully. Active sessions revoked.`);
      setResetModalUserId(null);
      setResetPasswordInput('');
    } catch (err: any) {
      setUserError(err.message || 'Failed to reset password');
    } finally {
      setIsResetting(false);
    }
  };

  const handleAssignMember = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedRepoId || !assignUserId) return;
    setIsAssigning(true);
    setUserError(null);
    setUserSuccess(null);
    try {
      const resp = await authFetch(`/api/v1/repos/${selectedRepoId}/members`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: assignUserId, role: assignRole }),
      });
      if (!resp.ok) {
        const errData = await resp.json().catch(() => ({}));
        throw new Error(errData.detail || 'Failed to assign repository membership');
      }
      setUserSuccess(`Repository membership assigned.`);
      await fetchMembers(selectedRepoId);
    } catch (err: any) {
      setUserError(err.message || 'Failed to assign membership');
    } finally {
      setIsAssigning(false);
    }
  };

  const handleRevokeMember = async (targetUserId: string) => {
    if (!selectedRepoId) return;
    setUserError(null);
    setUserSuccess(null);
    try {
      const resp = await authFetch(`/api/v1/repos/${selectedRepoId}/members/${targetUserId}`, {
        method: 'DELETE',
      });
      if (!resp.ok) {
        const errData = await resp.json().catch(() => ({}));
        throw new Error(errData.detail || 'Failed to revoke repository membership');
      }
      setUserSuccess('Repository membership revoked.');
      await fetchMembers(selectedRepoId);
    } catch (err: any) {
      setUserError(err.message || 'Failed to revoke membership');
    }
  };

  return (
    <div style={{ padding: '24px', maxWidth: '1280px', margin: '0 auto' }}>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '24px', fontWeight: 700, margin: '0 0 8px 0', color: '#f8fafc' }}>
          9. User & Access Management (Admin Console)
        </h2>
        <p style={{ color: '#94a3b8', fontSize: '14px', margin: 0 }}>
          Manage user identities, enforce server-side role-based access controls (RBAC), and configure repository memberships.
        </p>
      </div>

      {userError && (
        <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '8px', padding: '12px 16px', color: '#f87171', marginBottom: '20px', fontSize: '13px' }}>
          ⚠️ {userError}
        </div>
      )}

      {userSuccess && (
        <div style={{ background: 'rgba(34, 197, 94, 0.1)', border: '1px solid rgba(34, 197, 94, 0.3)', borderRadius: '8px', padding: '12px 16px', color: '#4ade80', marginBottom: '20px', fontSize: '13px' }}>
          ✓ {userSuccess}
        </div>
      )}

      {/* Grid: Create User & Overview */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '20px', marginBottom: '24px' }}>
        {/* Create User Card */}
        <div style={{ background: '#1e293b', padding: '20px', borderRadius: '8px', border: '1px solid #334155' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 600, margin: '0 0 16px 0', color: '#f8fafc' }}>
            Provision New User Account
          </h3>
          <form onSubmit={handleCreateUser} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: '#94a3b8', marginBottom: '6px' }}>
                Username
              </label>
              <input
                type="text"
                value={newUsername}
                onChange={(e) => setNewUsername(e.target.value)}
                placeholder="e.g. jdoe_reviewer"
                required
                style={{ width: '100%', background: '#0f172a', border: '1px solid #334155', borderRadius: '6px', padding: '8px 12px', color: '#fff', fontSize: '13px', boxSizing: 'border-box' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: '#94a3b8', marginBottom: '6px' }}>
                Initial Password
              </label>
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="••••••••"
                required
                style={{ width: '100%', background: '#0f172a', border: '1px solid #334155', borderRadius: '6px', padding: '8px 12px', color: '#fff', fontSize: '13px', boxSizing: 'border-box' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: '#94a3b8', marginBottom: '6px' }}>
                System Role
              </label>
              <select
                value={newRole}
                onChange={(e) => setNewRole(e.target.value as any)}
                style={{ width: '100%', background: '#0f172a', border: '1px solid #334155', borderRadius: '6px', padding: '8px 12px', color: '#fff', fontSize: '13px', boxSizing: 'border-box' }}
              >
                <option value="reviewer">Reviewer (Access to assigned repositories)</option>
                <option value="viewer">Viewer (Read-only demo access)</option>
                <option value="admin">Administrator (Universal full access)</option>
              </select>
            </div>
            <button
              type="submit"
              disabled={isCreatingUser}
              style={{ marginTop: '8px', background: '#2563eb', color: '#fff', border: 'none', borderRadius: '6px', padding: '10px', fontSize: '13px', fontWeight: 600, cursor: isCreatingUser ? 'not-allowed' : 'pointer' }}
            >
              {isCreatingUser ? 'Creating Account...' : 'Create Account'}
            </button>
          </form>
        </div>

        {/* Roles & Permissions Reference */}
        <div style={{ background: '#1e293b', padding: '20px', borderRadius: '8px', border: '1px solid #334155' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 600, margin: '0 0 16px 0', color: '#f8fafc' }}>
            RBAC Permission Specifications
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px', fontSize: '12px' }}>
            <div style={{ background: '#0f172a', padding: '12px', borderRadius: '6px', border: '1px solid #334155' }}>
              <div style={{ fontWeight: 700, color: '#38bdf8', marginBottom: '6px' }}>ADMIN</div>
              <ul style={{ paddingLeft: '16px', margin: 0, color: '#94a3b8', lineHeight: '1.6' }}>
                <li>Universal repository access</li>
                <li>Create & delete repos</li>
                <li>Trigger ingestion pipelines</li>
                <li>Manage users & assign roles</li>
                <li>Manage repo memberships</li>
                <li>Manage reports & configs</li>
              </ul>
            </div>
            <div style={{ background: '#0f172a', padding: '12px', borderRadius: '6px', border: '1px solid #334155' }}>
              <div style={{ fontWeight: 700, color: '#a78bfa', marginBottom: '6px' }}>REVIEWER</div>
              <ul style={{ paddingLeft: '16px', margin: 0, color: '#94a3b8', lineHeight: '1.6' }}>
                <li>Assigned repositories only</li>
                <li>Browse Knowledge Graph</li>
                <li>Explore codebase files</li>
                <li>Use GraphRAG Assistant</li>
                <li>View Impact & Reports</li>
                <li>No repo creation/deletion</li>
                <li>No ingestion triggering</li>
              </ul>
            </div>
            <div style={{ background: '#0f172a', padding: '12px', borderRadius: '6px', border: '1px solid #334155' }}>
              <div style={{ fontWeight: 700, color: '#34d399', marginBottom: '6px' }}>VIEWER</div>
              <ul style={{ paddingLeft: '16px', margin: 0, color: '#94a3b8', lineHeight: '1.6' }}>
                <li>Assigned demo repos only</li>
                <li>Read-only graph & files</li>
                <li>View technical reports</li>
                <li>No state-mutating actions</li>
                <li>No shared resource modification</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* User Directory Table */}
      <div style={{ background: '#1e293b', padding: '20px', borderRadius: '8px', border: '1px solid #334155', marginBottom: '24px' }}>
        <h3 style={{ fontSize: '16px', fontWeight: 600, margin: '0 0 16px 0', color: '#f8fafc' }}>
          User Directory ({users.length} accounts)
        </h3>
        {isLoadingUsers ? (
          <div style={{ color: '#94a3b8', fontSize: '13px' }}>Loading user directory...</div>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px', textAlign: 'left' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid #334155', color: '#94a3b8' }}>
                <th style={{ padding: '10px 12px' }}>Username</th>
                <th style={{ padding: '10px 12px' }}>Role</th>
                <th style={{ padding: '10px 12px' }}>Status</th>
                <th style={{ padding: '10px 12px' }}>Created</th>
                <th style={{ padding: '10px 12px', textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => {
                const isSelf = currentUser?.userId === u.user_id;
                return (
                  <tr key={u.user_id} style={{ borderBottom: '1px solid #1e293b' }}>
                    <td style={{ padding: '10px 12px', fontWeight: 600, color: '#f8fafc' }}>
                      {u.username} {isSelf && <span style={{ color: '#38bdf8', fontSize: '11px' }}>(You)</span>}
                    </td>
                    <td style={{ padding: '10px 12px' }}>
                      <select
                        value={u.role}
                        onChange={(e) => handleRoleChange(u.user_id, e.target.value)}
                        disabled={isSelf}
                        style={{
                          background: '#0f172a',
                          color: u.role === 'admin' ? '#38bdf8' : u.role === 'reviewer' ? '#a78bfa' : '#34d399',
                          border: '1px solid #334155',
                          borderRadius: '4px',
                          padding: '4px 8px',
                          fontSize: '12px',
                          fontWeight: 600,
                        }}
                      >
                        <option value="admin">ADMIN</option>
                        <option value="reviewer">REVIEWER</option>
                        <option value="viewer">VIEWER</option>
                      </select>
                    </td>
                    <td style={{ padding: '10px 12px' }}>
                      <span
                        style={{
                          padding: '3px 8px',
                          borderRadius: '12px',
                          fontSize: '11px',
                          fontWeight: 700,
                          background: u.is_active ? 'rgba(34, 197, 94, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                          color: u.is_active ? '#4ade80' : '#f87171',
                          border: `1px solid ${u.is_active ? 'rgba(34, 197, 94, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
                        }}
                      >
                        {u.is_active ? 'ACTIVE' : 'DEACTIVATED'}
                      </span>
                    </td>
                    <td style={{ padding: '10px 12px', color: '#94a3b8', fontSize: '12px' }}>
                      {u.created_at ? u.created_at.substring(0, 10) : 'N/A'}
                    </td>
                    <td style={{ padding: '10px 12px', textAlign: 'right' }}>
                      <div style={{ display: 'inline-flex', gap: '8px' }}>
                        <button
                          onClick={() => {
                            setResetModalUserId(u.user_id);
                            setResetModalUsername(u.username);
                            setResetPasswordInput('');
                          }}
                          style={{
                            background: '#0f172a',
                            border: '1px solid #334155',
                            color: '#cbd5e1',
                            borderRadius: '4px',
                            padding: '4px 10px',
                            fontSize: '11px',
                            cursor: 'pointer',
                          }}
                        >
                          Reset Password
                        </button>
                        <button
                          onClick={() => handleToggleStatus(u)}
                          disabled={isSelf}
                          style={{
                            background: u.is_active ? 'rgba(239, 68, 68, 0.1)' : 'rgba(34, 197, 94, 0.1)',
                            border: `1px solid ${u.is_active ? '#ef4444' : '#22c55e'}`,
                            color: u.is_active ? '#f87171' : '#4ade80',
                            borderRadius: '4px',
                            padding: '4px 10px',
                            fontSize: '11px',
                            fontWeight: 600,
                            cursor: isSelf ? 'not-allowed' : 'pointer',
                          }}
                        >
                          {u.is_active ? 'Deactivate' : 'Activate'}
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>

      {/* Repository Membership Management */}
      <div style={{ background: '#1e293b', padding: '20px', borderRadius: '8px', border: '1px solid #334155' }}>
        <h3 style={{ fontSize: '16px', fontWeight: 600, margin: '0 0 8px 0', color: '#f8fafc' }}>
          Repository Memberships & Access Assignment
        </h3>
        <p style={{ color: '#94a3b8', fontSize: '13px', margin: '0 0 16px 0' }}>
          Assign reviewers or viewers to specific repositories. Users can only access repositories they are explicitly members of.
        </p>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
          <label style={{ fontSize: '13px', color: '#94a3b8' }}>Target Repository:</label>
          <select
            value={selectedRepoId}
            onChange={(e) => setSelectedRepoId(e.target.value)}
            style={{ background: '#0f172a', color: '#fff', border: '1px solid #334155', borderRadius: '4px', padding: '6px 12px', fontSize: '13px' }}
          >
            {repositories.map((r) => (
              <option key={r.repo_id} value={r.repo_id}>
                {r.name} ({r.repo_id.substring(0, 8)})
              </option>
            ))}
          </select>
        </div>

        {/* Current Members List */}
        <div style={{ marginBottom: '20px' }}>
          <h4 style={{ fontSize: '14px', color: '#cbd5e1', margin: '0 0 10px 0' }}>
            Current Repository Members
          </h4>
          {isLoadingMembers ? (
            <div style={{ color: '#94a3b8', fontSize: '13px' }}>Loading members...</div>
          ) : members.length === 0 ? (
            <div style={{ color: '#94a3b8', fontSize: '13px', fontStyle: 'italic' }}>No non-admin members currently assigned to this repository.</div>
          ) : (
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
              {members.map((m) => (
                <div
                  key={m.user_id}
                  style={{
                    background: '#0f172a',
                    border: '1px solid #334155',
                    borderRadius: '6px',
                    padding: '8px 12px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '10px',
                    fontSize: '12px',
                  }}
                >
                  <span style={{ fontWeight: 600, color: '#f8fafc' }}>{m.username}</span>
                  <span style={{ color: m.role === 'reviewer' ? '#a78bfa' : '#34d399', textTransform: 'uppercase', fontSize: '10px', fontWeight: 700 }}>
                    {m.role}
                  </span>
                  <button
                    onClick={() => handleRevokeMember(m.user_id)}
                    style={{
                      background: 'transparent',
                      border: 'none',
                      color: '#f87171',
                      cursor: 'pointer',
                      fontSize: '14px',
                      padding: 0,
                    }}
                    title="Revoke access"
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Grant Membership Form */}
        <form onSubmit={handleAssignMember} style={{ display: 'flex', gap: '12px', alignItems: 'center', flexWrap: 'wrap' }}>
          <select
            value={assignUserId}
            onChange={(e) => setAssignUserId(e.target.value)}
            style={{ background: '#0f172a', color: '#fff', border: '1px solid #334155', borderRadius: '4px', padding: '6px 12px', fontSize: '13px', minWidth: '180px' }}
          >
            <option value="">Select User...</option>
            {users
              .filter((u) => u.role !== 'admin')
              .map((u) => (
                <option key={u.user_id} value={u.user_id}>
                  {u.username} ({u.role.toUpperCase()})
                </option>
              ))}
          </select>
          <select
            value={assignRole}
            onChange={(e) => setAssignRole(e.target.value as any)}
            style={{ background: '#0f172a', color: '#fff', border: '1px solid #334155', borderRadius: '4px', padding: '6px 12px', fontSize: '13px' }}
          >
            <option value="reviewer">Reviewer</option>
            <option value="viewer">Viewer</option>
          </select>
          <button
            type="submit"
            disabled={!assignUserId || isAssigning}
            style={{
              background: '#2563eb',
              color: '#fff',
              border: 'none',
              borderRadius: '6px',
              padding: '7px 14px',
              fontSize: '13px',
              fontWeight: 600,
              cursor: !assignUserId || isAssigning ? 'not-allowed' : 'pointer',
            }}
          >
            {isAssigning ? 'Granting...' : 'Grant Repository Access'}
          </button>
        </form>
      </div>

      {/* Password Reset Modal */}
      {resetModalUserId && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0, 0, 0, 0.7)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
          }}
        >
          <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '24px', width: '100%', maxWidth: '400px' }}>
            <h4 style={{ margin: '0 0 12px 0', color: '#f8fafc', fontSize: '16px' }}>
              Reset Password for {resetModalUsername}
            </h4>
            <p style={{ color: '#94a3b8', fontSize: '13px', margin: '0 0 16px 0' }}>
              Setting a new password will immediately revoke all active sessions for this user.
            </p>
            <form onSubmit={handleResetPassword} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <input
                type="password"
                value={resetPasswordInput}
                onChange={(e) => setResetPasswordInput(e.target.value)}
                placeholder="Enter new password (min 6 chars)"
                required
                style={{ background: '#0f172a', border: '1px solid #334155', borderRadius: '6px', padding: '8px 12px', color: '#fff', fontSize: '13px' }}
              />
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
                <button
                  type="button"
                  onClick={() => setResetModalUserId(null)}
                  style={{ background: '#0f172a', border: '1px solid #334155', color: '#cbd5e1', borderRadius: '6px', padding: '8px 14px', fontSize: '13px', cursor: 'pointer' }}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isResetting || resetPasswordInput.length < 6}
                  style={{ background: '#2563eb', color: '#fff', border: 'none', borderRadius: '6px', padding: '8px 14px', fontSize: '13px', fontWeight: 600, cursor: isResetting ? 'not-allowed' : 'pointer' }}
                >
                  {isResetting ? 'Resetting...' : 'Confirm Reset'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
