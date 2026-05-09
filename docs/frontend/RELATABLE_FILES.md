# Relatable Files (Frontend)

The frontend uses a Multi-Page Architecture (MPA) distributed across static files. State and network logic are modularized using ES6 imports.

## 1. Authentication
- **`frontend/login/login.html`**: Unified entry point for all users.
- **`frontend/login/js/auth.js`**: Captures login submissions, sends them to `/auth/login`, and stores the returned JWT in `localStorage`. Routes to `/sender_panel/pages/dashboard.html` or `/receiver_panel/pages/dashboard.html`.

## 2. Panels (Sender & Receiver)
Both `frontend/sender_panel/` and `frontend/receiver_panel/` share a common architectural pattern.
- **`pages/`**:
  - `dashboard.html`: The main view containing the Calendar grid, action panel, and popup modals.
  - `bills.html`: A detailed list view of all `UNPAID` bills for the user.
  - `history.html`: A detailed ledger view of all `PAID` bills and remittance transactions.

## 3. Core Modules (`js/core/`)
- **`api.js`**: Standardized wrappers for `fetch()`. Automatically injects the `Authorization: Bearer <token>` header into all outbound requests.
- **`auth_guard.js`**: Invoked at the top of every page script. Checks if a valid token exists; if not, kicks the user back to the login screen.
- **`state.js`**: A simple singleton object holding transient state like `selectedBill`, `selectedDate`, and cached `currentBills`.
- **`utils.js`**: Pure JavaScript logic. Contains the all-important Projection Engine (`getProjectedBills`).

## 4. Components & Features
- **`js/components/ui.js`**: Handles all imperative DOM updates (e.g., `renderBillTable()`, `displayStatusMessage()`).
- **`js/components/calendar.js`**: Generates the dynamic month/year CSS Grid calendar based on active dates.
- **`js/features/billListing.js`**: Connects `api.js` fetches to `ui.js` rendering specifically for the lists.
