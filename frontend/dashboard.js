import * as api from './api.js';
import * as ui from './ui.js';
import * as modal from './modal.js';
import { getDaysUntilDue } from './utils.js';

let selectedBill = null;
let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();
let selectedDate = null; // Format: YYYY-MM-DD

function selectBill(bill, row) {
  selectedBill = bill;
  ui.clearSelection();
  ui.updateSelectedText(bill);

  ui.elements.markPaidButton.textContent = bill.status === 'PAID' ? 'Mark UNPAID' : 'Mark PAID';
  ui.elements.markPaidButton.disabled = false;
  ui.elements.deleteButton.disabled = false;
  row.classList.add('selected');
}

async function fetchBills() {
  ui.showStatus('Loading bills...');
  ui.elements.billsEl.textContent = '';
  ui.elements.paidBillsEl.textContent = '';
  ui.updateSelectedText({name: 'Select a bill to see actions.', total_amount: '-', due_date: '-', status: '-', recurring_interval: '-'});
  selectedBill = null;
  ui.clearSelection();

  try {
    const allBills = await api.fetchAllBills();
    
    // Determine which dates should glow (all UNPAID bills)
    const upcomingBills = allBills.filter(b => b.status === 'UNPAID');
    renderCalendar(upcomingBills);

    if (selectedDate) {
      const billsForDate = allBills.filter(b => b.due_date === selectedDate);
      const dueForDate = billsForDate.filter(b => b.status === 'UNPAID');
      const paidForDate = billsForDate.filter(b => b.status === 'PAID');

      ui.renderList(ui.elements.billsEl, dueForDate, `No due bills for ${selectedDate}.`, selectBill, openCreateModal);
      ui.renderList(ui.elements.paidBillsEl, paidForDate, `No paid bills for ${selectedDate}.`, selectBill);
      ui.showStatus(`Showing bills for ${selectedDate}.`);
    } else {
      ui.elements.billsEl.innerHTML = '<p class="bill-empty-note">Please select a date on the calendar to view bills.</p>';
      ui.elements.paidBillsEl.innerHTML = '<p class="bill-empty-note">Please select a date on the calendar to view bills.</p>';
      ui.showStatus('Select a date on the calendar.');
    }
  } catch (error) {
    ui.showStatus(`Unable to load bills: ${error.message}`);
    console.error(error);
  }
}

async function patchBill(status) {
  if (!selectedBill) return;

  ui.showStatus(`Updating ${selectedBill.name}...`);

  try {
    await api.updateBillStatus(selectedBill.id, status);
    selectedBill.status = status;

    if (status === 'UNPAID') {
      ui.showStatus(`Bill updated to UNPAID.`);
    }

    await fetchBills();
  } catch (error) {
    ui.showStatus('Unable to update bill.');
    console.error(error);
  }
}

async function deleteBill() {
  if (!selectedBill) return;

  ui.showStatus(`Deleting ${selectedBill.name}...`);

  try {
    await api.deleteBillById(selectedBill.id);
    await fetchBills();
  } catch (error) {
    ui.showStatus('Unable to delete bill.');
    console.error(error);
  }
}

async function createBill(event) {
  event.preventDefault();

  const name = ui.elements.createBillForm.name.value.trim();
  const total_amount = parseFloat(ui.elements.createBillForm.total_amount.value);
  const due_date = ui.elements.createBillForm.due_date.value;
  const category = ui.elements.createBillForm.category.value.trim() || null;
  const recurring_interval = ui.elements.createBillForm.recurring_interval.value;

  if (!name || !due_date || Number.isNaN(total_amount) || total_amount < 0) {
    ui.showStatus('Please provide valid bill name, amount, and due date.');
    return;
  }

  ui.showStatus('Creating bill...');

  try {
    await api.createBill({ name, due_date, total_amount, category, recurring_interval });
    ui.showStatus('Bill created successfully.');
    ui.elements.createBillForm.reset();
    modal.closeCreateModal();
    modal.setDueDateDefaults();
    await fetchBills();
  } catch (error) {
    ui.showStatus(`Unable to create bill: ${error.message}`);
    console.error(error);
  }
}

function openCreateModal() {
  modal.openCreateModal();
}

function renderCalendar(upcomingBills) {
  ui.elements.calendarGrid.textContent = '';
  
  const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  ui.elements.calendarMonthYear.textContent = `${monthNames[currentMonth]} ${currentYear}`;
  
  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const dueDates = new Set(upcomingBills.map(b => b.due_date));
  
  // Headers
  const dayHeaders = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
  dayHeaders.forEach(d => {
    const el = document.createElement('div');
    el.textContent = d;
    el.style.textAlign = 'center';
    el.style.fontWeight = 'bold';
    el.style.fontSize = '0.7rem';
    ui.elements.calendarGrid.appendChild(el);
  });
  
  // Padding for first day
  const firstDay = new Date(currentYear, currentMonth, 1).getDay();
  for (let i = 0; i < firstDay; i++) {
    const el = document.createElement('div');
    ui.elements.calendarGrid.appendChild(el);
  }
  
  // Days
  for (let i = 1; i <= daysInMonth; i++) {
    const el = document.createElement('div');
    el.className = 'calendar-day';
    el.textContent = i;
    el.style.cursor = 'pointer';
    
    const dateStr = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
    
    // Highlight if selected
    if (dateStr === selectedDate) {
      el.style.background = '#dbeafe';
      el.style.borderColor = '#2563eb';
    }

    // Check if it's a glowing date
    if (dueDates.has(dateStr)) {
      el.classList.add('glow');
    }

    el.addEventListener('click', () => {
      selectedDate = dateStr;
      fetchBills();
    });
    
    ui.elements.calendarGrid.appendChild(el);
  }
}

function changeMonth(delta) {
  currentMonth += delta;
  if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
  } else if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  fetchBills();
}

async function handleSearch() {
  const query = ui.elements.searchInput.value.trim();
  if (!query) {
    ui.elements.searchResultsEl.textContent = '';
    return;
  }
  
  ui.showStatus(`Searching for "${query}"...`);
  try {
    const results = await api.searchBills(query);
    ui.renderList(ui.elements.searchResultsEl, results, 'No matching bills found.', selectBill);
    ui.showStatus(`Found ${results.length} bills matching "${query}".`);
  } catch (error) {
    ui.showStatus(`Search failed: ${error.message}`);
    console.error(error);
  }
}

function setupEventListeners() {
  ui.elements.markPaidButton.addEventListener('click', () => {
    if (!selectedBill) return;
    const nextStatus = selectedBill.status === 'PAID' ? 'UNPAID' : 'PAID';
    patchBill(nextStatus);
  });
  ui.elements.deleteButton.addEventListener('click', deleteBill);
  ui.elements.createBillForm.addEventListener('submit', createBill);
  ui.elements.closeCreateModalButton.addEventListener('click', modal.closeCreateModal);
  ui.elements.createModal.addEventListener('click', (event) => {
    if (event.target === ui.elements.createModal) {
      modal.closeCreateModal();
    }
  });
  ui.elements.searchButton.addEventListener('click', handleSearch);
  ui.elements.searchInput.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') handleSearch();
  });
  ui.elements.prevMonthBtn.addEventListener('click', () => changeMonth(-1));
  ui.elements.nextMonthBtn.addEventListener('click', () => changeMonth(1));
}

function init() {
  modal.setDueDateDefaults();
  setupEventListeners();
  fetchBills();
}

init();
