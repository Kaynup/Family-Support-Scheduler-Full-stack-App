import * as API from '../core/api.js';
import * as UI from '../components/ui.js';
import * as Calendar from '../components/calendar.js';
import { state } from '../core/state.js';
import { getProjectedBills, filterBillsForDisplay } from '../core/utils.js';
import * as Modal from '../components/modal.js';

export function handleSelectBill(bill, rowEl) {
  state.selectedBill = bill;
  UI.clearSelectionHighlights();
  UI.renderSelectedBillSummary(bill);
  const isProjected = !!bill.isProjected;
  UI.elements.deleteButton.disabled = isProjected; // Keep delete disabled for virtuals
  UI.displayStatusMessage(isProjected ? 'Projected bill selected.' : `Selected: ${bill.name}.`);
  rowEl.classList.add('selected');
}

export async function fetchAndRenderBills() {
  prepareUIForLoading();

  try {
    const rawBills = await API.fetchAllBills();
    const allBills = getProjectedBills(rawBills);
    const todayStr = new Date().toISOString().slice(0,10);
    const visibleBills = allBills.filter(b => !(b.status === 'UNPAID' && b.due_date < todayStr));
    const filteredBills = filterBillsForDisplay(visibleBills);
    
    state.currentBills = filteredBills;

    Calendar.renderCalendar(filteredBills, (dateStr) => {
      state.selectedDate = dateStr;
      fetchAndRenderBills();
    });

    updateDashboardLists(filteredBills);
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
