export const elements = {
  billsEl: document.getElementById('bills'),
  paidBillsEl: document.getElementById('paid-bills'),
  statusEl: document.getElementById('status'),
  selectedText: document.getElementById('selected-text'),
  markPaidButton: document.getElementById('mark-paid'),
  deleteButton: document.getElementById('delete-bill'),
  createBillForm: document.getElementById('create-bill-form'),
  dueDateInput: document.getElementById('bill-due'),
  createModal: document.getElementById('create-modal'),
  closeCreateModalButton: document.getElementById('close-create-modal'),
  searchInput: document.getElementById('search-input'),
  searchButton: document.getElementById('search-btn'),
  searchResultsEl: document.getElementById('search-results-list'),
  calendarGrid: document.getElementById('calendar-grid'),
  calendarMonthYear: document.getElementById('calendar-month-year'),
  prevMonthBtn: document.getElementById('prev-month'),
  nextMonthBtn: document.getElementById('next-month'),
};

export function showStatus(message) {
  elements.statusEl.textContent = message;
}

export function updateSelectedText(bill) {
  if (bill.name === 'Select a bill to see actions.') {
    elements.selectedText.textContent = bill.name;
  } else {
    elements.selectedText.textContent = `${bill.name} · Rs.${bill.total_amount} · due ${bill.due_date} · ${bill.status} · ${bill.recurring_interval || 'NONE'}`;
  }
}

export function clearSelection() {
  document.querySelectorAll('.selected').forEach((row) => row.classList.remove('selected'));
  elements.markPaidButton.disabled = true;
  elements.deleteButton.disabled = true;
}

export function renderList(container, bills, emptyText, onSelectBill, onAddClick) {
  container.textContent = '';

  const table = document.createElement('table');
  table.className = 'bill-table';

  const headerRow = document.createElement('tr');
  headerRow.innerHTML = '<th>Name</th><th>Category</th><th>Amount</th><th>Due (Calendar)</th>';

  const thead = document.createElement('thead');
  thead.appendChild(headerRow);
  table.appendChild(thead);

  const tbody = document.createElement('tbody');

  if (!bills.length) {
    const noteRow = document.createElement('tr');
    const noteCell = document.createElement('td');
    noteCell.colSpan = 4;
    noteCell.className = 'bill-empty-note';
    noteCell.textContent = emptyText;
    noteRow.appendChild(noteCell);
    tbody.appendChild(noteRow);
  } else {
    bills.forEach((bill) => {
      const row = document.createElement('tr');
      row.className = 'bill-row';
      row.innerHTML = `
        <td>${bill.name}</td>
        <td>${bill.category || '-'}</td>
        <td>Rs.${bill.total_amount}</td>
        <td>${bill.due_date}</td>
      `;
      row.addEventListener('click', () => onSelectBill(bill, row));
      tbody.appendChild(row);
    });
  }

  if (onAddClick && container.id === 'bills') {
    const addRow = document.createElement('tr');
    addRow.className = 'bill-add-row';
    addRow.innerHTML = `
      <td colspan="4">
        <button type="button" class="bill-add-button">+</button>
      </td>
    `;
    addRow.querySelector('.bill-add-button').addEventListener('click', onAddClick);
    tbody.appendChild(addRow);
  }

  table.appendChild(tbody);
  container.appendChild(table);
}