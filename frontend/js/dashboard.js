import * as UI from './components/ui.js';
import * as Modal from './components/modal.js';
import * as Calendar from './components/calendar.js';
import { state } from './core/state.js';

import * as BillListing from './features/billListing.js';
import * as BillStatus from './features/billStatus.js';
import * as BillDeletion from './features/billDeletion.js';
import * as BillCreation from './features/billCreation.js';
import * as BillSearch from './features/billSearch.js';

function setupGlobalEventListeners() {
  UI.elements.markPaidButton.addEventListener('click', () => {
    if (!state.selectedBill) {
      UI.displayStatusMessage('Please select a bill from the list first!')
      return;
    }
    const nextStatus = state.selectedBill.status === 'PAID' ? 'UNPAID' : 'PAID';
    BillStatus.patchBillStatus(nextStatus);
  });

  UI.elements.deleteButton.addEventListener('click', BillDeletion.handleOpenDeleteConfirmation);
  UI.elements.confirmDeleteButton.addEventListener('click', BillDeletion.handleConfirmDelete);
  UI.elements.cancelDeleteButton.addEventListener('click', Modal.handleCloseDeleteModal);

  UI.elements.createBillForm.addEventListener('submit', BillCreation.handleCreateBillSubmit);
  UI.elements.closeCreateModalButton.addEventListener('click', Modal.handleCloseCreateModal);

  // Close modals when clicking outside
  window.addEventListener('click', (e) => {
    if (e.target === UI.elements.createModal) Modal.handleCloseCreateModal();
    if (e.target === UI.elements.deleteModal) Modal.handleCloseDeleteModal();
  });

  UI.elements.searchButton.addEventListener('click', BillSearch.handleSearchSubmit);
  UI.elements.searchInput.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') BillSearch.handleSearchSubmit();
  });

  UI.elements.prevMonthBtn.addEventListener('click', () => Calendar.handleMonthChange(-1, BillListing.fetchAndRenderBills));
  UI.elements.nextMonthBtn.addEventListener('click', () => Calendar.handleMonthChange(1, BillListing.fetchAndRenderBills));
}

function initializeApp() {
  Modal.setDueDateDefaults();
  setupGlobalEventListeners();
  BillListing.fetchAndRenderBills();
}

initializeApp();
