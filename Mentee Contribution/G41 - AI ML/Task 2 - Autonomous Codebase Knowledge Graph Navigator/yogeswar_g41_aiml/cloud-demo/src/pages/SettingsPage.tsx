import React, { useState } from 'react';
import { useSnapshot } from '../context/SnapshotContext';

export const SettingsPage: React.FC = () => {
  const { activeRepoId, activeCommitSha } = useSnapshot();
  const [notifications, setNotifications] = useState<boolean>(true);

  return (
    <div style={{ padding: '24px' }}>
      <h2>8. Settings</h2>
      <p style={{ color: '#94a3b8' }}>
        Manage connected repositories, view active authenticated identity and token lifetimes, and configure UI preferences.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '20px' }}>
        {/* RepoAccessManager Component */}
        <div style={{ background: '#1e293b', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
          <h3>Repository Access (RepoAccessManager)</h3>
          <p style={{ fontSize: '13px', color: '#94a3b8' }}>Connected bare mirrors and repository authorization</p>
          <div style={{ background: '#0f172a', padding: '12px', borderRadius: '6px', marginTop: '12px', fontSize: '13px' }}>
            <div><strong>Active Repository:</strong> <code>{activeRepoId}</code></div>
            <div><strong>Role:</strong> Owner (Authoritative check via <code>repo_memberships</code>)</div>
            <div><strong>Commit:</strong> <code>{activeCommitSha.substring(0, 10)}...</code></div>
          </div>
        </div>

        {/* TokenExpiryView Component */}
        <div style={{ background: '#1e293b', padding: '16px', borderRadius: '8px', border: '1px solid #334155' }}>
          <h3>Session & Token Expiry (TokenExpiryView)</h3>
          <p style={{ fontSize: '13px', color: '#94a3b8' }}>Active RS256 token lifetime and security parameters</p>
          <div style={{ background: '#0f172a', padding: '12px', borderRadius: '6px', marginTop: '12px', fontSize: '13px', lineHeight: '1.8' }}>
            <div><strong>Algorithm:</strong> RS256 (RSA-SHA256)</div>
            <div><strong>Access Token Expiry:</strong> 15 minutes (Memory-only)</div>
            <div><strong>Refresh Token Expiry:</strong> 7 days (HTTP-only Secure Cookie)</div>
            <div><strong>Reuse Detection:</strong> Active (Revokes entire token family)</div>
          </div>
        </div>
      </div>

      {/* NotificationPreferences Component */}
      <div style={{ background: '#1e293b', padding: '16px', borderRadius: '8px', marginTop: '20px', border: '1px solid #334155' }}>
        <h3>User Preferences (NotificationPreferences)</h3>
        <label style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '8px', cursor: 'pointer' }}>
          <input
            type="checkbox"
            checked={notifications}
            onChange={(e) => setNotifications(e.target.checked)}
          />
          <span>Notify when ingestion workers complete bare Git snapshot processing</span>
        </label>
      </div>
    </div>
  );
};
