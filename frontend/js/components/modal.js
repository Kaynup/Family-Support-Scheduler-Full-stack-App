import * as UI from './ui.js';

export function handleOpenCreateModal() {
  UI.elements.createModal.classList.remove('hidden');
  setDueDateDefaults();
  UI.elements.createBillForm.name.focus();
}

export function handleCloseCreateModal() {
  UI.elements.createModal.classList.add('hidden');
}

export function handleOpenDeleteModal() {
  UI.elements.deleteModal.classList.remove('hidden');
}

export function handleCloseDeleteModal() {
  UI.elements.deleteModal.classList.add('hidden');
}

export function setDueDateDefaults() {
  if (!UI.elements.dueDateInput) return;

  const today = new Date();
  const defaultDue = new Date(today);
  defaultDue.setDate(defaultDue.getDate() + 3);

  UI.elements.dueDateInput.min = today.toISOString().slice(0, 10);
  UI.elements.dueDateInput.value = defaultDue.toISOString().slice(0, 10);
}
