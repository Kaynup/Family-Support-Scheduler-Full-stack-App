import * as api from '../core/api.js';
import * as ui from '../components/ui.js';
import * as calendar from '../components/calendar.js';
import { state } from '../core/state.js';
import { getProjectedBills } from '../core/utils.js';
import { openCreateModal } from '../components/modal.js';

export function selectBill(bill, row) {
  state.selectedBill = bill;
  ui.clearSelection();
  ui.updateSelectedText(bill);

  ui.elements.markPaidButton.textContent = bill.status === 'PAID' ? 'Mark UNPAID' : 'Mark PAID';
  
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

export async function fetchBills() {
  prepareUIForLoading();

  try {
    const rawBills = await api.fetchAllBills();
    const allBills = getProjectedBills(rawBills, state.currentYear, state.currentMonth, state.projectionCount);
    
    calendar.renderCalendar(allBills, (dateStr) => {
      state.selectedDate = dateStr;
      fetchBills();
    });

    updateDashboardLists(allBills);
  } catch (error) {
    ui.showStatus(`Unable to load bills: ${error.message}`);
    console.error(error);
  }
}

function prepareUIForLoading() {
  ui.showStatus('Loading bills...');
  ui.elements.billsEl.textContent = '';
  ui.elements.paidBillsEl.textContent = '';
  ui.updateSelectedText({name: 'Select a bill to see actions.', total_amount: '-', due_date: '-', status: '-', recurring_interval: '-'});
  state.selectedBill = null;
  ui.clearSelection();
}

function updateDashboardLists(allBills) {
  if (!state.selectedDate) {
    showEmptyDateState();
    return;
  }

  const billsForDate = allBills.filter(b => b.due_date === state.selectedDate);
  const dueForDate = billsForDate.filter(b => b.status === 'UNPAID');
  const paidForDate = billsForDate.filter(b => b.status === 'PAID');

  ui.renderList(ui.elements.billsEl, dueForDate, `No due bills for ${state.selectedDate}.`, selectBill, openCreateModal);
  ui.renderList(ui.elements.paidBillsEl, paidForDate, `No paid bills for ${state.selectedDate}.`, selectBill);
  ui.showStatus(`Showing bills for ${state.selectedDate}.`);
}

function showEmptyDateState() {
  ui.elements.billsEl.innerHTML = '<p class="bill-empty-note">Please select a date on the calendar to view bills.</p>';
  ui.elements.paidBillsEl.innerHTML = '<p class="bill-empty-note">Please select a date on the calendar to view bills.</p>';
  ui.showStatus('Select a date on the calendar.');
}
