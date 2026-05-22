import { guardRoute } from './core/auth_guard.js';
guardRoute();

import { fetchRemittanceHistory } from './core/api.js';
import { setLoggedInUserLabel } from '../../shared/js/ui/session_user.js';
import { renderRemittanceHistoryRows, renderRemittanceHistoryError } from '../../shared/js/ui/remittance_history.js';

document.addEventListener('DOMContentLoaded', async () => {
    setLoggedInUserLabel('user-info');
    
    const listEl = document.getElementById('history-list');
    
    try {
        const data = await fetchRemittanceHistory();
        renderRemittanceHistoryRows(listEl, data, {
            emptyMessage: 'No payment history available.',
        });
    } catch(err) {
        renderRemittanceHistoryError(listEl, err.message);
    }
});
