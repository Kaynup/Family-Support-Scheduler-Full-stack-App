export const elements = {
  billsContainerEl: document.getElementById('bills'),
  paidBillsContainerEl: document.getElementById('paid-bills'),
  statusDisplayEl: document.getElementById('status'),
  selectedBillSummaryEl: document.getElementById('selected-text'),
  markPaidButton: document.getElementById('mark-paid'),
  deleteButton: document.getElementById('delete-bill'),
  createBillForm: document.getElementById('create-bill-form'),
  dueDateInput: document.getElementById('bill-due'),
  createModal: document.getElementById('create-modal'),
  closeCreateModalButton: document.getElementById('close-create-modal'),
  searchInput: document.getElementById('search-input'),
  searchButton: document.getElementById('search-btn'),
  searchResultsContainerEl: document.getElementById('search-results-list'),
  calendarGridEl: document.getElementById('calendar-grid'),
  calendarMonthYearEl: document.getElementById('calendar-month-year'),
  prevMonthBtn: document.getElementById('prev-month'),
  nextMonthBtn: document.getElementById('next-month'),
  deleteModal: document.getElementById('delete-modal'),
  confirmDeleteButton: document.getElementById('confirm-delete'),
  cancelDeleteButton: document.getElementById('cancel-delete'),
};

export function displayStatusMessage(message) {
  elements.statusDisplayEl.textContent = message;
}

export function renderSelectedBillSummary(bill) {
  if (bill.name === 'Select a bill to see actions.') {
    elements.selectedBillSummaryEl.textContent = bill.name;
  } else {
    elements.selectedBillSummaryEl.textContent = `${bill.name} · Rs.${bill.total_amount} · due ${bill.due_date} · ${bill.status} · ${bill.recurring_interval || 'NONE'}`;
  }
}

export function clearSelectionHighlights() {
  document.querySelectorAll('.selected').forEach((rowEl) => rowEl.classList.remove('selected'));
  elements.markPaidButton.disabled = true;
  elements.deleteButton.disabled = true;
}

export function renderBillTable(containerEl, billsList, emptyMessage, onSelectBill, onAddClick) {
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

  if (onAddClick && containerEl.id === 'bills') {
    renderAddButtonRowHTML(tbodyEl, onAddClick);
  }

  tableEl.appendChild(tbodyEl);
  containerEl.appendChild(tableEl);
}

function getTableHeaderHTML() {
  const theadEl = document.createElement('thead');
  const headerRowEl = document.createElement('tr');
  headerRowEl.innerHTML = '<th>Name</th><th>Category</th><th>Amount</th><th>Due (Calendar)</th>';
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
    rowEl.addEventListener('click', () => onSelectBill(bill, rowEl));
    tbodyEl.appendChild(rowEl);
  });
}

function renderAddButtonRowHTML(tbodyEl, onAddClick) {
  const addRowEl = document.createElement('tr');
  addRowEl.className = 'bill-add-row';
  addRowEl.innerHTML = `
    <td colspan="4">
      <button type="button" class="bill-add-button">+</button>
    </td>
  `;
  addRowEl.querySelector('.bill-add-button').addEventListener('click', onAddClick);
  tbodyEl.appendChild(addRowEl);
}
