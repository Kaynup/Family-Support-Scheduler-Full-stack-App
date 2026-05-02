import * as ui from './components/ui.js';
import * as modal from './components/modal.js';
import * as calendar from './components/calendar.js';
import { state } from './core/state.js';

import { fetchBills } from './features/billListing.js';
import { patchBill } from './features/billStatus.js';
import { openDeleteConfirmation, handleConfirmDelete } from './features/billDeletion.js';
import { createBill } from './features/billCreation.js';
import { handleSearch } from './features/billSearch.js';

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
