import { guardRoute } from './core/auth_guard.js';
guardRoute();

import * as UI from './components/ui.js';
import * as Modal from './components/modal.js';
import * as Calendar from './components/calendar.js';
import { state } from './core/state.js';
import { fetchAllBills, payBill, fetchUpcomingBills, fetchUsers, fetchAllBillsForBeneficiary } from './core/api.js';
import { getProjectedBills, filterBillsForDisplay } from './core/utils.js';

// Track the currently selected beneficiary for refresh functionality
let currentBeneficiaryId = null;

async function fetchAndRenderBills() {
    try {
        const bills = await fetchAllBills();
        const allBills = getProjectedBills(bills);
        const todayStr = new Date().toISOString().slice(0,10);
        const visible = allBills.filter(b => !(b.status === 'UNPAID' && b.due_date < todayStr));
        const filtered = filterBillsForDisplay(visible);

        UI.renderBillTable(UI.elements.billsContainerEl, filtered, 'No bills to pay.', handleBillSelect);

        const handleCalendarClick = (dateStr) => {
            state.selectedDate = dateStr;
            const dateFiltered = filtered.filter(b => b.due_date === dateStr);
            UI.renderBillTable(UI.elements.billsContainerEl, dateFiltered, `No bills on ${dateStr}`, handleBillSelect);
            Calendar.renderCalendar(filtered, handleCalendarClick); // refresh selection highlight with handler
        };

        Calendar.renderCalendar(filtered, handleCalendarClick);
    } catch(err) {
        UI.displayStatusMessage('Error fetching bills: ' + err.message);
    }
}

async function fetchAndRenderBillsForBeneficiary(beneficiaryId) {
    try {
        const bills = await fetchAllBillsForBeneficiary(beneficiaryId);
        const allBills = getProjectedBills(bills);
        const todayStr = new Date().toISOString().slice(0,10);
        const visible = allBills.filter(b => !(b.is_expired === 'Y' || (b.status === 'UNPAID' && b.due_date < todayStr)));
        const filtered = filterBillsForDisplay(visible);
        UI.renderBillTable(UI.elements.billsContainerEl, filtered, 'No bills to pay.', handleBillSelect);
        const handleCalendarClick = (dateStr) => {
            state.selectedDate = dateStr;
            const dateFiltered = filtered.filter(b => b.due_date === dateStr);
            UI.renderBillTable(UI.elements.billsContainerEl, dateFiltered, `No bills on ${dateStr}`, handleBillSelect);
            Calendar.renderCalendar(filtered, handleCalendarClick);
        };
        Calendar.renderCalendar(filtered, handleCalendarClick);
    } catch(err) {
        UI.displayStatusMessage('Error fetching bills: ' + err.message);
    }
}

async function refreshCurrentView() {
    if (currentBeneficiaryId === null) {
        await fetchAndRenderBills();
    } else {
        await fetchAndRenderBillsForBeneficiary(currentBeneficiaryId);
    }
}

async function loadBeneficiaries() {
    try {
        const users = await fetchUsers('beneficiary');
        const container = document.getElementById('beneficiary-filter');
        if (!container) return;
        container.innerHTML = '';

        const allBtn = document.createElement('button');
        allBtn.textContent = 'All Beneficiaries';
        allBtn.className = 'tab-btn active';
        allBtn.addEventListener('click', async () => {
            document.querySelectorAll('#beneficiary-filter .tab-btn').forEach(b => b.classList.remove('active'));
            allBtn.classList.add('active');
            currentBeneficiaryId = null;
            fetchAndRenderBills();
        });
        container.appendChild(allBtn);

        users.forEach(u => {
            const btn = document.createElement('button');
            btn.textContent = u.username;
            btn.className = 'tab-btn';
            btn.addEventListener('click', async () => {
                document.querySelectorAll('#beneficiary-filter .tab-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentBeneficiaryId = u.id;
                fetchAndRenderBillsForBeneficiary(u.id);
            });
            container.appendChild(btn);
        });
    } catch (err) {
        console.error('Failed to load beneficiaries:', err);
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
        UI.elements.prevMonthBtn.addEventListener('click', () => Calendar.handleMonthChange(-1, refreshCurrentView));
        UI.elements.nextMonthBtn.addEventListener('click', () => Calendar.handleMonthChange(1, refreshCurrentView));
    }
    
    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', refreshCurrentView);
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
}

async function dueBillsPopUpWindow() {
    if (sessionStorage.getItem('upcomingModalShown')) return;
    try {
        const upcomingBills = await fetchUpcomingBills(3);
        if (upcomingBills.length > 0) {
            if(UI.elements.upcomingList) {
                UI.elements.upcomingList.innerHTML = '';
                upcomingBills.forEach(bill => {
                    const item = document.createElement('tr');
                    item.className = 'upcoming-item';
                    item.innerHTML = `<td>${bill.name}</td><td>${bill.due_date}</td><td>Rs.${bill.total_amount}</td>`;
                    UI.elements.upcomingList.appendChild(item);
                });
            }
            if(UI.elements.upcomingModal) {
                UI.elements.upcomingModal.classList.remove('hidden');
            }
            sessionStorage.setItem('upcomingModalShown', 'true');
        }
    } catch (error) {
        console.error('Failed to fetch upcoming bills:', error);
    }
}

function initializeApp() {
    setupGlobalEventListeners();
        if (UI.elements.userInfoEl) {
            const uname = localStorage.getItem('username') || 'Unknown';
            const role = localStorage.getItem('role') || '';
            UI.elements.userInfoEl.textContent = `Logged in as ${uname} (${role})`;
        }
        loadBeneficiaries();
        fetchAndRenderBills();
        dueBillsPopUpWindow();
}

initializeApp();
