import React, { createContext, useContext, useState, ReactNode } from 'react';
import snapshotData from '../data/graph_snapshot.json';

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

const defaultRepo: RepositoryItem = {
  repo_id: snapshotData.repository.repo_id,
  name: snapshotData.repository.name,
  git_url: snapshotData.repository.git_url,
  default_branch: 'main',
  status: 'ACTIVE',
};

const defaultSnapshot: SnapshotItem = {
  repo_id: snapshotData.repository.repo_id,
  commit_sha: snapshotData.snapshot.commit_sha,
};

const SnapshotContext = createContext<SnapshotContextType>({
  activeRepoId: defaultRepo.repo_id,
  activeCommitSha: defaultSnapshot.commit_sha,
  repositories: [defaultRepo],
  snapshots: [defaultSnapshot],
  isLoadingRepos: false,
  isLoadingSnapshots: false,
  error: null,
  setActiveSnapshot: () => {},
  selectRepo: async () => {},
  refreshRepositories: async () => {},
});

export const SnapshotProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [activeRepoId, setActiveRepoId] = useState<string>(defaultRepo.repo_id);
  const [activeCommitSha, setActiveCommitSha] = useState<string>(defaultSnapshot.commit_sha);

  const [repositories] = useState<RepositoryItem[]>([defaultRepo]);
  const [snapshots] = useState<SnapshotItem[]>([defaultSnapshot]);

  const setActiveSnapshot = (repoId: string, commitSha: string) => {
    setActiveRepoId(repoId);
    setActiveCommitSha(commitSha);
  };

  const selectRepo = async (repoId: string) => {
    setActiveRepoId(repoId);
  };

  const refreshRepositories = async () => {};

  return (
    <SnapshotContext.Provider
      value={{
        activeRepoId,
        activeCommitSha,
        repositories,
        snapshots,
        isLoadingRepos: false,
        isLoadingSnapshots: false,
        error: null,
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
