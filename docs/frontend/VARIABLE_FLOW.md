# Frontend Variable Flow

## Scope
This document tracks the browser-side variables and shared helpers used by the login, sender, and receiver pages.

## Real Variables and State
- Session values: `token`, `role`, and `username` in `localStorage`.
- Auth guard state: `requireRole(expectedRole)` clears session data and redirects when the role does not match.
- Shared app state: `createAppState()` provides `currentUser`, `selectedBill`, `currentMonth`, `currentYear`, `selectedDate`, `projectionCount`, and optional overrides.
- Sender dashboard state: `currentBeneficiaryId` in `sender_panel/js/dashboard.js` scopes bill refreshes to one beneficiary.
- Receiver create flow state: `state.newCreatedBill` holds the most recently created bill so the table can reselect it.
- Alert state: `sessionStorage.upcomingModalShown` prevents the upcoming/expired modal from showing more than once per session.
- Shared API base URL: `API_BASE_URL` in `frontend/shared/js/config.js`.

## Flow
1. Login stores `token`, `role`, and `username`.
2. Route guards verify the stored role before a page loads.
3. Shared API helpers add the bearer token to requests and normalize responses.
4. Page scripts render the dashboard, modal, table, or form state from the fetched data.
5. User interaction updates `selectedBill`, `selectedDate`, or panel-specific variables, then rerenders the UI.

## Notes
Keep shared state here only if it crosses more than one page. Page-only DOM references belong in the function docs.