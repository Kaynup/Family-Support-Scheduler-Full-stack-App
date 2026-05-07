import * as UI from './ui.js';

export function handleOpenDeleteModal() {
  if (UI.elements.deleteModal) {
    UI.elements.deleteModal.classList.remove('hidden');
  }
}

export function handleCloseDeleteModal() {
  if (UI.elements.deleteModal) {
    UI.elements.deleteModal.classList.add('hidden');
  }
}
