import { guardRoute } from './core/auth_guard.js';
guardRoute();

import { fetchRemittanceHistory } from './core/api.js';

document.addEventListener('DOMContentLoaded', async () => {
    const listEl = document.getElementById('history-list');
    
    try {
        const data = await fetchRemittanceHistory();
        listEl.innerHTML = '';
        
        if (data.length === 0) {
            listEl.innerHTML = '<tr><td colspan="5" class="bill-empty-note">No outgoing payments found.</td></tr>';
            return;
        }
        
        data.forEach(tx => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>#${tx.transaction_id}</td>
                <td>Bill ${tx.bill_id}</td>
                <td>${tx.currency} ${tx.amount}</td>
                <td><span class="status-badge status-${tx.transaction_status.toLowerCase()}" style="background-color: #10b981; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.8rem;">${tx.transaction_status}</span></td>
                <td>${new Date(tx.created_at).toLocaleString()}</td>
            `;
            listEl.appendChild(row);
        });
    } catch(err) {
        listEl.innerHTML = `<tr><td colspan="5" class="bill-empty-note" style="color:red;">Error loading history: ${err.message}</td></tr>`;
    }
});
