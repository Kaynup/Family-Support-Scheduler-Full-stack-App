import { guardRoute } from './core/auth_guard.js';
guardRoute();

import * as UI from './components/ui.js';
import * as Modal from './components/modal.js';
import { state } from './core/state.js';
import { fetchAllBills, payBill, searchBills } from './core/api.js';
import { getProjectedBills, filterBillsForDisplay } from './core/utils.js';

export async function fetchAndRenderBills() {
    try {
        const bills = await fetchAllBills();
        const realUnpaidBills = bills.filter(b => b.status === 'UNPAID');

        UI.renderBillTable(UI.elements.billsContainerEl, realUnpaidBills, 'No bills to pay.', handleBillSelect);
        
        if (state.newCreatedBill) {
            const row = document.querySelector(`tr[data-bill-id="${state.newCreatedBill.id}"]`);
            if (row) handleBillSelect(state.newCreatedBill, row);
            state.newCreatedBill = null;
        }
    } catch(err) {
        UI.displayStatusMessage('Error fetching bills: ' + err.message);
    }
}

function handleBillSelect(bill, rowElement) {
    UI.clearSelectionHighlights();
    rowElement.classList.add('selected');
    state.selectedBill = bill;

    UI.renderSelectedBillSummary(bill);

    const isProjected = !!bill.isProjected;
    if (bill.status === 'UNPAID' && !isProjected) {
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
            textEl.textContent = `Pay Rem.${state.selectedBill.total_amount} for ${state.selectedBill.name}?`;
            Modal.handleOpenPayModal();
        });
    }

    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', fetchAndRenderAllBills);
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
                UI.renderSelectedBillSummary({ name: 'Select a bill to see actions.' });
            } catch (err) {
                UI.displayStatusMessage('Payment failed: ' + err.message);
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
                const filtered = filterBillsForDisplay(data);
                const nonProjectedFiltered = filtered.filter(b => !b.isProjected);
                UI.renderBillTable(UI.elements.billsContainerEl, nonProjectedFiltered, 'No matches found.', handleBillSelect);
            } catch (err) {
                UI.displayStatusMessage('Search failed: ' + err.message);
            }
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
