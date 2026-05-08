import { guardRoute } from './core/auth_guard.js';
guardRoute();

import * as UI from './components/ui.js';
import { fetchRemittanceHistory } from './core/api.js';

document.addEventListener('DOMContentLoaded', async () => {
    if (document.getElementById('user-info')) {
        const uname = localStorage.getItem('username') || 'Unknown';
        const role = localStorage.getItem('role') || '';
        document.getElementById('user-info').textContent = `Logged in as ${uname} (${role})`;
    }
    
    const listEl = document.getElementById('history-list');
    
    try {
        const data = await fetchRemittanceHistory();
        listEl.innerHTML = '';
        
        if (data.length === 0) {
            listEl.innerHTML = '<tr><td colspan="5" class="bill-empty-note">No payment history available.</td></tr>';
            return;
        }
        
        data.forEach(tx => {
            const row = document.createElement('tr');
            const senderName = tx.other_username || 'Unknown';
            const billName = tx.bill_name || 'Unknown';
            row.innerHTML = `
                <td>#${tx.transaction_id}</td>
                <td>${senderName} - ${billName}</td>
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
