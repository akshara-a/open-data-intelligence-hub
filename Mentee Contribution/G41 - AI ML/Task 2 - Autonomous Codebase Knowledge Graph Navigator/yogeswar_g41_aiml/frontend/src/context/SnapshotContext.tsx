import React, { createContext, useContext, useState, useEffect, useRef, ReactNode, useCallback } from 'react';
import { useAuth } from './AuthContext';

export interface RepositoryItem {
  repo_id: string;
  name: string;
  git_url: string;
  default_branch?: string;
  status?: string;
  created_at?: string;
}

export interface SnapshotItem {
  repo_id: string;
  commit_sha: string;
  created_at?: string;
}

export interface SnapshotContextType {
  activeRepoId: string;
  activeCommitSha: string;
  repositories: RepositoryItem[];
  snapshots: SnapshotItem[];
  isLoadingRepos: boolean;
  isLoadingSnapshots: boolean;
  error: string | null;
  setActiveSnapshot: (repoId: string, commitSha: string) => void;
  selectRepo: (repoId: string) => Promise<void>;
  refreshRepositories: () => Promise<void>;
}

const defaultRepoId = 'repo_demo_sample';
const defaultCommitSha = 'c0ffee1234567890abcdef1234567890abcdef12';

const SnapshotContext = createContext<SnapshotContextType>({
  activeRepoId: defaultRepoId,
  activeCommitSha: defaultCommitSha,
  repositories: [],
  snapshots: [],
  isLoadingRepos: false,
  isLoadingSnapshots: false,
  error: null,
  setActiveSnapshot: () => {},
  selectRepo: async () => {},
  refreshRepositories: async () => {},
});

export const SnapshotProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { isAuthenticated, authFetch } = useAuth();

  const [activeRepoId, setActiveRepoId] = useState<string>(() => {
    return sessionStorage.getItem('activeRepoId') || localStorage.getItem('activeRepoId') || defaultRepoId;
  });
  const [activeCommitSha, setActiveCommitSha] = useState<string>(() => {
    return sessionStorage.getItem('activeCommitSha') || localStorage.getItem('activeCommitSha') || defaultCommitSha;
  });

  const [repositories, setRepositories] = useState<RepositoryItem[]>([]);
  const [snapshots, setSnapshots] = useState<SnapshotItem[]>([]);
  const [isLoadingRepos, setIsLoadingRepos] = useState<boolean>(false);
  const [isLoadingSnapshots, setIsLoadingSnapshots] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const snapshotReqIdRef = useRef<number>(0);

  const setActiveSnapshot = useCallback((repoId: string, commitSha: string) => {
    setActiveRepoId(repoId);
    setActiveCommitSha(commitSha);
    sessionStorage.setItem('activeRepoId', repoId);
    sessionStorage.setItem('activeCommitSha', commitSha);
    localStorage.setItem('activeRepoId', repoId);
    localStorage.setItem('activeCommitSha', commitSha);
  }, []);

  const fetchSnapshotsForRepo = useCallback(
    async (repoId: string): Promise<SnapshotItem[]> => {
      const currentReqId = ++snapshotReqIdRef.current;
      setIsLoadingSnapshots(true);
      try {
        const resp = await authFetch(`/api/v1/repos/${encodeURIComponent(repoId)}/snapshots`);
        if (resp.ok) {
          const data: SnapshotItem[] = await resp.json();
          if (currentReqId === snapshotReqIdRef.current) {
            setSnapshots(data);
            if (data.length > 0) {
              const latestCommit = data[0].commit_sha;
              setActiveSnapshot(repoId, latestCommit);
            }
            return data;
          }
        }
      } catch (err: any) {
        if (currentReqId === snapshotReqIdRef.current) {
          console.warn(`Failed to fetch snapshots for ${repoId}:`, err);
        }
      } finally {
        if (currentReqId === snapshotReqIdRef.current) {
          setIsLoadingSnapshots(false);
        }
      }
      return [];
    },
    [authFetch, setActiveSnapshot]
  );

  const refreshRepositories = useCallback(async () => {
    if (!isAuthenticated) return;
    setIsLoadingRepos(true);
    setError(null);
    try {
      const resp = await authFetch('/api/v1/repos');
      if (resp.ok) {
        const data: RepositoryItem[] = await resp.json();
        setRepositories(data);

        // Select initial repo if needed
        if (data.length > 0) {
          const currentValid = data.some((r) => r.repo_id === activeRepoId);
          const targetRepoId = currentValid ? activeRepoId : data[0].repo_id;
          if (!currentValid) {
            setActiveRepoId(targetRepoId);
          }
          await fetchSnapshotsForRepo(targetRepoId);
        }
      } else {
        setError(`Failed to fetch repositories (HTTP ${resp.status})`);
      }
    } catch (err: any) {
      setError(err?.message || 'Error communicating with repository API.');
    } finally {
      setIsLoadingRepos(false);
    }
  }, [isAuthenticated, authFetch, activeRepoId, fetchSnapshotsForRepo]);

  const selectRepo = useCallback(
    async (repoId: string) => {
      setActiveRepoId(repoId);
      sessionStorage.setItem('activeRepoId', repoId);
      localStorage.setItem('activeRepoId', repoId);
      await fetchSnapshotsForRepo(repoId);
    },
    [fetchSnapshotsForRepo]
  );

  useEffect(() => {
    if (isAuthenticated) {
      refreshRepositories();
    }
  }, [isAuthenticated, refreshRepositories]);

  return (
    <SnapshotContext.Provider
      value={{
        activeRepoId,
        activeCommitSha,
        repositories,
        snapshots,
        isLoadingRepos,
        isLoadingSnapshots,
        error,
        setActiveSnapshot,
        selectRepo,
        refreshRepositories,
      }}
    >
      {children}
    </SnapshotContext.Provider>
  );
};

export const useSnapshot = () => useContext(SnapshotContext);
