import * as API from '../core/api.js';
import * as UI from '../components/ui.js';
import * as BillListing from './billListing.js';

export async function handleSearchSubmit() {
  const query = UI.elements.searchInput.value.trim();
  if (!query) {
    UI.elements.searchResultsContainerEl.textContent = '';
    return;
  }
  UI.displayStatusMessage(`Searching for "${query}"...`);
  try {
    const results = await API.searchBills(query);
    UI.renderBillTable(UI.elements.searchResultsContainerEl, results, 'No matching bills found.', BillListing.handleSelectBill);
    UI.displayStatusMessage(`Found ${results.length} bills matching "${query}".`);
  } catch (error) {
    UI.displayStatusMessage(`Search failed: ${error.message}`);
    console.error(error);
  }
}
