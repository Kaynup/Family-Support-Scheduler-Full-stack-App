# Family Support Scheduler / Remittance Platform

Remittance isn't just about sending money; it's about fulfilling obligations. Migrant workers frequently need to ensure specific bills back home (like rent, school tuition, or medical bills) are paid on strict deadlines. Missing a date can have severe consequences.

## Objective

Build a calendar-based scheduling and remittance platform designed for recurring family bills.
It allows beneficiaries to log, track, and manage their expenses, while allowing senders to view these obligations and fulfill them directly via stablecoin remittance.

## Dual-Panel Architecture

The application is split into three main components:

1. **Backend API (FastAPI)**: Serves both panels, providing RESTful endpoints for authentication, bill management, and remittance processing.
2. **Receiver Panel (Frontend - Port 3000)**: Used by beneficiaries. They can log upcoming expenses, categorize them, and track what has been paid.
3. **Sender Panel (Frontend - Port 3001)**: Used by senders (e.g., migrant workers). They can view the bills their family members have posted and pay them directly through the platform.

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

### 3. Start the Receiver Panel
```bash
make start-receiver
```
The receiver panel will be available at `http://127.0.0.1:3000/pages/login.html`.

### 4. Start the Sender Panel
```bash
make start-sender
```
The sender panel will be available at `http://127.0.0.1:3001/pages/login.html`.

## Testing

To run the full suite of unit and integration tests:
```bash
make run-tests
```
Tests will execute via `pytest` and automatically apply the correct environment variable context.

## Documentation
- **Backend**: See `docs/backend/` for details on APIs, schemas, and service logic.
- **Frontend**: See `docs/frontend/` for details on the MPA architecture and rendering logic.