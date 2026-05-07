import * as UI from './ui.js';

export function handleOpenPayModal() {
  if (UI.elements.payModal) {
    UI.elements.payModal.classList.remove('hidden');
  }
}

export function handleClosePayModal() {
  if (UI.elements.payModal) {
    UI.elements.payModal.classList.add('hidden');
  }
}
