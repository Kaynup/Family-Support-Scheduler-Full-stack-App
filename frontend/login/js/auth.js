import { API_BASE_URL } from '../../shared/js/config.js';

function showError(msg) {
  const errEl = document.getElementById('error-message');
  if (errEl) {
    errEl.textContent = msg;
    errEl.style.display = 'block';
  } else {
    alert(msg);
  }
}

export async function handleLoginSubmit(event) {
  event.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  try {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Login failed');

    localStorage.setItem('token', data.access_token);
    localStorage.setItem('role', data.role);

    if (data.role === 'beneficiary') {
      window.location.href = '/receiver_panel/pages/dashboard.html';
    } else if (data.role === 'sender') {
      window.location.href = '/sender_panel/pages/dashboard.html';
    } else {
      throw new Error('Unknown role received from server.');
    }
  } catch (err) {
    showError(err.message);
  }
}

export async function handleRegisterSubmit(event) {
  event.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const role = document.getElementById('role').value;

  try {
    const res = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, role })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Registration failed');

    alert('Registration successful! You can now log in.');
    window.location.href = 'login.html';
  } catch (err) {
    showError(err.message);
  }
}
