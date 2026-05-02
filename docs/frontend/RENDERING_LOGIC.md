# Rendering Logic and Data Flow

This document covers the complete data lifecycle from API fetch to
pixel rendering, including the projection engine, calendar coloring
algorithm, and event handling architecture.

---

## 1. Application Initialization

When dashboard.html loads, the browser executes js/dashboard.js as
an ES6 module. The module's init() function runs immediately:

    1. modal.setDueDateDefaults() -- sets the create form's date constraints.
    2. setupEventListeners() -- wires all click/keyup handlers.
    3. fetchBills() -- triggers the first data load.

The init() call is at module scope (not inside DOMContentLoaded) because
the script tag has `type="module"`, which defers execution until after
the DOM is fully parsed. This is a deliberate choice -- module scripts
are deferred by default in all modern browsers.

---

## 2. The fetchBills() Cycle

This is the central data flow function. Every user action that changes
data (creating, updating, deleting, changing month, selecting a date)
ultimately calls fetchBills() to refresh the UI.

The cycle proceeds as follows:

    Step 1: Reset UI
        - Show "Loading bills..." in the status bar.
        - Clear both bill list containers (due and paid).
        - Reset the selected bill text to the default prompt.
        - Set state.selectedBill to null.
        - Disable both action buttons (Mark PAID, Delete).

    Step 2: Fetch Data
        - Call api.fetchAllBills() which sends GET /bills/all to the backend.
        - The backend returns all non-deleted bills from the database.
        - The API client extracts the .data array from the response.

    Step 3: Project Recurring Bills
        - Pass the raw bills array through getProjectedBills().
        - This function serves as the **sole source of truth** for 
          recurring bill forecasting. It generates virtual future 
          instances for every recurring bill (WEEKLY or MONTHLY) 
          up to the specified projection count.
        - The result is a combined array of real and projected bills.

    Step 4: Render Calendar
        - Pass the combined array to calendar.renderCalendar().
        - The calendar builds a date-indexed map of bill statuses.
        - Each day cell receives the appropriate glow class.
        - A click handler is attached to each day cell.

    Step 5: Render Bill Lists
        - If state.selectedDate is set (user clicked a day):
            - Filter bills by due_date matching the selected date.
            - Split into UNPAID (due) and PAID arrays.
            - Render both lists using ui.renderList().
        - If no date is selected:
            - Show "Please select a date" placeholder in both panels.

    Step 6: Error Handling
        - If the fetch fails (backend down, network error), display
          the error message in the status bar.
        - Log the full error to the console for debugging.

---

## 3. Bill Projection Engine (core/utils.js)

### Purpose

The database only contains bills that have been explicitly created 
by the user. If a MONTHLY bill was created on May 3 and has not 
been paid yet, the database contains exactly one record. 
The user cannot see that the same bill will be due on June 2, 
July 2, August 1, etc., because the backend does not 
automatically generate future rows.

The projection engine fills this gap by generating virtual bill objects
that represent future recurring instances.

### Algorithm

    Input: Array of real bills, target year, target month.
    Output: Array of real bills + projected bills.

    1. Copy the input array to avoid mutation.

    2. Filter to bills that have recurring_interval !== 'NONE'.

    3. Group recurring bills by name. For each name, keep only the
       bill with the latest due_date. This prevents projecting from
       an older instance when a newer one already exists.

    4. For each latest instance:
        a. Start from its due_date.
        b. Loop forward:
            - WEEKLY: add 7 days to the current date.
            - MONTHLY: add 1 calendar month to the current date.
        c. For each projected date:
            - Check if a real bill with the same name already exists
              on that date (database already has it).
            - If not, create a virtual bill object:
                - Copy all fields from the source bill.
                - Override id with "proj-{sourceId}-{dateStr}".
                - Override due_date with the projected date.
                - Set status to UNPAID.
                - Set isProjected to true.
        d. Stop when the projected date exceeds the horizon
           (end of the year after the target year).

    5. Return the combined array.

### Projection Horizon

The horizon is set to December 31 of (targetYear + 1). This means
if the user is viewing April 2026, projections extend through
December 31, 2027. This gives approximately 20 months of lookahead,
which is sufficient for most household budgeting needs.

### Month Arithmetic

For MONTHLY projections, the engine uses JavaScript's setMonth()
method rather than adding a fixed 30-day offset. This means:

    May 31 + 1 month = June 30 (not July 1)
    January 31 + 1 month = February 28/29

This is more calendar-accurate than the backend's 30-day timedelta,
which is a known divergence between the two systems.

### Projected Bill Identification

Projected bills are identified by two markers:

    1. The id field is a string starting with "proj-".
       Real bills have numeric integer IDs.
    2. The isProjected field is set to true.
       Real bills do not have this field.

The selectBill() function checks for the "proj-" prefix
and disables the Mark PAID and Delete buttons when a projected bill
is selected. This prevents the user from trying to operate on a
record that does not exist in the database.

---

## 4. Calendar Rendering Algorithm (components/calendar.js)

### Grid Construction

The calendar builds a 7-column CSS Grid with three types of cells:

    1. Header cells: S M T W T F S (7 cells, always present).
    2. Padding cells: Empty divs to align day 1 with its weekday.
       Count = getDay() of the first day of the month (0=Sunday).
    3. Day cells: One div per day of the month.

The total number of cells in the grid varies by month:
- February 2026 (starts Sunday): 7 headers + 0 padding + 28 days = 35
- March 2026 (starts Sunday): 7 headers + 0 padding + 31 days = 38
- April 2026 (starts Wednesday): 7 headers + 3 padding + 30 days = 40

### Date String Format

Every day cell has a corresponding date string in YYYY-MM-DD format.
This string is constructed by zero-padding the month and day:

    `${year}-${String(month+1).padStart(2,'0')}-${String(day).padStart(2,'0')}`

This format matches the ISO date strings returned by the backend,
enabling direct string comparison for bill matching.

### Status Aggregation

Before rendering day cells, the algorithm builds a lookup map:

    dateInfo = {
        "2026-05-03": { statuses: Set(["UNPAID"]), hasExpired: false },
        "2026-05-04": { statuses: Set(["PAID"]), hasExpired: false },
        "2026-04-29": { statuses: Set(["UNPAID"]), hasExpired: true },
        ...
    }

Each bill is iterated once. For each bill:
- Its status (PAID/UNPAID) is added to the date's status Set.
- If its is_expired field is 'Y', or if it is UNPAID and its due_date
  is before today, the date's hasExpired flag is set to true.

This aggregation handles dates with multiple bills correctly.
A date with one PAID and one UNPAID bill will have both statuses
in its Set, triggering the "mixed" color.

### Color Priority

The glow class assignment follows a strict priority order:

    1. Expired (highest priority): If any bill on the date is expired,
       the date gets .glow-expired (black), regardless of other bills.

    2. Mixed: If the date has both UNPAID and PAID bills (and none
       are expired), it gets .glow-mixed (orange).

    3. Due: If the date has only UNPAID bills, it gets .glow (red).

    4. Paid: If the date has only PAID bills, it gets .glow-paid (green).

    5. No bills: No glow class. Default white cell.

The "today" class (.today, blue) is applied independently of glow
classes. A date can be both "today" and "glow" simultaneously,
though the glow class will visually dominate because it is declared
later in the CSS cascade.

### Selection Highlighting

When the user clicks a day cell, state.selectedDate is set to that
date string. On the next fetchBills() cycle, the calendar re-renders
and applies inline styles to the selected day:

    background: #dbeafe
    borderColor: #2563eb

These inline styles override the glow class backgrounds, ensuring
the selected date is always visually distinct regardless of its
bill status.

### Month Navigation

The changeMonth() function modifies state.currentMonth and
state.currentYear, handling year rollovers:

    - Month goes above 11: reset to 0, increment year.
    - Month goes below 0: reset to 11, decrement year.

After updating state, it calls the onUpdate callback (which is
fetchBills()) to re-render the entire UI with the new month context.

---

## 5. Bill List Rendering (components/ui.js)

### Table Generation

The renderList() function builds an HTML table programmatically:

    table.bill-table
        thead
            tr (header row: Name, Category, Amount, Due)
        tbody
            tr.bill-row (one per bill, clickable)
            -- or --
            tr (single cell spanning 4 columns with empty message)
            tr.bill-add-row (optional, only in "Due Bills" panel)

Each bill row displays four cells. The amount is prefixed with "Rs."
and the category shows "-" if null.

### Click Handling

Each bill row has a click event listener that calls the selectBill
callback. The callback receives the full bill object and the DOM row
element. This two-argument pattern allows the orchestrator to both
update state (from the bill object) and update the DOM (by adding
the .selected class to the row).

### Add Button

The "+" button row is conditionally appended only when:
1. An onAddClick callback is provided.
2. The container's id is "bills" (the Due Bills panel).

This prevents the add button from appearing in the Paid Bills panel
or the search results panel, where creating a new bill would be
contextually inappropriate.

The button is styled as a perfect circle (border-radius: 999px) with
a blue outline, creating a floating action button aesthetic.

### Empty State

When the bills array is empty, a single row spanning all four columns
displays the provided emptyText message. This ensures the table
structure is maintained even when there is no data, preventing layout
shifts when bills are loaded.

---

## 6. Modal Lifecycle (components/modal.js)

### Visibility Pattern

Both modals use CSS class toggling for visibility:

    Show: element.classList.remove('hidden')
    Hide: element.classList.add('hidden')

The `.modal` class sets `display: flex` for centering.
The `.modal.hidden` class overrides with `display: none`.

### Create Modal

Opening sequence:
1. Remove 'hidden' class from the modal container.
2. Call setDueDateDefaults() to constrain the date input.
3. Focus the name input for immediate typing.

Closing triggers:
- Click the X button (close-create-modal).
- Click outside the modal content (on the backdrop).
- Successful form submission (from dashboard.js).

### Delete Modal

Opening sequence:
1. Update the confirmation text to include the bill name.
2. Remove 'hidden' class from the modal container.

Closing triggers:
- Click the Cancel button.
- Click outside the modal content (on the backdrop).
- Successful deletion (from dashboard.js).

### Date Defaults

The setDueDateDefaults() function runs on init and on every modal open:
- Sets the date input's `min` attribute to today's date (ISO string).
  This prevents the user from selecting a past date.
- Sets the date input's `value` to 3 days from today.
  This provides a sensible default for most short-term bills.

---

## 7. API Communication Layer (core/api.js)

### Request Wrapper

All API calls go through a single requestJson() function:

    1. Construct the full URL by prepending the API base URL.
    2. Execute fetch() with the provided options.
    3. Parse the response body as JSON.
       If parsing fails, default to an empty object.
    4. If the response status is not 2xx, throw an Error
       with the most descriptive message available:
       payload.detail > payload.message > statusText > "HTTP {code}"
    5. Return the parsed payload on success.

This centralized error extraction means every UI component gets
consistent, human-readable error messages without duplicating
the parsing logic.

### Response Normalization

The fetchAllBills() and searchBills() functions normalize the backend
response format. The backend returns { OK, total_count, data: [...] }
but these functions return just the data array. They also handle the
edge case where the response might be a plain array (for forward
compatibility), falling back gracefully:

    Array.isArray(result) ? result : result.data || []

### Exported Functions

| Function | Method | Endpoint | Returns |
| -------- | ------ | -------- | ------- |
| fetchUpcomingBills(days) | GET | /bills/upcoming?days={n} | Array of bills |
| fetchAllBills() | GET | /bills/all | Array of bills |
| updateBillStatus(id, status) | PUT | /bills/{id} | void |
| deleteBillById(id) | DELETE | /bills/{id} | void |
| createBill(payload) | POST | /bills/new | Created bill object |
| searchBills(name) | GET | /bills/search?name={q} | Array of bills |

Note: fetchUpcomingBills() is defined but not currently called by
the frontend. It exists for potential future use (e.g., a notification
badge). The automation shell script calls the same endpoint directly.

---

## 8. Event Handling Architecture (features/*)

The business logic is modularized into feature files. `dashboard.js` wires these features to UI elements via event listeners.

### Bill Selection Logic (in billListing.js)

When a bill row is clicked, selectBill() executes:

    1. Store the bill object in state.selectedBill.
    2. Clear all existing .selected classes from other rows.
    3. Update the action panel text with bill details:
       "{name} . Rs.{amount} . due {date} . {status} . {interval}"
    4. Set the Mark PAID button label based on current status.
    5. Check if the bill is projected (id starts with "proj-").
       - If projected: disable both action buttons, show status message.
       - If real: enable both action buttons.
    6. Add .selected class to the clicked row.

### Status Update Flow (in billStatus.js)

When Mark PAID is clicked:

    1. Read state.selectedBill.status.
    2. Compute the opposite status (PAID -> UNPAID, UNPAID -> PAID).
    3. Call api.updateBillStatus(id, newStatus).
    4. On success: update the in-memory bill object's status,
       show success message, and call fetchBills() to refresh.
    5. On failure: show error message in status bar.

The system relies on the **Bill Projection Engine** (Step 3) to visually 
forecast future bills. When a user marks a bill as PAID, the 
`fetchBills()` cycle is re-triggered. The engine then uses the 
newly-paid bill as the "anchor" to project the next upcoming 
instance, which will appear in the calendar as a virtual UNPAID bill.
The backend does not generate any rows automatically.

### Deletion Flow (in billDeletion.js)

When Delete is clicked:

    1. Open the delete confirmation modal.
    2. Update the confirmation text with the bill's name.
    3. Wait for user to click Confirm or Cancel.
    4. On Confirm: call api.deleteBillById(id).
    5. On success: close the modal, call fetchBills() to refresh.
    6. On failure: show error message in status bar.

### Creation Flow (in billCreation.js)

When the create form is submitted:

    1. Prevent default form submission.
    2. Read all form values.
    3. Validate: name non-empty, amount non-negative and valid, date set.
    4. Call api.createBill() with the form data.
    5. On success: reset the form, close the modal, restore date defaults,
       and call fetchBills() to refresh.
    6. On failure: show the backend's validation error in the status bar.

### Search Flow (in billSearch.js)

When the search button is clicked or Enter is pressed in the input:

    1. Read and trim the search input value.
    2. If empty, clear the search results container and return.
    3. Call api.searchBills(query).
    4. Render the results using ui.renderList() in the search container.
    5. Show the result count in the status bar.
    6. On failure: show error message in status bar.

Search results use the same table format and click handlers as the
bill lists. Clicking a search result selects it for actions just
like clicking a bill in the due/paid panels.
