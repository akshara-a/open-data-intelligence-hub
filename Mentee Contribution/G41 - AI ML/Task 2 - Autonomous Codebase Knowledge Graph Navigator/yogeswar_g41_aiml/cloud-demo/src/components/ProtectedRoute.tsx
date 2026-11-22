import React from 'react';
import { Navigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactElement;
  allowedRoles?: string[];
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, allowedRoles }) => {
  const { user, isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return (
      <div
        style={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          background: '#090d16',
          color: '#94a3b8',
          fontFamily: 'system-ui, sans-serif',
        }}
      >
        <div
          style={{
            width: '40px',
            height: '40px',
            border: '3px solid #1e293b',
            borderTopColor: '#3b82f6',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            marginBottom: '16px',
          }}
        />
        <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
        <div style={{ fontSize: '14px', letterSpacing: '0.05em' }}>Verifying authenticated session...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Enforce role-based access control
  if (allowedRoles && allowedRoles.length > 0 && user) {
    const userRole = user.role.toLowerCase();
    const hasPermission = allowedRoles.some((r) => r.toLowerCase() === userRole);
    if (!hasPermission) {
      return (
        <div
          style={{
            padding: '48px 24px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '60vh',
            textAlign: 'center',
            fontFamily: 'system-ui, sans-serif',
          }}
        >
          <div
            style={{
              width: '64px',
              height: '64px',
              borderRadius: '50%',
              background: 'rgba(239, 68, 68, 0.1)',
              border: '2px solid #ef4444',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '32px',
              marginBottom: '20px',
            }}
          >
            🛡️
          </div>
          <h2 style={{ fontSize: '22px', color: '#f87171', margin: '0 0 12px 0' }}>
            Access Denied (403 Forbidden)
          </h2>
          <p style={{ color: '#94a3b8', maxWidth: '520px', lineHeight: '1.6', fontSize: '14px', margin: '0 0 24px 0' }}>
            Your active role <strong style={{ color: '#f1f5f9', textTransform: 'uppercase' }}>{user.role}</strong> does not have permission to access this administrative resource. Administrative privileges are required.
          </p>
          <div style={{ display: 'flex', gap: '12px' }}>
            <Link
              to="/"
              style={{
                background: '#2563eb',
                color: '#fff',
                textDecoration: 'none',
                padding: '10px 20px',
                borderRadius: '6px',
                fontSize: '13px',
                fontWeight: 600,
              }}
            >
              Return to Dashboard
            </Link>
          </div>
        </div>
      );
    }
  }

  return children;
};
