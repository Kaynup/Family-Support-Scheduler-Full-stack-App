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
  if (sessionStorage.getItem('upcomingModalShown')) return;

  try {
    const upcomingBills = await fetchUpcomingBills(3);
    const { fetchExpiredBills } = await import('./core/api.js');
    const expiredBills = await fetchExpiredBills();

    // Sort upcoming: soonest due at top (ascending)
    const sortedUpcoming = upcomingBills.sort((a, b) => new Date(a.due_date) - new Date(b.due_date));
    // Sort expired: most recent expired at top (descending)
    const sortedExpired = expiredBills.sort((a, b) => new Date(b.due_date) - new Date(a.due_date));

    const allAlertBills = [...sortedUpcoming, ...sortedExpired];

    if (allAlertBills.length > 0) {
      if (UI.elements.upcomingList) {
        UI.elements.upcomingList.innerHTML = '';
        allAlertBills.forEach(bill => {
          const item = document.createElement('tr');
          item.className = 'upcoming-item';
          const isExp = new Date(bill.due_date) < new Date(new Date().toDateString());
          const statusTxt = isExp ? '<span style="color:red;font-weight:bold;">EXPIRED</span>' : 'DUE';
          item.innerHTML = `<td>${bill.name}</td><td>${bill.due_date}</td><td>Rs.${bill.total_amount}</td><td>${statusTxt}</td><td>${bill.recurring_interval}</td>`;
          UI.elements.upcomingList.appendChild(item);
        });
      }
      if (UI.elements.upcomingModal) {
        UI.elements.upcomingModal.classList.remove('hidden');
      }
      sessionStorage.setItem('upcomingModalShown', 'true');
    }
  } catch (error) {
    console.error('Failed to fetch alert bills:', error);
  }
}

function initializeApp() {
  setupGlobalEventListeners();
  if (UI.elements.userInfoEl) {
    const uname = localStorage.getItem('username') || 'Unknown';
    const role = localStorage.getItem('role') || '';
    UI.elements.userInfoEl.textContent = `Logged in as ${uname} (${role})`;
  }
  BillListing.fetchAndRenderBills();
  dueBillsPopUpWindow();
}

initializeApp();
