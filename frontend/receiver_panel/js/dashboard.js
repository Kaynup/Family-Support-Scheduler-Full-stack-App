import { guardRoute } from './core/auth_guard.js';
guardRoute();

import * as UI from './components/ui.js';
import * as Modal from './components/modal.js';
import * as Calendar from './components/calendar.js';
import { state } from './core/state.js';

import * as BillListing from './features/billListing.js';
import * as BillStatus from './features/billStatus.js';
import * as BillDeletion from './features/billDeletion.js';
import * as BillSearch from './features/billSearch.js';
import { fetchUpcomingBills } from './core/api.js';
import { fetchExpiredBills } from './core/api.js';
import { setLoggedInUserLabel } from '../../shared/js/ui/session_user.js';
import { showUpcomingAndExpiredBills } from '../../shared/js/ui/upcoming_alerts.js';

function setupGlobalEventListeners() {
  // Mark Paid button removed; marking paid is handled when sender pays.

  if (UI.elements.deleteButton) {
    UI.elements.deleteButton.addEventListener('click', BillDeletion.handleOpenDeleteConfirmation);
    UI.elements.confirmDeleteButton.addEventListener('click', BillDeletion.handleConfirmDelete);
    UI.elements.cancelDeleteButton.addEventListener('click', Modal.handleCloseDeleteModal);
  }

  const refreshBtn = document.getElementById('refresh-btn');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', () => location.reload());
  }

  // Close modals when clicking outside
  window.addEventListener('click', (e) => {
    if (e.target === UI.elements.deleteModal) Modal.handleCloseDeleteModal();
  });

  if (UI.elements.upcomingOkButton) {
    UI.elements.upcomingOkButton.addEventListener('click', () => {
      if (UI.elements.upcomingModal) UI.elements.upcomingModal.classList.add('hidden');
    });
  }

  if (UI.elements.searchButton) {
    UI.elements.searchButton.addEventListener('click', BillSearch.handleSearchSubmit);
  }
  if (UI.elements.searchInput) {
    UI.elements.searchInput.addEventListener('keyup', (e) => {
      if (e.key === 'Enter') BillSearch.handleSearchSubmit();
    });
  }

  if (UI.elements.prevMonthBtn && UI.elements.nextMonthBtn) {
    UI.elements.prevMonthBtn.addEventListener('click', () => Calendar.handleMonthChange(-1, BillListing.fetchAndRenderBills));
    UI.elements.nextMonthBtn.addEventListener('click', () => Calendar.handleMonthChange(1, BillListing.fetchAndRenderBills));
  }
}

async function dueBillsPopUpWindow() {
  try {
    await showUpcomingAndExpiredBills({
      fetchUpcoming: fetchUpcomingBills,
      fetchExpired: fetchExpiredBills,
      listEl: UI.elements.upcomingList,
      modalEl: UI.elements.upcomingModal,
    });
  } catch (error) {
    console.error('Failed to fetch alert bills:', error);
  }
}

function initializeApp() {
  setupGlobalEventListeners();
  setLoggedInUserLabel('user-info');
  BillListing.fetchAndRenderBills();
  dueBillsPopUpWindow();
}

initializeApp();
