# Files Involved in Frontend

The frontend is split into `receiver_panel` and `sender_panel`. Both have a parallel structure:

- `css/`: Shared styling.
- `js/core/`:
  - `api.js`: Network requests and JWT injection.
  - `state.js`: Client-side state (selected bill, current calendar month).
  - `utils.js`: Helper functions.
  - `auth_guard.js`: Role enforcement and token validation checks.
- `js/components/`:
  - `ui.js`: DOM element references and rendering functions.
  - `calendar.js`: Calendar rendering logic.
  - `modal.js`: Modal open/close handlers.
- `js/features/` (Receiver only):
  - Split logic for `billListing.js`, `billStatus.js`, `billDeletion.js`, `billSearch.js`.
- `pages/`: HTML files for each view (`login.html`, `dashboard.html`, `bills.html`, `create.html`, `history.html`).
- `js/<page>.js`: Page-specific entry scripts that wire event listeners together.
