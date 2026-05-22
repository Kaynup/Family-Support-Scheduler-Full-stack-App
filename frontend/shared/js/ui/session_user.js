export function setLoggedInUserLabel(elementId = 'user-info') {
  const userInfoEl = document.getElementById(elementId);
  if (!userInfoEl) {
    return;
  }

  const username = localStorage.getItem('username') || 'Unknown';
  const role = localStorage.getItem('role') || '';
  userInfoEl.textContent = `Logged in as ${username} (${role})`;
}
