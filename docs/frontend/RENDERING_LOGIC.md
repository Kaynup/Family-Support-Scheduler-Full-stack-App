# Rendering Logic

The frontend follows a clean event-driven rendering cycle using per-page entry scripts:

1. **Initialization (`<page>.js`)**:
   - `guardRoute()` is called immediately to verify authentication.
   - The DOMContentLoaded event or direct invocation triggers `initializeApp()`.
   - Data is fetched via `api.js`.
   - Event listeners are bound to static DOM elements defined in `ui.js`.

2. **State Management (`state.js`)**:
   - Holds shared UI state such as the currently selected bill, the active month for the calendar, and the user's role/token context.

3. **Rendering (`ui.js` & `calendar.js`)**:
   - Data is passed into pure rendering functions.
   - The DOM is mutated directly using Vanilla JS (`document.createElement`, `innerHTML`).
   - Dynamic elements (like table rows) have their event listeners attached at the time of creation inside `renderBillRowsHTML`.

This pattern ensures that memory leaks are avoided and event listeners are not accidentally duplicated.
