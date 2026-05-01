import * as api from './api.js';
import * as ui from './ui.js';
import * as modal from './modal.js';
import { state } from './state.js';
import * as calendar from './calendar.js';
import { getProjectedBills } from './utils.js';

function selectBill(bill, row) {
  state.selectedBill = bill;
  ui.clearSelection();
  ui.updateSelectedText(bill);

  ui.elements.markPaidButton.textContent = bill.status === 'PAID' ? 'Mark UNPAID' : 'Mark PAID';
  
  // Disable actions for projected bills since they don't exist in the DB yet
  // We check for both the explicit flag and the ID prefix as a fallback
  const isProjected = bill.isProjected === true || (typeof bill.id === 'string' && bill.id.startsWith('proj-'));
  
  ui.elements.markPaidButton.disabled = isProjected;
  ui.elements.deleteButton.disabled = isProjected;
  
  if (isProjected) {
    ui.showStatus('Projected bill: Actions are disabled until the current instance is paid.');
  } else {
    ui.showStatus(`Selected: ${bill.name}. You can now Mark Paid or Delete.`);
  }

  row.classList.add('selected');
}

async function fetchBills() {
  ui.showStatus('Loading bills...');
  ui.elements.billsEl.textContent = '';
  ui.elements.paidBillsEl.textContent = '';
  ui.updateSelectedText({name: 'Select a bill to see actions.', total_amount: '-', due_date: '-', status: '-', recurring_interval: '-'});
  state.selectedBill = null;
  ui.clearSelection();

  try {
    const rawBills = await api.fetchAllBills();
    // Use the custom projection count from state
    const allBills = getProjectedBills(rawBills, state.currentYear, state.currentMonth, state.projectionCount);
    
    calendar.renderCalendar(allBills, (dateStr) => {
      state.selectedDate = dateStr;
      fetchBills();
    });

    if (state.selectedDate) {
      const billsForDate = allBills.filter(b => b.due_date === state.selectedDate);
      const dueForDate = billsForDate.filter(b => b.status === 'UNPAID');
      const paidForDate = billsForDate.filter(b => b.status === 'PAID');

      ui.renderList(ui.elements.billsEl, dueForDate, `No due bills for ${state.selectedDate}.`, selectBill, openCreateModal);
      ui.renderList(ui.elements.paidBillsEl, paidForDate, `No paid bills for ${state.selectedDate}.`, selectBill);
      ui.showStatus(`Showing bills for ${state.selectedDate}.`);
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
  if (!state.selectedBill) return;
  ui.showStatus(`Updating ${state.selectedBill.name}...`);
  try {
    await api.updateBillStatus(state.selectedBill.id, status);
    state.selectedBill.status = status;
    ui.showStatus(`Bill updated to ${status}.`);
    await fetchBills();
  } catch (error) {
    ui.showStatus('Unable to update bill.');
    console.error(error);
  }
}

function openDeleteConfirmation() {
  if (!state.selectedBill) return;
  const textEl = document.getElementById('delete-confirm-text');
  if (textEl) {
    textEl.textContent = `Are you sure you want to delete "${state.selectedBill.name}"?`;
  }
  modal.openDeleteModal();
}

async function handleConfirmDelete() {
  if (!state.selectedBill) return;
  ui.showStatus(`Deleting ${state.selectedBill.name}...`);
  try {
    await api.deleteBillById(state.selectedBill.id);
    modal.closeDeleteModal();
    await fetchBills();
  } catch (error) {
    ui.showStatus('Unable to delete bill.');
    console.error(error);
  }
}

async function createBill(event) {
  event.preventDefault();
  const form = ui.elements.createBillForm;
  const name = form.name.value.trim();
  const total_amount = parseFloat(form.total_amount.value);
  const due_date = form.due_date.value;
  const category = form.category.value.trim() || null;
  const recurring_interval = form.recurring_interval.value;

  if (!name || !due_date || Number.isNaN(total_amount) || total_amount < 0) {
    ui.showStatus('Please provide valid bill name, amount, and due date.');
    return;
  }

  ui.showStatus('Creating bill...');
  try {
    await api.createBill({ name, due_date, total_amount, category, recurring_interval });
    ui.showStatus('Bill created successfully.');
    form.reset();
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
    if (!state.selectedBill) return;
    const nextStatus = state.selectedBill.status === 'PAID' ? 'UNPAID' : 'PAID';
    patchBill(nextStatus);
  });
  ui.elements.deleteButton.addEventListener('click', openDeleteConfirmation);
  ui.elements.confirmDeleteButton.addEventListener('click', handleConfirmDelete);
  ui.elements.cancelDeleteButton.addEventListener('click', modal.closeDeleteModal);

  ui.elements.createBillForm.addEventListener('submit', createBill);
  ui.elements.closeCreateModalButton.addEventListener('click', modal.closeCreateModal);
  
  // Close modals when clicking outside
  window.addEventListener('click', (e) => {
    if (e.target === ui.elements.createModal) modal.closeCreateModal();
    if (e.target === ui.elements.deleteModal) modal.closeDeleteModal();
  });

  ui.elements.searchButton.addEventListener('click', handleSearch);
  ui.elements.searchInput.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') handleSearch();
  });
  ui.elements.prevMonthBtn.addEventListener('click', () => calendar.changeMonth(-1, fetchBills));
  ui.elements.nextMonthBtn.addEventListener('click', () => calendar.changeMonth(1, fetchBills));
}

function init() {
  modal.setDueDateDefaults();
  setupEventListeners();
  fetchBills();
}

init();
