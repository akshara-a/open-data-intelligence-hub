import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useSnapshot } from '../context/SnapshotContext';

interface Finding {
  statement: string;
  finding_type: 'verified_static' | 'potential_uncertain';
  evidence_ids: string[];
  file_path?: string;
  line_range?: string;
  confidence: number;
}

interface EvidenceRecord {
  evidence_id: string;
  file_path?: string;
  line_range?: string;
  description?: string;
  extraction_rule?: string;
}

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  verifiedFindings?: Finding[];
  uncertainFindings?: Finding[];
  recommendations?: string[];
  evidenceIds?: string[];
  insufficientEvidence?: boolean;
  toolTrace?: Array<{ tool: string; status: string; count?: number; error?: string }>;
}

export const AssistantPage: React.FC = () => {
  const params = useParams<{ repoId: string; commitSha: string }>();
  const { activeRepoId, activeCommitSha } = useSnapshot();

  const repoId = params.repoId || activeRepoId;
  const commitSha = params.commitSha || activeCommitSha;

  const [prompt, setPrompt] = useState<string>('');
  const [threadId, setThreadId] = useState<string | null>(null);
  const [evidenceOpen, setEvidenceOpen] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(false);
  const [workflowStage, setWorkflowStage] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [evidenceStore, setEvidenceStore] = useState<Record<string, EvidenceRecord>>({});
  const [selectedEvidenceId, setSelectedEvidenceId] = useState<string | null>(null);

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 'init-msg',
      role: 'assistant',
      content:
        'Hello! I am your Autonomous Codebase Assistant. Ask me architectural, dependency, API, or code explanation questions regarding the active snapshot context.',
      timestamp: new Date().toLocaleTimeString(),
    },
  ]);

  // Load thread history if threadId exists
  useEffect(() => {
    if (!threadId) return;
    const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
    fetch(`/api/v1/repos/${repoId}/snapshots/${commitSha}/assistant/threads/${threadId}`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    })
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data && data.messages) {
          const loaded: ChatMessage[] = data.messages.map((m: any, idx: number) => ({
            id: m.message_id || `hist-${idx}`,
            role: m.role,
            content: m.content,
            timestamp: m.created_at ? new Date(m.created_at).toLocaleTimeString() : '',
            verifiedFindings: m.findings?.verified,
            uncertainFindings: m.findings?.uncertain,
            evidenceIds: m.evidence?.map((e: any) => e.evidence_id),
            toolTrace: m.tool_trace,
          }));
          setMessages(loaded);
        }
      })
      .catch(() => {});
  }, [threadId, repoId, commitSha]);

  const handleSend = async () => {
    if (!prompt.trim() || loading) return;

    const userQuestion = prompt.trim();
    setPrompt('');
    setError(null);
    setLoading(true);
    setWorkflowStage('Validating request & intent understanding...');

    const userMessage: ChatMessage = {
      id: `usr-${Date.now()}`,
      role: 'user',
      content: userQuestion,
      timestamp: new Date().toLocaleTimeString(),
    };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      setWorkflowStage('Executing GraphRAG retrieval & Controlled Graph Gateway...');

      const resp = await fetch(`/api/v1/repos/${repoId}/snapshots/${commitSha}/assistant/chat`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          question: userQuestion,
          thread_id: threadId || undefined,
        }),
      });

      if (!resp.ok) {
        const errData = await resp.json().catch(() => ({ detail: `HTTP ${resp.status}` }));
        throw new Error(errData.detail || `Server returned HTTP ${resp.status}`);
      }

      const data = await resp.json();
      setThreadId(data.thread_id);

      // Collect returned evidence
      if (data.evidence && Array.isArray(data.evidence)) {
        setEvidenceStore((prev) => {
          const updated = { ...prev };
          data.evidence.forEach((ev: EvidenceRecord) => {
            if (ev.evidence_id) updated[ev.evidence_id] = ev;
          });
          return updated;
        });
      }

      const answer = data.answer || {};
      const assistantMessage: ChatMessage = {
        id: `asst-${Date.now()}`,
        role: 'assistant',
        content: answer.markdown_response || answer.summary || 'Investigation completed.',
        timestamp: new Date().toLocaleTimeString(),
        verifiedFindings: answer.verified_findings,
        uncertainFindings: answer.uncertain_findings,
        recommendations: answer.recommendations,
        evidenceIds: answer.evidence_references,
        insufficientEvidence: answer.insufficient_evidence,
        toolTrace: data.tool_trace,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      setError(err.message || 'Failed to communicate with assistant service.');
      setMessages((prev) => [
        ...prev,
        {
          id: `err-${Date.now()}`,
          role: 'assistant',
          content: `**Error**: ${err.message || 'Failed to complete investigation.'}`,
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
    } finally {
      setLoading(false);
      setWorkflowStage('');
    }
  };

  const handleNewConversation = () => {
    setThreadId(null);
    setMessages([
      {
        id: 'new-init',
        role: 'assistant',
        content: 'New investigation started. Ask a question regarding the active snapshot context.',
        timestamp: new Date().toLocaleTimeString(),
      },
    ]);
  };

  return (
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <div>
          <h2 style={{ margin: 0 }}>4. AI Assistant</h2>
          <p style={{ color: '#94a3b8', margin: '4px 0 0 0', fontSize: '13px' }}>
            Evidence-grounded codebase investigation powered by LangGraph, GraphRAG, and Controlled Graph Gateway.
          </p>
        </div>
        <button
          onClick={handleNewConversation}
          style={{
            background: '#334155',
            color: '#fff',
            border: 'none',
            padding: '8px 16px',
            borderRadius: '6px',
            cursor: 'pointer',
            fontSize: '13px',
          }}
        >
          + New Conversation
        </button>
      </div>

      {/* Snapshot Context Banner */}
      <div
        style={{
          background: '#1e293b',
          padding: '10px 16px',
          borderRadius: '6px',
          marginBottom: '20px',
          display: 'flex',
          gap: '24px',
          fontSize: '13px',
          border: '1px solid #334155',
        }}
      >
        <div>
          <strong>Repository:</strong> <code style={{ color: '#38bdf8' }}>{repoId}</code>
        </div>
        <div>
          <strong>Commit SHA:</strong>{' '}
          <code style={{ color: '#38bdf8' }}>{commitSha.substring(0, 10)}...</code>
        </div>
        {threadId && (
          <div>
            <strong>Thread:</strong> <code style={{ color: '#a78bfa' }}>{threadId}</code>
          </div>
        )}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: evidenceOpen ? '2.5fr 1fr' : '1fr', gap: '20px' }}>
        {/* Main Chat Panel */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            height: '620px',
            background: '#1e293b',
            borderRadius: '8px',
            padding: '16px',
            border: '1px solid #334155',
          }}
        >
          {/* ChatTranscript Component */}
          <div style={{ flex: 1, overflowY: 'auto', marginBottom: '16px', paddingRight: '8px' }}>
            <h3 style={{ fontSize: '14px', margin: '0 0 12px 0', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Chat Transcript (ChatTranscript)
            </h3>

            {messages.map((m) => (
              <div
                key={m.id}
                style={{
                  margin: '12px 0',
                  padding: '14px',
                  borderRadius: '6px',
                  background: m.role === 'user' ? '#1e3a8a' : '#0f172a',
                  border: m.role === 'user' ? '1px solid #2563eb' : '1px solid #1e293b',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                  <strong style={{ color: m.role === 'user' ? '#93c5fd' : '#38bdf8', fontSize: '13px' }}>
                    {m.role === 'user' ? 'You' : 'Autonomous Assistant'}:
                  </strong>
                  <span style={{ fontSize: '11px', color: '#64748b' }}>{m.timestamp}</span>
                </div>

                {/* Render Markdown Response */}
                <div
                  style={{
                    lineHeight: '1.6',
                    fontSize: '13px',
                    color: '#e2e8f0',
                    whiteSpace: 'pre-wrap',
                    fontFamily: 'system-ui, -apple-system, sans-serif',
                  }}
                >
                  {m.content}
                </div>

                {/* Verified Findings Badges */}
                {m.verifiedFindings && m.verifiedFindings.length > 0 && (
                  <div style={{ marginTop: '12px', borderTop: '1px solid #1e293b', paddingTop: '8px' }}>
                    <div style={{ fontSize: '11px', color: '#4ade80', fontWeight: 600, marginBottom: '4px' }}>
                      VERIFIED STATIC FINDINGS:
                    </div>
                    {m.verifiedFindings.map((vf, idx) => (
                      <div
                        key={idx}
                        style={{
                          fontSize: '12px',
                          color: '#cbd5e1',
                          background: '#064e3b',
                          padding: '4px 8px',
                          borderRadius: '4px',
                          margin: '4px 0',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '8px',
                        }}
                      >
                        <span style={{ color: '#34d399', fontWeight: 'bold' }}>✓</span>
                        <span>{vf.statement}</span>
                        {vf.file_path && (
                          <code style={{ background: '#022c22', padding: '2px 4px', borderRadius: '3px', color: '#a7f3d0' }}>
                            {vf.file_path}:{vf.line_range}
                          </code>
                        )}
                        {vf.evidence_ids &&
                          vf.evidence_ids.map((eid) => (
                            <button
                              key={eid}
                              onClick={() => setSelectedEvidenceId(eid)}
                              style={{
                                background: '#1e3a8a',
                                color: '#93c5fd',
                                border: 'none',
                                borderRadius: '3px',
                                padding: '2px 6px',
                                fontSize: '11px',
                                cursor: 'pointer',
                              }}
                            >
                              [{eid}]
                            </button>
                          ))}
                      </div>
                    ))}
                  </div>
                )}

                {/* Uncertain Findings Badges */}
                {m.uncertainFindings && m.uncertainFindings.length > 0 && (
                  <div style={{ marginTop: '8px' }}>
                    <div style={{ fontSize: '11px', color: '#fbbf24', fontWeight: 600, marginBottom: '4px' }}>
                      POTENTIAL / UNCERTAIN COUPLINGS (DYNAMIC):
                    </div>
                    {m.uncertainFindings.map((uf, idx) => (
                      <div
                        key={idx}
                        style={{
                          fontSize: '12px',
                          color: '#fef3c7',
                          background: '#78350f',
                          padding: '4px 8px',
                          borderRadius: '4px',
                          margin: '4px 0',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '8px',
                        }}
                      >
                        <span style={{ color: '#f59e0b', fontWeight: 'bold' }}>⚠</span>
                        <span>{uf.statement}</span>
                        {uf.file_path && (
                          <code style={{ background: '#451a03', padding: '2px 4px', borderRadius: '3px', color: '#fde68a' }}>
                            {uf.file_path}:{uf.line_range}
                          </code>
                        )}
                      </div>
                    ))}
                  </div>
                )}

                {/* Tool trace pills */}
                {m.toolTrace && m.toolTrace.length > 0 && (
                  <div style={{ marginTop: '8px', display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                    <span style={{ fontSize: '10px', color: '#64748b' }}>Tools invoked:</span>
                    {m.toolTrace.map((tt, idx) => (
                      <span
                        key={idx}
                        style={{
                          fontSize: '10px',
                          background: '#1e293b',
                          color: '#94a3b8',
                          padding: '2px 6px',
                          borderRadius: '4px',
                        }}
                      >
                        {tt.tool} ({tt.status})
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div
                style={{
                  margin: '12px 0',
                  padding: '12px',
                  borderRadius: '6px',
                  background: '#0f172a',
                  border: '1px solid #3b82f6',
                  color: '#93c5fd',
                  fontSize: '13px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                }}
              >
                <div
                  style={{
                    width: '14px',
                    height: '14px',
                    border: '2px solid #3b82f6',
                    borderTopColor: 'transparent',
                    borderRadius: '50%',
                    animation: 'spin 1s linear infinite',
                  }}
                />
                <span>{workflowStage || 'Executing LangGraph supervisor workflow...'}</span>
              </div>
            )}
          </div>

          {error && (
            <div
              style={{
                background: '#7f1d1d',
                color: '#fecaca',
                padding: '8px 12px',
                borderRadius: '4px',
                fontSize: '12px',
                marginBottom: '8px',
              }}
            >
              <strong>Error:</strong> {error}
            </div>
          )}

          {/* PromptInputBox Component */}
          <div style={{ display: 'flex', gap: '8px' }}>
            <input
              type="text"
              placeholder="Ask an architectural, dependency, or code question..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              disabled={loading}
              style={{
                flex: 1,
                padding: '12px',
                borderRadius: '4px',
                background: '#0f172a',
                color: '#fff',
                border: '1px solid #334155',
                fontSize: '13px',
              }}
            />
            <button
              onClick={handleSend}
              disabled={loading || !prompt.trim()}
              style={{
                background: loading ? '#475569' : '#2563eb',
                color: '#fff',
                border: 'none',
                padding: '12px 24px',
                borderRadius: '4px',
                cursor: loading ? 'default' : 'pointer',
                fontWeight: 600,
                fontSize: '13px',
              }}
            >
              {loading ? 'Analyzing...' : 'Send'}
            </button>
            <button
              onClick={() => setEvidenceOpen(!evidenceOpen)}
              style={{
                background: '#334155',
                color: '#fff',
                border: 'none',
                padding: '12px 16px',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '13px',
              }}
            >
              {evidenceOpen ? 'Hide Evidence' : 'Show Evidence'}
            </button>
          </div>
        </div>

        {/* CollapsibleEvidenceDrawer Component */}
        {evidenceOpen && (
          <div
            style={{
              background: '#1e293b',
              borderRadius: '8px',
              padding: '16px',
              border: '1px solid #334155',
              height: '620px',
              overflowY: 'auto',
            }}
          >
            <h3 style={{ fontSize: '14px', margin: '0 0 4px 0', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Evidence Drawer (CollapsibleEvidenceDrawer)
            </h3>
            <p style={{ fontSize: '12px', color: '#64748b', margin: '0 0 16px 0' }}>
              Verified Grounding Evidence Citations ({Object.keys(evidenceStore).length} collected)
            </p>

            {Object.keys(evidenceStore).length === 0 ? (
              <div style={{ color: '#64748b', fontSize: '13px', textAlign: 'center', marginTop: '40px' }}>
                No citations retrieved yet. Ask a question to inspect grounding evidence.
              </div>
            ) : (
              Object.values(evidenceStore).map((ev) => {
                const isSelected = selectedEvidenceId === ev.evidence_id;
                return (
                  <div
                    key={ev.evidence_id}
                    style={{
                      background: isSelected ? '#1e3a8a' : '#0f172a',
                      padding: '12px',
                      borderRadius: '6px',
                      marginBottom: '10px',
                      fontSize: '12px',
                      border: isSelected ? '1px solid #38bdf8' : '1px solid #1e293b',
                    }}
                  >
                    <div>
                      <strong>Citation:</strong> <code style={{ color: '#38bdf8' }}>[{ev.evidence_id}]</code>
                    </div>
                    {ev.file_path && (
                      <div style={{ marginTop: '4px' }}>
                        <strong>File:</strong> <code>{ev.file_path}</code>
                      </div>
                    )}
                    {ev.line_range && (
                      <div style={{ marginTop: '4px' }}>
                        <strong>Lines:</strong> <code>{ev.line_range}</code>
                      </div>
                    )}
                    {ev.description && (
                      <div style={{ marginTop: '4px', color: '#94a3b8' }}>
                        <strong>Rule:</strong> {ev.description}
                      </div>
                    )}
                    <div style={{ marginTop: '4px', fontSize: '11px', color: '#64748b' }}>
                      <strong>Commit:</strong> <code>{commitSha.substring(0, 8)}</code>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        )}
      </div>
    </div>
  );
};
