import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { App } from './App';
import { SnapshotProvider } from './context/SnapshotContext';
import { AuthProvider } from './context/AuthContext';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <SnapshotProvider>
          <App />
        </SnapshotProvider>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
