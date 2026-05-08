export function guardRoute() {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');
  if (!token || role !== 'sender') {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    window.location.href = '/login/login.html';
  }
}
