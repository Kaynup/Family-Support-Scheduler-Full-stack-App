# Frontend Classes and Functions

## Scope
The frontend is mostly modular functions and shared helpers, not classes.

## Login Functions
- `handleLoginSubmit(event)` posts credentials to `/auth/login`, stores the token and role, and redirects to the sender or receiver dashboard.
- `handleRegisterSubmit(event)` posts to `/auth/register`, shows field-level validation messages, and redirects back to `login.html` on success.
- `showError(msg)` displays page-level auth errors.

## Shared Core Functions
- `requestJson(path, options)` adds the bearer token, performs the fetch, and normalizes JSON error handling.
- `fetchUpcomingBills(days)`, `fetchExpiredBills()`, `fetchAllBills()`, `fetchAllBillsForBeneficiary(beneficiaryId)`, `fetchUsers(role)`, `searchBills(name)`, `createBill(payload)`, `updateBillStatus(id, status)`, `deleteBillById(id)`, `payBill(billId, amount)`, and `fetchRemittanceHistoryByRole(role)` map directly to backend endpoints.
- `clearSession()` and `requireRole(expectedRole)` handle auth gating.
- `createAppState(overrides)` seeds shared dashboard state.
- `getDaysUntilDue(bill)`, `isBillExpired(bill)`, and `filterBillsForDisplay(bills)` support bill display rules.
- `setLoggedInUserLabel(elementId)` prints the username and role into the dashboard header.
- `renderRemittanceHistoryRows(listEl, data)` and `renderRemittanceHistoryError(listEl, message)` populate the remittance history table.
- `showUpcomingAndExpiredBills(options)` fills the upcoming bills modal and suppresses repeat display with `sessionStorage`.

## Panel Entry Points
- Sender dashboard: `fetchAndRenderBills()`, `fetchAndRenderBillsForBeneficiary()`, `refreshCurrentView()`, `loadBeneficiaries()`, `handleBillSelect()`, `setupGlobalEventListeners()`, `dueBillsPopUpWindow()`, and `initializeApp()`.
- Receiver dashboard: `fetchAndRenderAllBills()`, `handleBillSelect()`, `setupEventListeners()`, and `init()`.
- Receiver create page: the `DOMContentLoaded` submit handler in `create.js` builds the payload and opens the success modal.
- Sender and receiver history pages: `DOMContentLoaded` handlers fetch the remittance history and render it.

## Notes
If you add a new reusable UI behavior, document the shared helper first and then the page script that consumes it.