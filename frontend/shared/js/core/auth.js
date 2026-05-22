export function clearSession() {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
}

export function requireRole(expectedRole) {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');

  if (!token || role !== expectedRole) {
    clearSession();
    window.location.href = '/login/login.html';
    return false;
  }

  return true;
}
