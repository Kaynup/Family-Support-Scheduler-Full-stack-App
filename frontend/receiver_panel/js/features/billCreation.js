import * as API from '../core/api.js';
import * as UI from '../components/ui.js';
import * as BillListing from './billListing.js';
import * as Modal from '../components/modal.js';

export async function handleCreateBillSubmit(event) {
  event.preventDefault();
  const formEl = UI.elements.createBillForm;
  const name = formEl.name.value.trim();
  const totalAmount = parseFloat(formEl.total_amount.value);
  const dueDate = formEl.due_date.value;
  const category = formEl.category.value.trim() || null;
  const recurringInterval = formEl.recurring_interval.value;

  if (!name || !dueDate || Number.isNaN(totalAmount) || totalAmount < 0) {
    UI.displayStatusMessage('Please provide valid bill name, amount, and due date.');
    return;
  }

  UI.displayStatusMessage('Creating bill...');
  try {
    await API.createBill({ 
      name, 
      due_date: dueDate, 
      total_amount: totalAmount, 
      category, 
      recurring_interval: recurringInterval 
    });
    UI.displayStatusMessage('Bill created successfully.');
    formEl.reset();
    Modal.handleCloseCreateModal();
    Modal.setDueDateDefaults();
    await BillListing.fetchAndRenderBills();
  } catch (error) {
    UI.displayStatusMessage(`Unable to create bill: ${error.message}`);
    console.error(error);
  }
}
