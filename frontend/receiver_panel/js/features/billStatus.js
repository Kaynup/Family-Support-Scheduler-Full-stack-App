import * as API from '../core/api.js';
import * as UI from '../components/ui.js';
import { state } from '../core/state.js';
import * as BillListing from './billListing.js';

export async function patchBillStatus(newStatus) {
  if (!state.selectedBill) return;
  
  const isProjected = !!state.selectedBill.isProjected;
  const actionText = isProjected ? 'Creating record for' : 'Updating';
  
  UI.displayStatusMessage(`${actionText} ${state.selectedBill.name}...`);
  
  try {
    if (isProjected) {
      // "Promote" virtual bill to a real database record
      await API.createBill({
        name: state.selectedBill.name,
        due_date: state.selectedBill.due_date,
        total_amount: state.selectedBill.total_amount,
        category: state.selectedBill.category,
        recurring_interval: state.selectedBill.recurring_interval,
        status: newStatus
      });
    } else {
      // Normal update for existing record
      await API.updateBillStatus(state.selectedBill.id, newStatus);
    }
    
    UI.displayStatusMessage(`Bill marked as ${newStatus}.`);
    await BillListing.fetchAndRenderBills();
  } catch (error) {
    UI.displayStatusMessage(`Error: ${error.message}`);
    console.error(error);
  }
}
