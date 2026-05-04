import * as API from '../core/api.js';
import * as UI from '../components/ui.js';
import * as Calendar from '../components/calendar.js';
import { state } from '../core/state.js';
import { getProjectedBills } from '../core/utils.js';
import * as Modal from '../components/modal.js';

export function handleSelectBill(bill, rowEl) {
  state.selectedBill = bill;
  UI.clearSelectionHighlights();
  UI.renderSelectedBillSummary(bill);

  UI.elements.markPaidButton.textContent = bill.status === 'PAID' ? 'Mark UNPAID' : 'Mark PAID';

  const isProjected = !!bill.isProjected;

  UI.elements.markPaidButton.disabled = false; // Allow status updates for all
  UI.elements.deleteButton.disabled = isProjected; // Keep delete disabled for virtuals

  if (isProjected) {
    UI.displayStatusMessage('Projected bill: Marking as PAID will create a new record in the database.');
  } else {
    UI.displayStatusMessage(`Selected: ${bill.name}. You can now Mark Paid or Delete.`);
  }

  rowEl.classList.add('selected');
}

export async function fetchAndRenderBills() {
  prepareUIForLoading();

  try {
    const rawBills = await API.fetchAllBills();
    const allBills = getProjectedBills(rawBills, state.currentYear, state.currentMonth, state.projectionCount);

    Calendar.renderCalendar(allBills, (dateStr) => {
      state.selectedDate = dateStr;
      fetchAndRenderBills();
    });

    updateDashboardLists(allBills);
  } catch (error) {
    UI.displayStatusMessage(`Unable to load bills: ${error.message}`);
    console.error(error);
  }
}

function prepareUIForLoading() {
  UI.displayStatusMessage('Loading bills...');
  UI.elements.billsContainerEl.textContent = '';
  UI.elements.paidBillsContainerEl.textContent = '';
  UI.renderSelectedBillSummary({ name: 'Select a bill to see actions.', total_amount: '-', due_date: '-', status: '-', recurring_interval: '-' });
  state.selectedBill = null;
  UI.clearSelectionHighlights();
}

function updateDashboardLists(allBills) {
  if (!state.selectedDate) {
    renderEmptyDateState();
    return;
  }

  const billsForDate = allBills.filter(b => b.due_date === state.selectedDate);
  const dueForDate = billsForDate.filter(b => b.status === 'UNPAID');
  const paidForDate = billsForDate.filter(b => b.status === 'PAID');

  UI.renderBillTable(UI.elements.billsContainerEl, dueForDate, `No due bills for ${state.selectedDate}.`, handleSelectBill, Modal.handleOpenCreateModal);
  UI.renderBillTable(UI.elements.paidBillsContainerEl, paidForDate, `No paid bills for ${state.selectedDate}.`, handleSelectBill);
  UI.displayStatusMessage(`Showing bills for ${state.selectedDate}.`);
}

function renderEmptyDateState() {
  UI.elements.billsContainerEl.innerHTML = '<p class="bill-empty-note">Please select a date on the calendar to view bills.</p>';
  UI.elements.paidBillsContainerEl.innerHTML = '<p class="bill-empty-note">Please select a date on the calendar to view bills.</p>';
  UI.displayStatusMessage('Select a date on the calendar.');
}
