import * as API from '../core/api.js';
import * as UI from '../components/ui.js';
import { state } from '../core/state.js';
import * as BillListing from './billListing.js';
import * as Modal from '../components/modal.js';

export function handleOpenDeleteConfirmation() {
  if (!state.selectedBill) return;
  const confirmTextEl = document.getElementById('delete-confirm-text');
  if (confirmTextEl) {
    confirmTextEl.textContent = `Are you sure you want to delete "${state.selectedBill.name}"?`;
  }
  Modal.handleOpenDeleteModal();
}

export async function handleConfirmDelete() {
  if (!state.selectedBill) return;
  UI.displayStatusMessage(`Deleting ${state.selectedBill.name}...`);
  try {
    await API.deleteBillById(state.selectedBill.id);
    Modal.handleCloseDeleteModal();
    await BillListing.fetchAndRenderBills();
  } catch (error) {
    UI.displayStatusMessage('Unable to delete bill.');
    console.error(error);
  }
}
