# Family Support Scheduler

A calendar-based scheduling and remittance platform designed for recurring family bills.
It allows beneficiaries to log, track, and manage their expenses, while allowing senders to view these obligations and fulfill them directly via stablecoin remittance.

## Architecture
The application uses a decoupled frontend and backend:
1. **Frontend (Vanilla JS, HTML, CSS)**: A Multi-Page Application (MPA) split into unified login, `receiver_panel` for beneficiaries, and `sender_panel` for senders.
2. **Backend (FastAPI, Python)**: Provides RESTful endpoints for auth, bill management, and remittance processing.
3. **Database (MySQL)**: Stores users, bills (only active instances for recurring ones), and remittance history.

## Startup Instructions
Use the provided Makefile to manage services:

1. **Start the Database**
   Ensure MySQL is running and configured according to `.env`.
   (See `docs/database/` for schema and sample data instructions).

2. **Start the Backend API**
   ```bash
   make start-backend
   ```
   Runs on `http://127.0.0.1:8000`.

3. **Start the Frontend**
   ```bash
   make start-frontend
   ```
   Runs on `http://127.0.0.1:8003`. Navigate to `http://127.0.0.1:8003/login/login.html`.

## Testing
Run the full suite of unit and integration tests (uses `pytest`):
```bash
make run-tests
```

## Documentation
For deeper architectural details, refer to the following directories:
- `docs/backend/` - API structure, schema mapping, and service logic.
- `docs/frontend/` - MPA architecture, projection engine, and rendering logic.
- `docs/database/` - MySQL schema, query organization, and testing fixtures.
- `docs/automation/` - Makefiles, CLI scripts, and cron simulation.