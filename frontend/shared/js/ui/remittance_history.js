function buildStatusBadge(status) {
  return `<span class="status-badge status-${status.toLowerCase()}" style="background-color: #10b981; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.8rem;">${status}</span>`;
}

export function renderRemittanceHistoryRows(listEl, data, options = {}) {
  const {
    emptyMessage = 'No payment history available.',
  } = options;

  listEl.innerHTML = '';

  if (!data.length) {
    listEl.innerHTML = `<tr><td colspan="5" class="bill-empty-note">${emptyMessage}</td></tr>`;
    return;
  }

  data.forEach((tx) => {
    const row = document.createElement('tr');
    const otherUser = tx.other_username || 'Unknown';
    const billName = tx.bill_name || 'Unknown';

    row.innerHTML = `
      <td>#${tx.transaction_id}</td>
      <td>${otherUser} - ${billName}</td>
      <td>${tx.currency} ${tx.amount}</td>
      <td>${buildStatusBadge(tx.transaction_status)}</td>
      <td>${new Date(tx.created_at).toLocaleString()}</td>
    `;

    listEl.appendChild(row);
  });
}

export function renderRemittanceHistoryError(listEl, message, options = {}) {
  const { errorMessagePrefix = 'Error loading history: ' } = options;
  listEl.innerHTML = `<tr><td colspan="5" class="bill-empty-note" style="color:red;">${errorMessagePrefix}${message}</td></tr>`;
}
