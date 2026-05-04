# Frontend Rendering & Logic Flow (Detailed Schematic)

This document provides a comprehensive mapping of the frontend subsystem, detailing the sequential flow of execution, module responsibilities, and specific function signatures.

## 1. Module Hierarchy & Responsibilities

| Layer | Responsibility | Key Files |
| :--- | :--- | :--- |
| **Entry Point** | Application bootstrap and event orchestration. | `dashboard.js` |
| **Features** | Business logic for specific actions (CRUD, Search). | `features/*.js` |
| **Components** | UI rendering engines and DOM element registry. | `components/*.js` |
| **Core** | Shared state, API client, and mathematical utils. | `core/*.js` |

---

## 2. Detailed Interaction Sequence

```mermaid
sequenceDiagram
    participant User
    participant Dash as "dashboard.js"
    participant FeatList as "features/billListing.js"
    participant FeatStat as "features/billStatus.js"
    participant CompUI as "components/ui.js"
    participant CompCal as "components/calendar.js"
    participant CoreState as "core/state.js"
    participant CoreUtils as "core/utils.js"
    participant CoreAPI as "core/api.js"
    
    Note over User, CoreAPI: I. BOOTSTRAP PHASE
    User->>Dash: Load index.html
    Dash->>Dash: initializeApp()
    Dash->>Dash: setupGlobalEventListeners()
    Dash->>FeatList: fetchAndRenderBills()
    
    Note over User, CoreAPI: II. DATA FETCH & PROJECTION
    FeatList->>CoreAPI: fetchAllBills()
    CoreAPI-->>FeatList: JSON (Real Rows)
    FeatList->>CoreUtils: getProjectedBills(realBills, 12)
    Note over CoreUtils: generateProjectionsForBill()<br/>Calculates virtual instances
    CoreUtils-->>FeatList: Array [Real + Projected]
    Note over FeatList: allBills is kept in local scope<br/>for rendering pipeline
    
    Note over User, CoreAPI: III. RENDERING LOOP
    FeatList->>CompCal: renderCalendar(allBills, onDateClick)
    CompCal->>CompCal: buildDateInfoMap()
    CompCal->>CompCal: applyDayGlowEffect()
    CompCal->>CompUI: Inject HTML to elements.calendarGridEl
    
    FeatList->>FeatList: updateDashboardLists(allBills)
    FeatList->>CompUI: renderBillTable(dueForDate, handleSelectBill)
    CompUI-->>User: Visual Dashboard Refresh
    
    Note over User, CoreAPI: IV. SELECTION & ACTION
    User->>CompUI: Clicks a Bill Row
    CompUI->>FeatList: handleSelectBill(bill, rowEl)
    FeatList->>CoreState: Set state.selectedBill
    FeatList->>CompUI: renderSelectedBillSummary(bill)
    FeatList->>CompUI: Update Button States (disabled/enabled)

    User->>Dash: Clicks "Mark PAID"
    Dash->>FeatStat: patchBillStatus("PAID")
    alt isProjected == true
        FeatStat->>CoreAPI: createBill(newPayload)
    else isProjected == false
        FeatStat->>CoreAPI: updateBillStatus(id, "PAID")
    end
    CoreAPI-->>FeatStat: 200 OK / 201 Created
    FeatStat->>FeatList: fetchAndRenderBills() (Restart Phase II)
```

---

## 3. Comprehensive Function Reference

### Entry Point: `dashboard.js`
- **`initializeApp()`**: Entry point. Sets default dates, wires events, and triggers first fetch.
- **`setupGlobalEventListeners()`**: Attaches logic from `features/` to DOM IDs found in `ui.js`.

### Features Layer (`features/`)
- **`billListing.js`**
    - `fetchAndRenderBills()`: Orchestrates the API -> Projection -> Calendar flow.
    - `handleSelectBill(bill, rowEl)`: Updates selection state and enables/disables UI buttons.
    - `updateDashboardLists(allBills)`: Filters bills by selected date and renders sidebars.
- **`billStatus.js`**
    - `patchBillStatus(newStatus)`: Detects if a bill is projected (virtual) and either calls `POST` or `PUT`.
- **`billCreation.js`**
    - `handleCreateBillSubmit(event)`: Extracts form data and calls `API.createBill`.
- **`billDeletion.js`**
    - `handleOpenDeleteConfirmation()`: Populates the delete modal with selected bill details.
    - `handleConfirmDelete()`: Calls `API.deleteBillById`.
- **`billSearch.js`**
    - `handleSearchSubmit()`: Queries the backend via `API.searchBills` and renders a result table.

### Components Layer (`components/`)
- **`ui.js`**
    - `elements`: Registry of all interactive DOM elements (mapped by ID).
    - `renderBillTable()`: Higher-order function for generating dynamic tables.
    - `displayStatusMessage(msg)`: Updates the centralized terminal-style status bar.
- **`calendar.js`**
    - `renderCalendar()`: The main engine for drawing the month grid and padding.
    - `applyDayGlowEffect()`: Logic for assigning CSS classes (`glow`, `glow-paid`, `glow-expired`).
    - `handleMonthChange(delta)`: Updates state and re-fetches for navigation.
- **`modal.js`**
    - `handleOpenCreateModal()` / `handleCloseCreateModal()`: Visibility toggles.
    - `setDueDateDefaults()`: Logic for setting "Today + 3 days" on the creation form.

### Core Layer (`core/`)
- **`api.js`**: Native `fetch` wrappers for all `/bills` endpoints.
- **`utils.js`**:
    - `getProjectedBills()`: Core logic for generating virtual recurring instances.
    - `getDaysUntilDue()`: Date arithmetic for status logic.
- **`state.js`**: Single mutable object holding the current application context.
