import * as api from './api.js';
import * as ui from './ui.js';
import * as modal from './modal.js';
import { getDaysUntilDue } from './utils.js';

let selectedBill = null;

function selectBill(bill, row) {
  selectedBill = bill;
  ui.clearSelection();
  ui.updateSelectedText(`${bill.name} · ₹${bill.total_amount} · due ${bill.due_date} · ${bill.status}`);

  ui.elements.markPaidButton.textContent = bill.status === 'PAID' ? 'Mark UNPAID' : 'Mark PAID';
  ui.elements.markPaidButton.disabled = false;
  ui.elements.deleteButton.disabled = false;
  row.classList.add('selected');
}

async function fetchBills() {
  const days = Math.max(1, Number(ui.elements.daysInput.value) || 1);
  ui.showStatus('Loading bills...');
  ui.elements.billsEl.textContent = '';
  ui.elements.paidBillsEl.textContent = '';
  ui.updateSelectedText('Select a bill to see actions.');
  selectedBill = null;
  ui.clearSelection();

  try {
    const upcomingBills = await api.fetchUpcomingBills(days);
    const allBills = await api.fetchAllBills();
    const paidBills = allBills.filter((bill) => bill.status === 'PAID');

    ui.renderList(ui.elements.billsEl, upcomingBills, 'No current bills found.', selectBill, openCreateModal);
    ui.renderList(ui.elements.paidBillsEl, paidBills, 'No paid bills found.', selectBill);

    ui.showStatus(`Showing ${upcomingBills.length} due bill(s) and ${paidBills.length} paid bill(s).`);
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
      const dueDays = getDaysUntilDue(selectedBill);
      const currentDays = Math.max(1, Number(ui.elements.daysInput.value) || 1);
      if (dueDays > currentDays) {
        ui.elements.daysInput.value = dueDays;
        ui.showStatus(`Bill updated to UNPAID. Adjusted due filter to ${dueDays} day(s) so it appears.`);
      }
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

  if (!name || !due_date || Number.isNaN(total_amount) || total_amount < 0) {
    ui.showStatus('Please provide valid bill name, amount, and due date.');
    return;
  }

  ui.showStatus('Creating bill...');

  try {
    await api.createBill({ name, due_date, total_amount, category });
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

function setupEventListeners() {
  ui.elements.loadButton.addEventListener('click', fetchBills);
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
}

function init() {
  modal.setDueDateDefaults();
  setupEventListeners();
  fetchBills();
}

init();
