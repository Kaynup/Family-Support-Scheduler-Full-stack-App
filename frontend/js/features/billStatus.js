import * as api from '../core/api.js';
import * as ui from '../components/ui.js';
import { state } from '../core/state.js';
import { fetchBills } from './billListing.js';

export async function patchBill(status) {
  if (!state.selectedBill) return;
  ui.showStatus(`Updating ${state.selectedBill.name}...`);
  try {
    await api.updateBillStatus(state.selectedBill.id, status);
    state.selectedBill.status = status;
    ui.showStatus(`Bill updated to ${status}.`);
    await fetchBills();
  } catch (error) {
    ui.showStatus('Unable to update bill.');
    console.error(error);
  }
}
