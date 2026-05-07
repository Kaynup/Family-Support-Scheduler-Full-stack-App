export const elements = {
  billsContainerEl: document.getElementById('bills'),
  paidBillsContainerEl: document.getElementById('paid-bills'),
  statusDisplayEl: document.getElementById('status'),
  selectedBillSummaryEl: document.getElementById('selected-text'),
  payButton: document.getElementById('pay-bill'),
  searchInput: document.getElementById('search-input'),
  searchButton: document.getElementById('search-btn'),
  searchResultsContainerEl: document.getElementById('search-results-list'),
  calendarGridEl: document.getElementById('calendar-grid'),
  calendarMonthYearEl: document.getElementById('calendar-month-year'),
  prevMonthBtn: document.getElementById('prev-month'),
  nextMonthBtn: document.getElementById('next-month'),
  payModal: document.getElementById('pay-modal'),
  confirmPayButton: document.getElementById('confirm-pay'),
  cancelPayButton: document.getElementById('cancel-pay'),
  upcomingModal: document.getElementById('upcoming-modal'),
  upcomingList: document.getElementById('upcoming-bills-list'),
  upcomingOkButton: document.getElementById('upcoming-button'),
};

export function displayStatusMessage(message) {
  if (elements.statusDisplayEl) {
    elements.statusDisplayEl.textContent = message;
  }
}

export function renderSelectedBillSummary(bill) {
  if (!elements.selectedBillSummaryEl) return;
  if (bill.name === 'Select a bill to see actions.') {
    elements.selectedBillSummaryEl.textContent = bill.name;
  } else {
    elements.selectedBillSummaryEl.textContent = `${bill.name} · Rs.${bill.total_amount} · due ${bill.due_date} · ${bill.status} · ${bill.recurring_interval || 'NONE'}`;
  }
}

export function clearSelectionHighlights() {
  document.querySelectorAll('.selected').forEach((rowEl) => rowEl.classList.remove('selected'));
  if (elements.payButton) elements.payButton.disabled = true;
}

export function renderBillTable(containerEl, billsList, emptyMessage, onSelectBill) {
  if (!containerEl) return;
  containerEl.textContent = '';

  const tableEl = document.createElement('table');
  tableEl.className = 'bill-table';

  tableEl.appendChild(getTableHeaderHTML());

  const tbodyEl = document.createElement('tbody');

  if (!billsList.length) {
    renderEmptyStateHTML(tbodyEl, emptyMessage);
  } else {
    renderBillRowsHTML(tbodyEl, billsList, onSelectBill);
  }

  tableEl.appendChild(tbodyEl);
  containerEl.appendChild(tableEl);
}

function getTableHeaderHTML() {
  const theadEl = document.createElement('thead');
  const headerRowEl = document.createElement('tr');
  headerRowEl.innerHTML = '<th>Name</th><th>Category</th><th>Amount</th><th>Due Date</th>';
  theadEl.appendChild(headerRowEl);
  return theadEl;
}

function renderEmptyStateHTML(tbodyEl, emptyText) {
  const noteRowEl = document.createElement('tr');
  const noteCellEl = document.createElement('td');
  noteCellEl.colSpan = 4;
  noteCellEl.className = 'bill-empty-note';
  noteCellEl.textContent = emptyText;
  noteRowEl.appendChild(noteCellEl);
  tbodyEl.appendChild(noteRowEl);
}

function renderBillRowsHTML(tbodyEl, billsList, onSelectBill) {
  billsList.forEach((bill) => {
    const rowEl = document.createElement('tr');
    rowEl.className = 'bill-row';
    rowEl.innerHTML = `
      <td>${bill.name}</td>
      <td>${bill.category || '-'}</td>
      <td>Rs.${bill.total_amount}</td>
      <td>${bill.due_date}</td>
    `;
    if (onSelectBill) {
      rowEl.addEventListener('click', () => onSelectBill(bill, rowEl));
    }
    tbodyEl.appendChild(rowEl);
  });
}

export function renderRemittanceStatusBadge(status) {
  const badge = document.createElement('span');
  badge.className = `status-badge status-${status.toLowerCase()}`;
  badge.textContent = status;
  return badge;
}
