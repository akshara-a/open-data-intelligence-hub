import React, { createContext, useContext, useState, ReactNode } from 'react';

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

const defaultUser: UserProfile = {
  userId: 'usr_demo_admin',
  username: 'demo_user',
  role: 'admin',
};

const AuthContext = createContext<AuthContextType>({
  user: defaultUser,
  token: 'demo-static-token',
  isLoading: false,
  isAuthenticated: true,
  error: null,
  login: async () => true,
  logout: async () => {},
  refreshToken: async () => 'demo-static-token',
  authFetch: async (input: RequestInfo | URL, init?: RequestInit) => fetch(input, init),
});

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user] = useState<UserProfile | null>(defaultUser);

  const login = async () => true;
  const logout = async () => {};
  const refreshToken = async () => 'demo-static-token';

  const authFetch = async (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
    return fetch(input, init);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token: 'demo-static-token',
        isLoading: false,
        isAuthenticated: true,
        error: null,
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
