import { guardRoute } from './core/auth_guard.js';
guardRoute();

import * as UI from './components/ui.js';
import * as Modal from './components/modal.js';
import { state } from './core/state.js';
import { fetchAllBills } from './core/api.js';
import { getProjectedBills, filterBillsForDisplay } from './core/utils.js';

import * as BillStatus from './features/billStatus.js';
import * as BillDeletion from './features/billDeletion.js';
import * as BillSearch from './features/billSearch.js';

async function fetchAndRenderAllBills() {
  try {
    const rawBills = await fetchAllBills();
    const realUnpaidBills = rawBills.filter(b => b.status === 'UNPAID');

    UI.renderBillTable(UI.elements.billsContainerEl, realUnpaidBills, 'No bills found.', handleBillSelect);
    
    // If a new bill was created, select it after rendering
    if (state.newCreatedBill) {
      // Use setTimeout to ensure DOM is updated before querying
      setTimeout(() => {
        const newBillRow = document.querySelector(`tr[data-bill-id="${state.newCreatedBill.id}"]`);
        if (newBillRow) {
          handleBillSelect(state.newCreatedBill, newBillRow);
        }
        state.newCreatedBill = null; // Clear the temporary state
      }, 100);
    }
  } catch (error) {
    UI.displayStatusMessage('Error fetching bills: ' + error.message);
  }
}

function handleBillSelect(bill, rowElement) {
  UI.clearSelectionHighlights();
  rowElement.classList.add('selected');
  state.selectedBill = bill;

  UI.renderSelectedBillSummary(bill);
  UI.displayStatusMessage(`Selected: ${bill.name}.`);
  UI.elements.deleteButton.disabled = false;
}

function setupEventListeners() {
  // Mark Paid control removed; status will be updated when pay occurs.

  if (UI.elements.deleteButton) {
    UI.elements.deleteButton.addEventListener('click', BillDeletion.handleOpenDeleteConfirmation);
    UI.elements.confirmDeleteButton.addEventListener('click', () => {
        BillDeletion.handleConfirmDelete().then(fetchAndRenderAllBills);
    });
    UI.elements.cancelDeleteButton.addEventListener('click', Modal.handleCloseDeleteModal);
  }

  const refreshBtn = document.getElementById('refresh-btn');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', fetchAndRenderAllBills);
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
  if (UI.elements.userInfoEl) {
    const uname = localStorage.getItem('username') || 'Unknown';
    const role = localStorage.getItem('role') || '';
    UI.elements.userInfoEl.textContent = `Logged in as ${uname} (${role})`;
  }
  fetchAndRenderAllBills();
}

init();
