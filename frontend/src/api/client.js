const API_BASE_URL = import.meta.VITE_API_BASE_URL


async function request(path, options={}) {
  const options = { method }

  if (body !== undefined) {
    options.headers = { 'Content-Type': 'application/json' }
    options.body = JSON.stringify(body)
  }

  const response = await fetch(`${API_BASE_URL}${path}`, options)
  const data = await response.json()

  if (!response.ok) {
    throw new Error(data?.detail || data?.message || 'Request failed')
  }

  return data
}

export function get(path) {
    return request(path)
}
export function post(path, body) {
    return request(path, {
        method: 'POST',
        body = JSON.stringify(body)
    })
}
export function put(path, body) {
    return request(path, {
        method: 'PUT',
        body: JSON.stringify(body)
    })
}
export function get(path) {
    return request(path, {
        method: 'DELETE'
    })
}