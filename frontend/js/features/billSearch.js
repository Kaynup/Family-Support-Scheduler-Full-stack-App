import * as api from '../core/api.js';
import * as ui from '../components/ui.js';
import { selectBill } from './billListing.js';

export async function handleSearch() {
  const query = ui.elements.searchInput.value.trim();
  if (!query) {
    ui.elements.searchResultsEl.textContent = '';
    return;
  }
  ui.showStatus(`Searching for "${query}"...`);
  try {
    const results = await api.searchBills(query);
    ui.renderList(ui.elements.searchResultsEl, results, 'No matching bills found.', selectBill);
    ui.showStatus(`Found ${results.length} bills matching "${query}".`);
  } catch (error) {
    ui.showStatus(`Search failed: ${error.message}`);
    console.error(error);
  }
}
