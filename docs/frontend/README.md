# Frontend Documentation

The frontend is a **Multi-Page Application (MPA)** using Vanilla JavaScript (ES6 modules), HTML, and CSS. It utilizes a unified server running on port `8003` to serve static files.

## Architecture & Workspaces

The application is split into three main modules:
1. `login/`: A unified login portal. Authenticates via the backend API and routes the user based on their `role` (sender or beneficiary).
2. `receiver_panel/`: For beneficiaries. Allows creation, deletion, and tracking of bills. 
3. `sender_panel/`: For senders. Allows tracking of all beneficiary bills and executing remittance payments.

## Component Structure
Both panels share a highly similar modular structure:
- `core/api.js`: Handles backend HTTP requests and JWT injection.
- `core/auth_guard.js`: Protects pages by validating the token and role in `localStorage`.
- `core/state.js`: Global state management for the panel.
- `core/utils.js`: Logic for parsing bills, date calculations, and the Projection Engine.
- `components/ui.js`: DOM manipulation, rendering HTML tables, and dynamic UI updates.
- `components/calendar.js`: Logic for rendering the interactive grid calendar.
- `features/*`: Feature-specific logic (e.g., `billListing.js`, `billSearch.js`).

## The Projection Engine (Decoupling Lists vs. Calendar)
The frontend enforces a strict separation between real data and projected visualizations:
- **List Views & Dashboards**: These tables render exactly what is in the database (real, `UNPAID` bills). They do not hide expired bills, ensuring senders can pay them.
- **Calendar View**: The calendar takes the active database bills and runs them through a client-side Projection Engine in `utils.js` (`getProjectedBills`). This engine generates 12 months of future "virtual" instances for recurring bills so the user can visualize upcoming expenses on the calendar grid, without polluting the actual payment tables.
