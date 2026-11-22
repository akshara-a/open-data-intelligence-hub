import React, { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react';

export interface UserProfile {
  userId: string;
  username: string;
  role: string;
}

export interface AuthContextType {
  user: UserProfile | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  error: string | null;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<string | null>;
  authFetch: (input: RequestInfo | URL, init?: RequestInit) => Promise<Response>;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  isLoading: true,
  isAuthenticated: false,
  error: null,
  login: async () => false,
  logout: async () => {},
  refreshToken: async () => null,
  authFetch: async () => new Response(),
});

function parseJwt(token: string): any {
  try {
    const base64Url = token.split('.')[1];
    if (!base64Url) return null;
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      window
        .atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch {
    return null;
  }
}

function extractUserFromToken(token: string): UserProfile | null {
  const payload = parseJwt(token);
  if (!payload) return null;
  // Check expiry
  if (payload.exp && payload.exp * 1000 < Date.now()) {
    return null;
  }
  return {
    userId: payload.user_id || payload.sub || 'unknown',
    username: payload.username || payload.sub || 'user',
    role: payload.role || 'viewer',
  };
}

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const saveToken = useCallback((newToken: string | null) => {
    setToken(newToken);
    if (newToken) {
      sessionStorage.setItem('access_token', newToken);
      localStorage.setItem('access_token', newToken);
      const userProfile = extractUserFromToken(newToken);
      setUser(userProfile);
    } else {
      sessionStorage.removeItem('access_token');
      localStorage.removeItem('access_token');
      setUser(null);
    }
  }, []);

  const refreshToken = useCallback(async (): Promise<string | null> => {
    try {
      const resp = await fetch('/api/v1/auth/refresh', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
      });
      if (resp.ok) {
        const data = await resp.json();
        if (data.access_token) {
          saveToken(data.access_token);
          return data.access_token;
        }
      }
    } catch (err) {
      console.warn('Session refresh failed:', err);
    }
    saveToken(null);
    return null;
  }, [saveToken]);

  // Session restoration on mount
  useEffect(() => {
    let isMounted = true;

    async function restoreSession() {
      const stored = sessionStorage.getItem('access_token') || localStorage.getItem('access_token');
      if (stored) {
        const parsed = extractUserFromToken(stored);
        if (parsed) {
          if (isMounted) {
            setToken(stored);
            setUser(parsed);
            setIsLoading(false);
          }
          return;
        }
      }

      // Try refresh cookie if no valid token
      const newToken = await refreshToken();
      if (isMounted) {
        if (!newToken) {
          saveToken(null);
        }
        setIsLoading(false);
      }
    }

    restoreSession();

    return () => {
      isMounted = false;
    };
  }, [refreshToken, saveToken]);

  const login = async (username: string, password: string): Promise<boolean> => {
    setError(null);
    try {
      const resp = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
        credentials: 'include',
      });

      if (!resp.ok) {
        const errData = await resp.json().catch(() => ({}));
        setError(errData.detail || 'Authentication failed. Please check your credentials.');
        return false;
      }

      const data = await resp.json();
      if (data.access_token) {
        saveToken(data.access_token);
        return true;
      }
      setError('Invalid response from authentication server.');
      return false;
    } catch (err: any) {
      setError(err?.message || 'Network error occurred during login.');
      return false;
    }
  };

  const logout = async (): Promise<void> => {
    try {
      await fetch('/api/v1/auth/logout', {
        method: 'POST',
        credentials: 'include',
      });
    } catch (err) {
      console.warn('Logout network error:', err);
    } finally {
      saveToken(null);
    }
  };

  const authFetch = useCallback(
    async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
      let currentToken = token || sessionStorage.getItem('access_token') || localStorage.getItem('access_token');

      const headers = new Headers(init?.headers || {});
      if (currentToken) {
        headers.set('Authorization', `Bearer ${currentToken}`);
      }

      const config: RequestInit = {
        ...init,
        headers,
        credentials: 'include',
      };

      let resp = await fetch(input, config);

      // Handle 401: attempt token refresh once
      if (resp.status === 401) {
        const refreshed = await refreshToken();
        if (refreshed) {
          headers.set('Authorization', `Bearer ${refreshed}`);
          resp = await fetch(input, { ...config, headers });
        } else {
          // Token expired and refresh failed
          saveToken(null);
        }
      }

      return resp;
    },
    [token, refreshToken, saveToken]
  );

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        isAuthenticated: !!token && !!user,
        error,
        login,
        logout,
        refreshToken,
        authFetch,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
