import * as API from '../core/api.js';
import * as UI from '../components/ui.js';
import * as BillListing from './billListing.js';
import * as Calendar from '../components/calendar.js';
import { state } from '../core/state.js';
import { filterBillsForDisplay } from '../core/utils.js';

export async function handleSearchSubmit() {
  const query = UI.elements.searchInput.value.trim();
  if (!query) {
    UI.elements.searchResultsContainerEl.textContent = '';
    return;
  }
  UI.displayStatusMessage(`Searching for "${query}"...`);
  try {
    const results = await API.searchBills(query);
    const filtered = filterBillsForDisplay(results);
    
    const handleSearchResultSelect = (bill, rowEl) => {
      BillListing.handleSelectBill(bill, rowEl);
      // Update calendar to show glow on this bill's due date
      state.selectedDate = bill.due_date;
      const visibleBills = state.currentBills || [];
      Calendar.renderCalendar(visibleBills, (dateStr) => {
        state.selectedDate = dateStr;
        BillListing.fetchAndRenderBills();
      });
    };
    
    UI.renderBillTable(UI.elements.searchResultsContainerEl, filtered, 'No matching bills found.', handleSearchResultSelect);
    UI.displayStatusMessage(`Found ${filtered.length} bills matching "${query}".`);
  } catch (error) {
    UI.displayStatusMessage(`Search failed: ${error.message}`);
    console.error(error);
  }
}
