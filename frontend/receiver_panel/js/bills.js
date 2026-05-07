import { guardRoute } from './core/auth_guard.js';
guardRoute();

import * as UI from './components/ui.js';
import * as Modal from './components/modal.js';
import { state } from './core/state.js';
import { fetchAllBills } from './core/api.js';

import * as BillStatus from './features/billStatus.js';
import * as BillDeletion from './features/billDeletion.js';
import * as BillSearch from './features/billSearch.js';

async function fetchAndRenderAllBills() {
  try {
    const data = await fetchAllBills();
    UI.renderBillTable(UI.elements.billsContainerEl, data, 'No bills found.', handleBillSelect);
  } catch (error) {
    UI.displayStatusMessage('Error fetching bills: ' + error.message);
  }
}

function handleBillSelect(bill, rowElement) {
  UI.clearSelectionHighlights();
  rowElement.classList.add('selected');
  state.selectedBill = bill;

  UI.renderSelectedBillSummary(bill);

  UI.elements.markPaidButton.disabled = false;
  UI.elements.markPaidButton.textContent = bill.status === 'PAID' ? 'Mark UNPAID' : 'Mark PAID';
  UI.elements.deleteButton.disabled = false;
}

function setupEventListeners() {
  if (UI.elements.markPaidButton) {
    UI.elements.markPaidButton.addEventListener('click', () => {
      if (!state.selectedBill) {
        UI.displayStatusMessage('Please select a bill from the list first!')
        return;
      }
      const nextStatus = state.selectedBill.status === 'PAID' ? 'UNPAID' : 'PAID';
      BillStatus.patchBillStatus(nextStatus).then(fetchAndRenderAllBills);
    });
  }

  if (UI.elements.deleteButton) {
    UI.elements.deleteButton.addEventListener('click', BillDeletion.handleOpenDeleteConfirmation);
    UI.elements.confirmDeleteButton.addEventListener('click', () => {
        BillDeletion.handleConfirmDelete().then(fetchAndRenderAllBills);
    });
    UI.elements.cancelDeleteButton.addEventListener('click', Modal.handleCloseDeleteModal);
  }

  window.addEventListener('click', (e) => {
    if (e.target === UI.elements.deleteModal) Modal.handleCloseDeleteModal();
  });

  if (UI.elements.searchButton) {
    UI.elements.searchButton.addEventListener('click', BillSearch.handleSearchSubmit);
  }
  if (UI.elements.searchInput) {
    UI.elements.searchInput.addEventListener('keyup', (e) => {
      if (e.key === 'Enter') BillSearch.handleSearchSubmit();
    });
  }
}

function init() {
  setupEventListeners();
  fetchAndRenderAllBills();
}

init();
