import { elements } from './ui.js';

export function openCreateModal() {
  elements.createModal.classList.remove('hidden');
  setDueDateDefaults();
  elements.createBillForm.name.focus();
}

export function closeCreateModal() {
  elements.createModal.classList.add('hidden');
}

export function openDeleteModal() {
  elements.deleteModal.classList.remove('hidden');
}

export function closeDeleteModal() {
  elements.deleteModal.classList.add('hidden');
}

export function setDueDateDefaults() {
  if (!elements.dueDateInput) return;

  const today = new Date();
  const defaultDue = new Date(today);
  defaultDue.setDate(defaultDue.getDate() + 3);

  elements.dueDateInput.min = today.toISOString().slice(0, 10);
  elements.dueDateInput.value = defaultDue.toISOString().slice(0, 10);
}
