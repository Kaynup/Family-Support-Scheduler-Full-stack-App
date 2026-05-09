# Variables & Functions (Frontend)

The frontend JavaScript relies heavily on decoupled rendering functions and a global state object.

## State Variables (in `state.js`)
- **`state.selectedBill`**: Holds the JSON object of the currently clicked bill row.
- **`state.selectedDate`**: A string (e.g., `'2026-05-09'`) representing the user's active calendar selection.
- **`state.currentBills`**: A cached array of real `UNPAID` bills fetched from the API.

## Critical Functions

### `core/utils.js`
- **`filterBillsForDisplay(bills)`**:
  Strips out `PAID` bills from the dataset so list tables only render active obligations.
- **`getProjectedBills(bills, projectionCount = 12)`**:
  The **Projection Engine**. It iterates through recurring active bills and mathematically generates virtual objects for the next 12 intervals (setting `isProjected = true` on the output). Used exclusively to render recurring dots on the `Calendar`.

### `dashboard.js`
- **`fetchAndRenderBills()`**:
  The primary boot function. It fetches data via `api.js`, filters for real bills to render the `ui.js` tables, and feeds the entire set (with projections) to `calendar.js`.
- **`dueBillsPopUpWindow()`**:
  Executes on page load. Combines asynchronous calls to `fetchUpcomingBills()` and `fetchExpiredBills()`, merges them, and renders a localized modal table warning the user of immediate obligations.

### `components/ui.js`
- **`renderBillTable(containerEl, billsList, emptyMessage, onSelectBill)`**:
  Dynamically generates `<table>`, `<thead>`, and `<tbody>` elements. Generates strict columns: `Name`, `Category`, `Amount`, `Due Date`, and `Recurring`.
- **`clearSelectionHighlights()`**:
  Iterates over the DOM and strips `.selected` classes from all rows when state resets.
