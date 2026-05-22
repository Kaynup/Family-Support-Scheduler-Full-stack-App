import { API_BASE_URL } from '../config.js';

function clearSessionAndRedirect() {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  window.location.href = '/login/login.html';
}

export async function requestJson(path, options = {}) {
  const token = localStorage.getItem('token');
  const headers = { ...options.headers };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    if (response.status === 401) {
      clearSessionAndRedirect();
    }
    throw new Error(payload.detail || payload.message || response.statusText || `HTTP ${response.status}`);
  }

  return payload;
}

function normalizeList(payload) {
  return Array.isArray(payload) ? payload : payload.data || [];
}

export async function fetchUpcomingBills(days) {
  const result = await requestJson(`/bills/upcoming?days=${encodeURIComponent(days)}`);
  return normalizeList(result);
}

export async function fetchExpiredBills() {
  const result = await requestJson('/bills/expired');
  return normalizeList(result);
}

export async function fetchAllBills() {
  const result = await requestJson('/bills/all');
  return normalizeList(result);
}

export async function fetchAllBillsForBeneficiary(beneficiaryId) {
  const result = await requestJson(`/bills/all?beneficiary_id=${encodeURIComponent(beneficiaryId)}`);
  return normalizeList(result);
}

export async function fetchUsers(role) {
  const result = await requestJson(`/users?role=${encodeURIComponent(role)}`);
  return normalizeList(result);
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
  return normalizeList(result);
}

export async function payBill(billId, amount) {
  return requestJson('/remittance/pay', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ bill_id: billId, amount }),
  });
}

export async function fetchRemittanceHistoryByRole(role) {
  const endpoint = role === 'beneficiary' ? '/remittance/history/beneficiary' : '/remittance/history';
  const result = await requestJson(endpoint);
  return normalizeList(result);
}
