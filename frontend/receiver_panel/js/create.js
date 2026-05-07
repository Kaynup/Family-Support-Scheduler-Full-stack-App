import { guardRoute } from './core/auth_guard.js';
guardRoute();

import { createBill } from './core/api.js';

document.addEventListener('DOMContentLoaded', () => {
    const today = new Date();
    const defaultDue = new Date(today);
    defaultDue.setDate(defaultDue.getDate() + 3);

    const dueInput = document.getElementById('bill-due');
    if(dueInput) {
        dueInput.min = today.toISOString().slice(0, 10);
        dueInput.value = defaultDue.toISOString().slice(0, 10);
    }
});

document.getElementById('create-bill-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    
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
    
    if (!payload.name) {
        statusEl.textContent = 'Bill name cannot be empty.';
        return;
    }
    
    if (payload.total_amount <= 0) {
        statusEl.textContent = 'Amount must be greater than zero.';
        return;
    }
    
    try {
        await createBill(payload);
        window.location.href = 'bills.html';
    } catch(err) {
        statusEl.textContent = 'Failed to create bill: ' + err.message;
    }
});
