import { API_BASE_URL } from '../../../../shared/js/config.js';

async function requestJson(path, options = {}) {
  const token = localStorage.getItem('token');
  const headers = { ...options.headers };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    if (response.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      window.location.href = '/login/login.html';
    }
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

export async function searchBills(name) {
  const result = await requestJson(`/bills/search?name=${encodeURIComponent(name)}`);
  return Array.isArray(result) ? result : result.data || [];
}

export async function fetchRemittanceHistory() {
  const result = await requestJson('/remittance/history/beneficiary');
  return Array.isArray(result) ? result : result.data || [];
}
