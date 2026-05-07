import { API_BASE_URL } from './config.js';

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

    if (data.role !== 'beneficiary') {
        throw new Error('This panel is only for receivers (beneficiaries).');
    }

    localStorage.setItem('token', data.access_token);
    window.location.href = 'dashboard.html';
  } catch (err) {
    showError(err.message);
  }
}

export async function handleRegisterSubmit(event) {
  event.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  try {
    const res = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, role: 'beneficiary' })
    });
    
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Registration failed');

    alert('Registration successful! You can now login.');
    window.location.href = 'login.html';
  } catch (err) {
    showError(err.message);
  }
}
