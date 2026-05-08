# Family Support Scheduler / Remittance Platform

Remittance isn't just about sending money; it's about fulfilling obligations. Migrant workers frequently need to ensure specific bills back home (like rent, school tuition, or medical bills) are paid on strict deadlines. Missing a date can have severe consequences.

## Objective

Build a calendar-based scheduling and remittance platform designed for recurring family bills.
It allows beneficiaries to log, track, and manage their expenses, while allowing senders to view these obligations and fulfill them directly via stablecoin remittance.

## Architecture

The application is split into three main components:

1. **Backend API (FastAPI)**: Serves both panels, providing RESTful endpoints for authentication, bill management, and remittance processing.
2. **Unified Login (`frontend/login/`)**: A single authentication entry point. On login, the server returns the user's `role`; the client then redirects to the appropriate panel.
3. **Receiver Panel (`frontend/receiver_panel/`)**: Used by beneficiaries to log, track, and manage bills.
4. **Sender Panel (`frontend/sender_panel/`)**: Used by senders to view beneficiary bills and execute payments.

All panels are served by a **single HTTP server on port 3000** from the `frontend/` root. Panel access is enforced by `auth_guard.js` inside each panel, which verifies the user's `role` from `localStorage`.

### Role Descriptions
- **Beneficiary (`receiver_panel`)**: Can create, update, delete, and view their bills. Cannot process remittances.
- **Sender (`sender_panel`)**: Can view beneficiary bills and execute payments. Cannot create or delete bills.

## Tech Stack
- **Frontend**: Vanilla JS (ES6 modules), HTML5, CSS3.
- **Backend**: Python 3.10.20, FastAPI.
- **Database**: MySQL (8.0).
- **Authentication**: JWT, bcrypt hashing.

## Startup Instructions

Use the `Makefile` to manage the services.

### 1. Start the Database
Ensure your MySQL server is running and configured according to `.env`.

### 2. Start the Backend API
```bash
make start-backend
```
The backend will run on `http://127.0.0.1:8000`.

### 3. Start the Frontend
```bash
make start-frontend
```
Navigate to `http://127.0.0.1:3000/login/login.html` to begin.

Both panels are accessible from this single server — login routes you automatically based on your role.

## Testing

To run the full suite of unit and integration tests:
```bash
make run-tests
```
Tests will execute via `pytest` and automatically apply the correct environment variable context.

## Documentation
- **Backend**: See `docs/backend/` for details on APIs, schemas, and service logic.
- **Frontend**: See `docs/frontend/` for details on the MPA architecture and rendering logic.