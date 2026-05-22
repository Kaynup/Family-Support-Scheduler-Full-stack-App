import { guardRoute } from './core/auth_guard.js';
guardRoute();

import { createBill } from './core/api.js';
import { state } from './core/state.js';
import { setLoggedInUserLabel } from '../../shared/js/ui/session_user.js';

document.addEventListener('DOMContentLoaded', () => {
    setLoggedInUserLabel('user-info');

    const today = new Date();
    const defaultDue = new Date(today);
    defaultDue.setDate(defaultDue.getDate() + 3);

    const dueInput = document.getElementById('bill-due');
    if(dueInput) {
        dueInput.min = today.toISOString().slice(0, 10);
        dueInput.value = defaultDue.toISOString().slice(0, 10);
    }

    // Handle success modal OK button
    const successOkBtn = document.getElementById('success-ok-btn');
    if (successOkBtn) {
        successOkBtn.addEventListener('click', () => {
            window.location.href = 'bills.html';
        });
    }

    const form = document.getElementById('create-bill-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            console.log('Bill creation started...');
            
            const statusEl = document.getElementById('status');
            statusEl.textContent = 'Creating...';
            
            const payload = {
                name: form.name.value.trim(),
                due_date: form.due_date.value,
                total_amount: parseFloat(form.total_amount.value),
                category: form.category.value.trim() || null,
                recurring_interval: form.recurring_interval.value,
                status: 'UNPAID',
                creation_date: new Date().toISOString().slice(0, 10)
            };
            
            console.log('Payload:', payload);
            
            if (!payload.name) {
                statusEl.textContent = 'Bill name cannot be empty.';
                return;
            }
            
            if (isNaN(payload.total_amount) || payload.total_amount <= 0) {
                statusEl.textContent = 'Amount must be a valid number greater than zero.';
                return;
            }
            
            try {
                const response = await createBill(payload);
                console.log('Backend response:', response);
                
                // Store the created bill in state (Note: this is lost on redirect, but kept for logic consistency)
                if (response && response.data) {
                    state.newCreatedBill = response.data;
                }
                
                // Show success modal
                const successModal = document.getElementById('success-modal');
                if (successModal) {
                    successModal.classList.remove('hidden');
                } else {
                    alert('Bill created successfully!');
                    window.location.href = 'bills.html';
                }
            } catch(err) {
                console.error('Creation error:', err);
                statusEl.textContent = 'Failed to create bill: ' + err.message;
            }
        });
    } else {
        console.error('Form "create-bill-form" not found!');
    }
});
