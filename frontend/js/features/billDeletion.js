import * as api from '../core/api.js';
import * as ui from '../components/ui.js';
import { state } from '../core/state.js';
import { fetchBills } from './billListing.js';
import { openDeleteModal, closeDeleteModal } from '../components/modal.js';

export function openDeleteConfirmation() {
  if (!state.selectedBill) return;
  const textEl = document.getElementById('delete-confirm-text');
  if (textEl) {
    textEl.textContent = `Are you sure you want to delete "${state.selectedBill.name}"?`;
  }
  openDeleteModal();
}

export async function handleConfirmDelete() {
  if (!state.selectedBill) return;
  ui.showStatus(`Deleting ${state.selectedBill.name}...`);
  try {
    await api.deleteBillById(state.selectedBill.id);
    closeDeleteModal();
    await fetchBills();
  } catch (error) {
    ui.showStatus('Unable to delete bill.');
    console.error(error);
  }
}
