# Frontend Architecture

The frontend uses a Multi-Page Application (MPA) architecture divided into two independent panels.

## Dual-Panel System
1. **Receiver Panel** (`frontend/receiver_panel/`): Served on port 3000. For beneficiaries to manage, create, and track bills.
2. **Sender Panel** (`frontend/sender_panel/`): Served on port 3001. For senders to view beneficiary bills and execute stablecoin remittances.

Both panels share a similar structural pattern (Core, Components, Features, Pages) but are completely isolated to enforce role boundaries and security.

## Technology Stack
- **HTML5**: Structural pages.
- **Vanilla CSS**: Shared styles (`css/styles.css`).
- **Vanilla JavaScript (ES6 Modules)**: No bundlers or frameworks.

## Security
- Each panel enforces access via an `auth_guard.js` module.
- JWTs are stored in `localStorage` and sent via the `Authorization: Bearer <token>` header in `api.js`.
- If a token is missing, expired, or carries the wrong role, the user is redirected to the login page.
