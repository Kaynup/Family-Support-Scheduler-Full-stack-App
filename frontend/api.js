const API_URL = "http://127.0.0.1:8000";

async function requestJson(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, options);
  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(payload.detail || payload.message || response.statusText || `HTTP ${response.status}`);
  }

  return payload;
}

export async function fetchUpcomingBills(days) {
  const result = await requestJson(`/bills/upcoming?days=${encodeURIComponent(days)}`);
  return Array.isArray(result) ? result : result.data || [];
}

export async function fetchAllBills() {
  const result = await requestJson('/bills/all');
  return Array.isArray(result) ? result : result.data || [];
}

export async function updateBillStatus(id, status) {
  await requestJson(`/bills/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status }),
  });
}

export async function deleteBillById(id) {
  await requestJson(`/bills/${id}`, {
    method: 'DELETE',
  });
}

export async function createBill(payload) {
  return requestJson('/bills/new', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
}
