import { guardRoute } from './core/auth_guard.js';
guardRoute();

import * as UI from './components/ui.js';
import * as Modal from './components/modal.js';
import * as Calendar from './components/calendar.js';
import { state } from './core/state.js';
import { fetchAllBills, payBill } from './core/api.js';

async function fetchAndRenderBills() {
    try {
        const bills = await fetchAllBills();
        UI.renderBillTable(UI.elements.billsContainerEl, bills, 'No bills to pay.', handleBillSelect);
        Calendar.renderCalendar(bills, (dateStr) => {
            state.selectedDate = dateStr;
            const filtered = bills.filter(b => b.due_date === dateStr);
            UI.renderBillTable(UI.elements.billsContainerEl, filtered, `No bills on ${dateStr}`, handleBillSelect);
            Calendar.renderCalendar(bills, null); // refresh selection highlight
        });
    } catch(err) {
        UI.displayStatusMessage('Error fetching bills: ' + err.message);
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

function setupGlobalEventListeners() {
    if (UI.elements.prevMonthBtn && UI.elements.nextMonthBtn) {
        UI.elements.prevMonthBtn.addEventListener('click', () => Calendar.handleMonthChange(-1, fetchAndRenderBills));
        UI.elements.nextMonthBtn.addEventListener('click', () => Calendar.handleMonthChange(1, fetchAndRenderBills));
    }
    
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
                fetchAndRenderBills();
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
}

function initializeApp() {
    setupGlobalEventListeners();
    fetchAndRenderBills();
}

initializeApp();
