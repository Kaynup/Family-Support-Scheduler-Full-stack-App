export function guardRoute() {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');
  if (!token || role !== 'beneficiary') {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    window.location.href = '/login/login.html';
  }
}
