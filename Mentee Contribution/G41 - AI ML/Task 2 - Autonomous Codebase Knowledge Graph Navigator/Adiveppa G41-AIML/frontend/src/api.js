export const API_BASE_URL = 'http://127.0.0.1:8000'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      Accept: 'application/json',
      ...(options.body ? { 'Content-Type': 'application/json' } : {}),
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`
    try {
      const body = await response.json()
      detail = body.detail || detail
    } catch {
      // Keep the status-based message when the response has no JSON body.
    }
    throw new Error(detail)
  }

  return response.json()
}

export const api = {
  health: () => request('/health'),
  schema: () => request('/schema'),
  nodes: () => request('/nodes'),
  node: (nodeId) => request(`/nodes/${encodeURIComponent(nodeId)}`),
  cycles: () => request('/cycles'),
  blastRadius: (nodeId) =>
    request('/blast-radius', {
      method: 'POST',
      body: JSON.stringify({ node_id: nodeId }),
    }),
  navigate: (query) =>
    request('/navigate', {
      method: 'POST',
      body: JSON.stringify({ query }),
    }),
}
