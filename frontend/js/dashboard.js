import * as UI from './components/ui.js';
import * as Modal from './components/modal.js';
import * as Calendar from './components/calendar.js';
import { state } from './core/state.js';

import * as BillListing from './features/billListing.js';
import * as BillStatus from './features/billStatus.js';
import * as BillDeletion from './features/billDeletion.js';
import * as BillCreation from './features/billCreation.js';
import * as BillSearch from './features/billSearch.js';
import { fetchUpcomingBills } from './core/api.js';

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
    // if (e.target === UI.elements.upcomingModal) UI.elements.upcomingModal.classList.add('hidden');
  });

  UI.elements.upcomingOkButton.addEventListener('click', () => UI.elements.upcomingModal.classList.add('hidden'));

  UI.elements.searchButton.addEventListener('click', BillSearch.handleSearchSubmit);
  UI.elements.searchInput.addEventListener('keyup', (e) => {
    if (e.key === 'Enter') BillSearch.handleSearchSubmit();
  });

  UI.elements.prevMonthBtn.addEventListener('click', () => Calendar.handleMonthChange(-1, BillListing.fetchAndRenderBills));
  UI.elements.nextMonthBtn.addEventListener('click', () => Calendar.handleMonthChange(1, BillListing.fetchAndRenderBills));
}

async function dueBillsPopUpWindow() {
  if (sessionStorage.getItem('upcomingModalShown')) return;

  try {
    const upcomingBills = await fetchUpcomingBills(3);
    if (upcomingBills.length > 0) {
      UI.elements.upcomingList.innerHTML = '';
      upcomingBills.forEach(bill => {
        const item = document.createElement('tr');
        item.className = 'upcoming-item';
        item.innerHTML = `<td>${bill.name}</td><td>${bill.due_date}</td><td>Rs.${bill.total_amount}</td>`;
        UI.elements.upcomingList.appendChild(item);
      });
      UI.elements.upcomingModal.classList.remove('hidden');

      sessionStorage.setItem('upcomingModalShown', 'true');
    }

  } catch (error) {
    console.error('Failed to fetch upcoming bills:', error);
  }
}

function initializeApp() {
  Modal.setDueDateDefaults();
  setupGlobalEventListeners();
  BillListing.fetchAndRenderBills();
  dueBillsPopUpWindow();
}

initializeApp();
