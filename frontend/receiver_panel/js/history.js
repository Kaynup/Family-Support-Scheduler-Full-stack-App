import { guardRoute } from './core/auth_guard.js';
guardRoute();

import * as UI from './components/ui.js';

document.addEventListener('DOMContentLoaded', async () => {
    const listEl = document.getElementById('history-list');
    
    // Note: Backend currently only supports sender history endpoint.
    // For receiver, we display a placeholder or empty list.
    try {
        // const data = await requestJson('/remittance/history');
        const data = []; // placeholder
        listEl.innerHTML = '';
        
        if (data.length === 0) {
            listEl.innerHTML = '<tr><td colspan="5" class="bill-empty-note">No payment history available for your bills.</td></tr>';
            return;
        }
        
        data.forEach(tx => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>#${tx.transaction_id}</td>
                <td>Bill ${tx.bill_id}</td>
                <td>${tx.currency} ${tx.amount}</td>
                <td><span class="status-badge status-${tx.transaction_status.toLowerCase()}">${tx.transaction_status}</span></td>
                <td>${new Date(tx.created_at).toLocaleString()}</td>
            `;
            listEl.appendChild(row);
        });
    } catch(err) {
        listEl.innerHTML = `<tr><td colspan="5" class="bill-empty-note" style="color:red;">Error loading history</td></tr>`;
    }
});
