import { useEffect, useRef, useState } from 'react'
import { api } from './api.js'

const NAV_ITEMS = [
  ['dashboard', 'Dashboard', '▦'],
  ['chat', 'AI Chat', '✦'],
  ['graph', 'Architecture Graph', '⌘'],
  ['blast', 'Blast Radius', '◎'],
  ['cycles', 'Circular Dependencies', '↻'],
  ['reports', 'Reports', '▤'],
]

const EXAMPLES = [
  'What is the blast radius of legacy-auth-module?',
  'Which circular dependencies exist?',
  'Which services depend on order-service?',
  'What happens if legacy-auth-module is deprecated?',
  'How can I reduce architectural coupling?',
]

function IconButton({ children, active, onClick, label }) {
  return (
    <button className={`nav-item ${active ? 'active' : ''}`} onClick={onClick} title={label}>
      <span className="nav-icon" aria-hidden="true">{children}</span>
      <span>{label}</span>
    </button>
  )
}

function StatusBadge({ healthy }) {
  return (
    <span className={`status-badge ${healthy ? 'healthy' : 'offline'}`}>
      <span className="status-dot" />
      {healthy ? 'Backend connected' : 'Backend unavailable'}
    </span>
  )
}

function MetricCard({ label, value, accent, detail }) {
  return (
    <article className="metric-card">
      <div className={`metric-accent ${accent}`} />
      <div>
        <span className="metric-label">{label}</span>
        <strong>{value ?? '—'}</strong>
        {detail && <small>{detail}</small>}
      </div>
    </article>
  )
}

function Panel({ title, subtitle, children, action }) {
  return (
    <section className="panel">
      {(title || action) && (
        <header className="panel-header">
          <div>
            {title && <h2>{title}</h2>}
            {subtitle && <p>{subtitle}</p>}
          </div>
          {action}
        </header>
      )}
      {children}
    </section>
  )
}

function ErrorState({ message, onRetry }) {
  return (
    <div className="error-state" role="alert">
      <span>!</span>
      <div>
        <strong>Could not retrieve backend data</strong>
        <p>{message}</p>
      </div>
      {onRetry && <button className="secondary-button" onClick={onRetry}>Retry</button>}
    </div>
  )
}

function Dashboard({ health, schema, cycles, loading, error, onRetry }) {
  const categories = schema?.node_type_counts || {}
  const cycleCount = cycles?.total_cycles ?? 0

  return (
    <div className="view-stack">
      <div className="page-heading">
        <div>
          <span className="eyebrow">Overview</span>
          <h1>Architecture Dashboard</h1>
        </div>
        <StatusBadge healthy={!error && health?.status === 'healthy'} />
      </div>

      {error && <ErrorState message={error} onRetry={onRetry} />}

      <div className="metrics-grid">
        <MetricCard label="Graph nodes" value={loading ? '—' : schema?.total_nodes} accent="blue" detail="Mock architecture components" />
        <MetricCard label="Relationships" value={loading ? '—' : schema?.total_edges} accent="purple" detail="Dependency connections" />
        <MetricCard label="Node categories" value={loading ? '—' : Object.keys(categories).length} accent="cyan" detail="Component classifications" />
        <MetricCard label="Circular dependencies" value={loading ? '—' : cycleCount} accent="amber" detail={cycleCount ? 'Architectural debt detected' : 'No cycles detected'} />
      </div>

      <div className="dashboard-grid">
        <Panel title="Graph composition" subtitle="Live distribution from the mock graph schema">
          <div className="category-list">
            {Object.entries(categories).map(([category, count]) => (
              <div className="category-row" key={category}>
                <span>{category}</span>
                <div className="category-track">
                  <div style={{ width: `${Math.max(12, (count / (schema?.total_nodes || 1)) * 100)}%` }} />
                </div>
                <strong>{count}</strong>
              </div>
            ))}
          </div>
        </Panel>

        <Panel title="Runtime context" subtitle="Current demo environment">
          <div className="context-card">
            <span className="context-icon">N</span>
            <div>
              <strong>NetworkX mock graph</strong>
              <p>{health?.dataset_source || 'data/mock_graph_seed.json'}</p>
            </div>
          </div>
          <div className="context-card">
            <span className="context-icon purple">C</span>
            <div>
              <strong>Generated Cypher</strong>
              <p>Templates are generated but not executed against Neo4j.</p>
            </div>
          </div>
          <div className="context-card">
            <span className="context-icon green">API</span>
            <div>
              <strong>FastAPI backend</strong>
              <p>http://127.0.0.1:8000 · {health?.engine || 'Status unavailable'}</p>
            </div>
          </div>
        </Panel>
      </div>
    </div>
  )
}

function renderInlineMarkdown(text) {
  const parts = text.split(/(\*\*[^*]+\*\*|`[^`]+`)/g)
  return parts.map((part, index) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={`strong-${index}`}>{part.slice(2, -2)}</strong>
    }
    if (part.startsWith('`') && part.endsWith('`')) {
      return <code key={`code-${index}`}>{part.slice(1, -1)}</code>
    }
    return <span key={`text-${index}`}>{part}</span>
  })
}

function MarkdownReport({ text }) {
  const lines = String(text || '').replace(/\r\n/g, '\n').split('\n')
  const blocks = []
  let index = 0

  while (index < lines.length) {
    const line = lines[index]

    if (!line.trim()) {
      index += 1
      continue
    }

    if (line.startsWith('```')) {
      const language = line.slice(3).trim()
      const codeLines = []
      index += 1
      while (index < lines.length && !lines[index].startsWith('```')) {
        codeLines.push(lines[index])
        index += 1
      }
      if (index < lines.length) index += 1
      blocks.push(
        <pre className="report-code-block" key={`code-${index}`}>
          {language && <span className="code-language">{language}</span>}
          <code>{codeLines.join('\n')}</code>
        </pre>,
      )
      continue
    }

    const heading = line.match(/^(#{1,6})\s+(.+)$/)
    if (heading) {
      const level = heading[1].length
      const HeadingTag = `h${Math.min(level, 4)}`
      blocks.push(<HeadingTag key={`heading-${index}`}>{renderInlineMarkdown(heading[2])}</HeadingTag>)
      index += 1
      continue
    }

    if (/^[-*_]{3,}$/.test(line.trim())) {
      blocks.push(<hr key={`hr-${index}`} />)
      index += 1
      continue
    }

    if (
      line.includes('|') &&
      index + 1 < lines.length &&
      /^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$/.test(lines[index + 1])
    ) {
      const parseRow = (row) => {
        const cells = row.split('|').map((cell) => cell.trim())
        if (row.trim().startsWith('|')) cells.shift()
        if (row.trim().endsWith('|')) cells.pop()
        return cells
      }
      const headers = parseRow(line)
      index += 2
      const rows = []
      while (index < lines.length && lines[index].includes('|') && lines[index].trim()) {
        rows.push(parseRow(lines[index]))
        index += 1
      }
      blocks.push(
        <div className="report-table-wrap" key={`table-${index}`}>
          <table>
            <thead><tr>{headers.map((header, headerIndex) => <th key={headerIndex}>{renderInlineMarkdown(header)}</th>)}</tr></thead>
            <tbody>{rows.map((row, rowIndex) => (
              <tr key={rowIndex}>{headers.map((_, columnIndex) => <td key={columnIndex}>{renderInlineMarkdown(row[columnIndex] || '')}</td>)}</tr>
            ))}</tbody>
          </table>
        </div>,
      )
      continue
    }

    if (line.startsWith('>')) {
      const quoteLines = []
      while (index < lines.length && lines[index].startsWith('>')) {
        quoteLines.push(lines[index].replace(/^>\s?/, ''))
        index += 1
      }
      blocks.push(<blockquote key={`quote-${index}`}>{renderInlineMarkdown(quoteLines.join(' '))}</blockquote>)
      continue
    }

    if (/^[-*+]\s+/.test(line)) {
      const items = []
      while (index < lines.length && /^[-*+]\s+/.test(lines[index])) {
        items.push(lines[index].replace(/^[-*+]\s+/, ''))
        index += 1
      }
      blocks.push(<ul key={`ul-${index}`}>{items.map((item, itemIndex) => <li key={itemIndex}>{renderInlineMarkdown(item)}</li>)}</ul>)
      continue
    }

    if (/^\d+[.)]\s+/.test(line)) {
      const items = []
      while (index < lines.length && /^\d+[.)]\s+/.test(lines[index])) {
        items.push(lines[index].replace(/^\d+[.)]\s+/, ''))
        index += 1
      }
      blocks.push(<ol key={`ol-${index}`}>{items.map((item, itemIndex) => <li key={itemIndex}>{renderInlineMarkdown(item)}</li>)}</ol>)
      continue
    }

    const paragraphLines = []
    while (
      index < lines.length &&
      lines[index].trim() &&
      !/^#{1,6}\s/.test(lines[index]) &&
      !/^[-*+]\s+/.test(lines[index]) &&
      !/^\d+[.)]\s+/.test(lines[index]) &&
      !lines[index].startsWith('```') &&
      !lines[index].startsWith('>')
    ) {
      paragraphLines.push(lines[index].trim())
      index += 1
    }
    blocks.push(<p key={`paragraph-${index}`}>{renderInlineMarkdown(paragraphLines.join(' '))}</p>)
  }

  return <div className="markdown-report">{blocks}</div>
}

function ChatView({ onReport }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', text: 'Ask a question about dependencies, blast radius, cycles, or architectural coupling. I will use the Task 2 graph analysis backend.' },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [latestAssistantId, setLatestAssistantId] = useState(null)
  const latestAssistantRef = useRef(null)
  const responseIdRef = useRef(0)

  useEffect(() => {
    if (latestAssistantId !== null) {
      latestAssistantRef.current?.scrollIntoView({ behavior: 'auto', block: 'start' })
    }
  }, [messages, latestAssistantId])

  async function sendMessage(text) {
    const question = (text ?? input).trim()
    if (!question || loading) return
    setMessages((current) => [...current, { role: 'user', text: question }])
    setInput('')
    setLoading(true)
    setError('')
    setLatestAssistantId(null)
    try {
      const result = await api.navigate(question)
      responseIdRef.current += 1
      const assistantId = responseIdRef.current
      setMessages((current) => [...current, { role: 'assistant', id: assistantId, text: result.report_markdown, result }])
      setLatestAssistantId(assistantId)
      onReport?.(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function handleComposerKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="view-stack chat-layout">
      <div className="page-heading"><div><span className="eyebrow">Graph reasoning</span><h1>AI Architecture Chat</h1></div></div>
      <div className="chat-shell">
        <div className="messages">
          {messages.map((message, index) => (
            <div className={`message-row ${message.role}`} key={`${message.role}-${index}`}>
              {message.role === 'assistant' && <div className="avatar assistant-avatar">AI</div>}
              <div
                className="message-bubble"
                ref={message.id === latestAssistantId ? latestAssistantRef : null}
              >
                <div className="message-label">{message.role === 'assistant' ? 'Architecture Assistant' : 'You'}</div>
                {message.role === 'assistant'
                  ? <MarkdownReport text={message.text} />
                  : <div className="user-message-copy">{message.text}</div>}
                {message.result?.reasoning_result && (
                  <AnalysisDetails result={message.result.reasoning_result} />
                )}
              </div>
            </div>
          ))}
          {loading && (
            <div className="message-row assistant">
              <div className="avatar assistant-avatar">AI</div>
              <div className="message-bubble loading-bubble"><span /><span /><span /></div>
            </div>
          )}
          {error && <ErrorState message={error} />}
        </div>
        <div className="chat-composer">
          <div className="example-list">
            {EXAMPLES.map((example) => <button key={example} onClick={() => sendMessage(example)} disabled={loading}>{example}</button>)}
          </div>
          <form onSubmit={(event) => { event.preventDefault(); sendMessage() }}>
            <textarea
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={handleComposerKeyDown}
              placeholder="Ask about your architecture..."
              aria-label="Architecture question"
              rows={2}
            />
            <button className="send-button" type="submit" disabled={loading || !input.trim()} aria-label="Send message">
              <span>Send</span>
              <span aria-hidden="true">➤</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

function AnalysisDetails({ result }) {
  const affected = result.affected_nodes || {}
  const risks = result.risks || []
  const recommendations = result.recommendations || []
  return (
    <div className="analysis-details">
      {affected.total_affected_count !== undefined && (
        <div className="mini-stat"><span>Affected components</span><strong>{affected.total_affected_count}</strong></div>
      )}
      {!!result.coupling_metrics && (
        <div className="mini-stat"><span>Coupling</span><strong>Ca {result.coupling_metrics.afferent_coupling} · Ce {result.coupling_metrics.efferent_coupling}</strong></div>
      )}
      {risks.length > 0 && (
        <div className="detail-section">
          <h4>Risks</h4>
          {risks.map((risk, index) => (
            <div className="risk-row" key={`${risk.risk_title}-${index}`}>
              <span className={`severity ${risk.severity?.toLowerCase()}`}>{risk.severity}</span>
              <div><strong>{risk.risk_title}</strong><p>{risk.explanation}</p></div>
            </div>
          ))}
        </div>
      )}
      {recommendations.length > 0 && (
        <div className="detail-section">
          <h4>Recommendations</h4>
          <ol>{recommendations.map((item, index) => <li key={index}><strong>{item.title}</strong><span>{item.intended_architectural_benefit}</span></li>)}</ol>
        </div>
      )}
    </div>
  )
}

function GraphView({ nodes, schema, openNodeId }) {
  const [category, setCategory] = useState('All')
  const [selectedNodeId, setSelectedNodeId] = useState(null)
  const [selectedDetails, setSelectedDetails] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [detailError, setDetailError] = useState('')
  const categories = ['All', ...Object.keys(schema?.node_type_counts || {})]
  const filtered = nodes.filter((node) => category === 'All' || node.type === category)
  const selectedNode = nodes.find((node) => node.id === selectedNodeId)
  const details = selectedDetails?.id === selectedNodeId ? selectedDetails : selectedNode

  useEffect(() => {
    if (openNodeId) setSelectedNodeId(openNodeId)
  }, [openNodeId])

  useEffect(() => {
    if (!selectedNodeId) return undefined

    let active = true
    setDetailLoading(true)
    setDetailError('')
    api.node(selectedNodeId)
      .then((result) => {
        if (active) setSelectedDetails(result)
      })
      .catch((err) => {
        if (active) setDetailError(err.message)
      })
      .finally(() => {
        if (active) setDetailLoading(false)
      })

    return () => { active = false }
  }, [selectedNodeId])

  useEffect(() => {
    if (!selectedNodeId) return undefined

    function closeOnEscape(event) {
      if (event.key === 'Escape') setSelectedNodeId(null)
    }

    window.addEventListener('keydown', closeOnEscape)
    return () => window.removeEventListener('keydown', closeOnEscape)
  }, [selectedNodeId])

  function renderRelationships(title, relatedIds) {
    return (
      <section className="component-relationships">
        <h3>{title} <span>{relatedIds?.length || 0}</span></h3>
        {relatedIds?.length ? (
          <ul>
            {relatedIds.map((id) => {
              const relatedNode = nodes.find((node) => node.id === id)
              return (
                <li key={id}>
                  <strong>{relatedNode?.name || id}</strong>
                  {relatedNode?.type && <span>{relatedNode.type}</span>}
                  <code>{id}</code>
                </li>
              )
            })}
          </ul>
        ) : <p className="empty-copy">No relationships reported.</p>}
      </section>
    )
  }

  return (
    <div className="view-stack">
      <div className="page-heading">
        <div><span className="eyebrow">Topology</span><h1>Architecture Graph</h1></div>
        <span className="offline-pill">Offline mock graph</span>
      </div>
      <Panel title="Components" subtitle={`${filtered.length} components displayed`} action={
        <select className="select-control" value={category} onChange={(event) => setCategory(event.target.value)}>
          {categories.map((item) => <option key={item}>{item}</option>)}
        </select>
      }>
        <div className="node-grid">
          {filtered.map((node) => (
            <button
              className={`node-card ${selectedNodeId === node.id ? 'selected' : ''}`}
              key={node.id}
              type="button"
              onClick={() => setSelectedNodeId(node.id)}
              aria-haspopup="dialog"
              aria-pressed={selectedNodeId === node.id}
            >
              <div className={`node-symbol node-${node.type?.toLowerCase().replaceAll(' ', '-')}`}>
                {node.type === 'Microservice' ? 'MS' : node.type === 'Database' ? 'DB' : node.type === 'API route' ? 'API' : node.type === 'Frontend component' ? 'UI' : node.type === 'Shared module' ? 'LIB' : 'N'}
              </div>
              <div>
                <span>{node.type}</span>
                <h3>{node.name}</h3>
                <code>{node.id}</code>
              </div>
            </button>
          ))}
        </div>
      </Panel>
      {selectedNodeId && (
        <div
          className="component-dialog-backdrop"
          onClick={(event) => {
            if (event.target === event.currentTarget) setSelectedNodeId(null)
          }}
        >
          <section className="component-dialog" role="dialog" aria-modal="true" aria-labelledby="component-dialog-title">
            <header className="component-dialog-header">
              <div>
                <span className="eyebrow">Component details</span>
                <h2 id="component-dialog-title">{details?.name || selectedNodeId}</h2>
              </div>
              <button className="component-dialog-close" type="button" onClick={() => setSelectedNodeId(null)} aria-label="Close component details">
                ×
              </button>
            </header>
            <div className="component-dialog-content">
              <div className="component-meta">
                <div><span>Type</span><strong>{details?.type || '—'}</strong></div>
                <div><span>ID</span><code>{details?.id || selectedNodeId}</code></div>
              </div>
              <section className="component-description">
                <h3>Description</h3>
                <p>{details?.description || 'No description available for this component.'}</p>
              </section>
              {detailLoading && <p className="component-loading" role="status">Loading relationships…</p>}
              {detailError && <ErrorState message={detailError} />}
              {!detailError && !detailLoading && details?.id === selectedNodeId && (
                <div className="component-relationship-grid">
                  {renderRelationships('Outgoing dependencies', details.direct_dependencies)}
                  {renderRelationships('Incoming dependents', details.direct_dependents)}
                </div>
              )}
            </div>
          </section>
        </div>
      )}
    </div>
  )
}

function BlastView({ nodes }) {
  const [nodeId, setNodeId] = useState('legacy-auth-module')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function analyze(event) {
    event?.preventDefault()
    if (!nodeId.trim()) return
    setLoading(true)
    setError('')
    try {
      setResult(await api.blastRadius(nodeId.trim()))
    } catch (err) {
      setResult(null)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const suggestions = nodes.filter((node) =>
    ['legacy-auth-module', 'order-service', 'payment-service', 'shared-customer-db'].includes(node.id),
  )

  return (
    <div className="view-stack">
      <div className="page-heading">
        <div><span className="eyebrow">Impact analysis</span><h1>Blast Radius</h1></div>
      </div>
      <Panel title="Analyze a component" subtitle="Enter a node ID or choose a common component">
        <form className="blast-search" onSubmit={analyze}>
          <input
            list="node-options"
            value={nodeId}
            onChange={(event) => setNodeId(event.target.value)}
            placeholder="e.g. legacy-auth-module"
            aria-label="Component ID"
          />
          <datalist id="node-options">
            {nodes.map((node) => <option value={node.id} key={node.id}>{node.name}</option>)}
          </datalist>
          <button className="primary-button" type="submit" disabled={loading}>{loading ? 'Analyzing…' : 'Analyze impact'}</button>
        </form>
        <div className="quick-picks">
          {suggestions.map((node) => (
            <button key={node.id} onClick={() => { setNodeId(node.id); setError('') }}>{node.name}</button>
          ))}
        </div>
      </Panel>

      {error && <ErrorState message={error} />}
      {result && (
        <>
          <div className="impact-summary">
            <article><span>Target</span><strong>{result.target_name}</strong><code>{result.target_id}</code></article>
            <article><span>Total affected</span><strong>{result.total_affected_count}</strong><small>Source excluded</small></article>
            <article><span>Direct dependents</span><strong>{result.direct_dependents.length}</strong></article>
            <article><span>Indirect dependents</span><strong>{result.indirect_dependents.length}</strong></article>
          </div>
          <div className="impact-grid">
            <AffectedList title="Affected services" items={result.affected_services} />
            <AffectedList title="Affected API routes" items={result.affected_api_routes} />
            <AffectedList title="Affected frontend components" items={result.affected_frontend_components} />
            <AffectedList title="Direct dependents" items={result.direct_dependents} />
          </div>
        </>
      )}
    </div>
  )
}

function AffectedList({ title, items }) {
  return (
    <article className="list-card">
      <div className="list-card-heading"><h3>{title}</h3><span>{items?.length || 0}</span></div>
      {items?.length ? (
        <ul>{items.map((item) => <li key={item}><span className="list-dot" /><code>{item}</code></li>)}</ul>
      ) : <p className="empty-copy">No components in this category.</p>}
    </article>
  )
}

function CyclesView({ cycles, nodes, loading, error, onRetry, onOpenComponent }) {
  const nodeNames = new Map(nodes.map((node) => [node.id, node.name]))

  return (
    <div className="view-stack">
      <div className="page-heading">
        <h1>Circular Dependencies</h1>
        <span className="cycle-count">{loading ? '—' : cycles?.total_cycles ?? 0} cycles</span>
      </div>
      {error && <ErrorState message={error} onRetry={onRetry} />}
      {cycles?.cycles?.length ? (
        <section className="cycle-list" aria-label="Detected dependency cycles">
          {cycles.cycles.map((cycle, index) => (
            <article className="cycle-row" key={`${cycle.join('-')}-${index}`}>
              <span className="cycle-number">{index + 1}</span>
              <div className="cycle-chain">
                {[...cycle, cycle[0]].map((nodeId, nodeIndex, chain) => (
                  <span className="cycle-step" key={`${nodeId}-${nodeIndex}`}>
                    <button
                      type="button"
                      className="cycle-component"
                      onClick={() => onOpenComponent(nodeId)}
                      title={nodeId}
                      aria-label={`Open details for ${nodeNames.get(nodeId) || nodeId}`}
                    >
                      {nodeNames.get(nodeId) || nodeId}
                    </button>
                    {nodeIndex < chain.length - 1 && <span className="cycle-arrow" aria-hidden="true">→</span>}
                  </span>
                ))}
              </div>
            </article>
          ))}
        </section>
      ) : (
        !loading && !error && <p className="cycle-empty">No circular dependencies detected.</p>
      )}
      {loading && <p className="cycle-empty" role="status">Loading cycles…</p>}
    </div>
  )
}

function ReportsView({ reports }) {
  const [selectedIndex, setSelectedIndex] = useState(reports.length - 1)
  const selected = reports[selectedIndex] || reports[reports.length - 1]

  function copyReport() {
    if (selected?.text) navigator.clipboard.writeText(selected.text)
  }

  function downloadReport() {
    if (!selected?.text) return
    const blob = new Blob([selected.text], { type: 'text/markdown;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = 'architecture-analysis.md'
    anchor.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="view-stack">
      <div className="page-heading">
        <div><span className="eyebrow">Generated output</span><h1>Architecture Reports</h1></div>
        <div className="report-actions">
          <button className="secondary-button" onClick={copyReport} disabled={!selected}>Copy Markdown</button>
          <button className="primary-button" onClick={downloadReport} disabled={!selected}>Download .md</button>
        </div>
      </div>
      {selected ? (
        <Panel title="Backend analysis" subtitle={`Question: ${selected.query}`}>
          <pre className="report-document">{selected.text}</pre>
        </Panel>
      ) : (
        <Panel title="No reports generated yet">
          <div className="empty-state">
            <span>▤</span>
            <h3>Start with AI Chat</h3>
            <p>Submit a supported architecture question and its backend report will appear here.</p>
          </div>
        </Panel>
      )}
      {reports.length > 1 && (
        <div className="report-history">
          <h3>Current-session reports</h3>
          {reports.map((report, index) => (
            <button key={`${report.query}-${index}`} onClick={() => setSelectedIndex(index)}>
              <span>{report.query}</span>
              <small>View report</small>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

export default function App() {
  const [activeView, setActiveView] = useState('dashboard')
  const [health, setHealth] = useState(null)
  const [schema, setSchema] = useState(null)
  const [nodes, setNodes] = useState([])
  const [cycles, setCycles] = useState(null)
  const [graphOpenNodeId, setGraphOpenNodeId] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [reports, setReports] = useState([])

  async function loadDashboard() {
    setLoading(true)
    setError('')
    try {
      const [healthResult, schemaResult, nodesResult, cyclesResult] = await Promise.all([
        api.health(),
        api.schema(),
        api.nodes(),
        api.cycles(),
      ])
      setHealth(healthResult)
      setSchema(schemaResult)
      setNodes(nodesResult)
      setCycles(cyclesResult)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadDashboard() }, [])

  function rememberNavigationReport(result) {
    if (!result?.report_markdown) return
    setReports((current) => [...current, { query: result.user_query, text: result.report_markdown }])
  }

  function openGraphComponent(nodeId) {
    setGraphOpenNodeId(nodeId)
    setActiveView('graph')
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark"><span>AI</span></div>
          <div><strong>AI Architecture</strong><small>Assistant</small></div>
        </div>
        <nav>
          {NAV_ITEMS.map(([id, label, icon]) => (
            <IconButton key={id} active={activeView === id} onClick={() => setActiveView(id)} label={label}>{icon}</IconButton>
          ))}
        </nav>
        <div className="sidebar-status">
          <StatusBadge healthy={!error && health?.status === 'healthy'} />
          <small>NetworkX mock graph</small>
        </div>
      </aside>

      <main>
        <header className="topbar">
          <div><span>Workspace</span><strong>Task 2 · Architecture Navigator</strong></div>
          <StatusBadge healthy={!error && health?.status === 'healthy'} />
        </header>
        <div className="content">
          {activeView === 'dashboard' && <Dashboard health={health} schema={schema} cycles={cycles} loading={loading} error={error} onRetry={loadDashboard} />}
          {activeView === 'chat' && <ChatView onReport={rememberNavigationReport} />}
          {activeView === 'graph' && <GraphView nodes={nodes} schema={schema} openNodeId={graphOpenNodeId} />}
          {activeView === 'blast' && <BlastView nodes={nodes} />}
          {activeView === 'cycles' && <CyclesView cycles={cycles} nodes={nodes} loading={loading} error={error} onRetry={loadDashboard} onOpenComponent={openGraphComponent} />}
          {activeView === 'reports' && <ReportsView reports={reports} />}
        </div>
      </main>
    </div>
  )
}
