import { guardRoute } from './core/auth_guard.js';
guardRoute();

import * as UI from './components/ui.js';
import * as Modal from './components/modal.js';
import { state } from './core/state.js';
import { fetchAllBills, payBill, searchBills } from './core/api.js';

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

  if (bill.status === 'UNPAID') {
      UI.elements.payButton.disabled = false;
  } else {
      UI.elements.payButton.disabled = true;
  }
}

function setupEventListeners() {
    if (UI.elements.payButton) {
        UI.elements.payButton.addEventListener('click', () => {
            if (!state.selectedBill) return;
            const textEl = document.getElementById('pay-confirm-text');
            textEl.textContent = `Pay Rs.${state.selectedBill.total_amount} for ${state.selectedBill.name}?`;
            Modal.handleOpenPayModal();
        });
    }
    
    if (UI.elements.cancelPayButton) {
        UI.elements.cancelPayButton.addEventListener('click', Modal.handleClosePayModal);
    }
    
    if (UI.elements.confirmPayButton) {
        UI.elements.confirmPayButton.addEventListener('click', async () => {
            if (!state.selectedBill) return;
            try {
                UI.elements.confirmPayButton.disabled = true;
                UI.elements.confirmPayButton.textContent = 'Processing...';
                
                await payBill(state.selectedBill.id, state.selectedBill.total_amount);
                
                UI.displayStatusMessage('Payment processed successfully!');
                Modal.handleClosePayModal();
                fetchAndRenderAllBills();
                UI.clearSelectionHighlights();
                state.selectedBill = null;
                UI.renderSelectedBillSummary({name: 'Select a bill to see actions.'});
            } catch(err) {
                alert('Payment failed: ' + err.message);
            } finally {
                UI.elements.confirmPayButton.disabled = false;
                UI.elements.confirmPayButton.textContent = 'Pay Now';
            }
        });
    }
    
    window.addEventListener('click', (e) => {
        if (e.target === UI.elements.payModal) Modal.handleClosePayModal();
    });

    if (UI.elements.searchButton) {
        UI.elements.searchButton.addEventListener('click', async () => {
            const query = UI.elements.searchInput.value.trim();
            if (!query) return fetchAndRenderAllBills();
            try {
                const data = await searchBills(query);
                UI.renderBillTable(UI.elements.billsContainerEl, data, 'No matches found.', handleBillSelect);
            } catch(err) {
                UI.displayStatusMessage('Search failed: ' + err.message);
            }
        });
    }
}

function init() {
  setupEventListeners();
  fetchAndRenderAllBills();
}

init();
