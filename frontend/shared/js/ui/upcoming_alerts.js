import { isBillExpired } from '../core/bill_utils.js';

export async function showUpcomingAndExpiredBills(options) {
  const {
    fetchUpcoming,
    fetchExpired,
    listEl,
    modalEl,
    sessionKey = 'upcomingModalShown',
  } = options;

  if (sessionStorage.getItem(sessionKey)) {
    return;
  }

  const [upcomingBills, expiredBills] = await Promise.all([
    fetchUpcoming(3),
    fetchExpired(),
  ]);

  const sortedUpcoming = [...upcomingBills].sort((a, b) => new Date(a.due_date) - new Date(b.due_date));
  const sortedExpired = [...expiredBills].sort((a, b) => new Date(b.due_date) - new Date(a.due_date));
  const allAlertBills = [...sortedUpcoming, ...sortedExpired];

  if (!allAlertBills.length || !listEl || !modalEl) {
    return;
  }

  listEl.innerHTML = '';

  allAlertBills.forEach((bill) => {
    const item = document.createElement('tr');
    item.className = 'upcoming-item';
    const expired = isBillExpired(bill);
    const status = expired
      ? '<span style="color:red;font-weight:bold;">EXPIRED</span>'
      : '<span style="font-weight:bold;">DUE</span>';

    item.innerHTML = `<td>${bill.name}</td><td>${bill.due_date}</td><td>Rs.${bill.total_amount}</td><td>${status}</td><td>${bill.recurring_interval}</td>`;
    listEl.appendChild(item);
  });

  modalEl.classList.remove('hidden');
  sessionStorage.setItem(sessionKey, 'true');
}
