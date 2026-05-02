import * as api from '../core/api.js';
import * as ui from '../components/ui.js';
import { fetchBills } from './billListing.js';
import { closeCreateModal, setDueDateDefaults } from '../components/modal.js';

export async function createBill(event) {
  event.preventDefault();
  const form = ui.elements.createBillForm;
  const name = form.name.value.trim();
  const total_amount = parseFloat(form.total_amount.value);
  const due_date = form.due_date.value;
  const category = form.category.value.trim() || null;
  const recurring_interval = form.recurring_interval.value;

  if (!name || !due_date || Number.isNaN(total_amount) || total_amount < 0) {
    ui.showStatus('Please provide valid bill name, amount, and due date.');
    return;
  }

  ui.showStatus('Creating bill...');
  try {
    await api.createBill({ name, due_date, total_amount, category, recurring_interval });
    ui.showStatus('Bill created successfully.');
    form.reset();
    closeCreateModal();
    setDueDateDefaults();
    await fetchBills();
  } catch (error) {
    ui.showStatus(`Unable to create bill: ${error.message}`);
    console.error(error);
  }
}
