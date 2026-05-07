# Frontend Refactor Tasks

Follow these tasks sequentially to implement the unified frontend authentication architecture.

## PHASE 1 — Shared Assets Extraction

### TASK 1.1 — Create Shared Directories
- Create `frontend/shared/css/` and `frontend/shared/js/`.
- Move all `.css` files from `frontend/receiver_panel/css/` into `frontend/shared/css/`.
- Delete `frontend/sender_panel/css/` entirely.

### TASK 1.2 — Centralize Config
- Create `frontend/shared/js/config.js` containing `export const API_BASE_URL = "http://127.0.0.1:8000";`.
- Delete `frontend/receiver_panel/js/config.js` and `frontend/sender_panel/js/config.js`.

---

## PHASE 2 — Unified Login Module

### TASK 2.1 — Create Login Files
- Create `frontend/login/login.html`. Build a login form that imports the shared CSS.
- Create `frontend/login/register.html`. Build a registration form that includes a `<select>` dropdown for Role (Sender or Beneficiary).

### TASK 2.2 — Create Auth Logic
- Create `frontend/login/js/auth.js`.
- Implement `handleLoginSubmit`:
  - POST to `/auth/login`.
  - Store `token` and `role` in `localStorage`.
  - `if (role === 'beneficiary') window.location.href = '/receiver_panel/pages/dashboard.html';`
  - `else if (role === 'sender') window.location.href = '/sender_panel/pages/dashboard.html';`
- Implement `handleRegisterSubmit`:
  - POST to `/auth/register` including the selected role from the dropdown.
  - Redirect to `login.html` on success.

---

## PHASE 3 — Panel Refactoring

### TASK 3.1 — Clean Up Receiver Panel
- Delete `frontend/receiver_panel/pages/login.html`, `register.html`.
- Delete `frontend/receiver_panel/js/auth.js`.
- Update `receiver_panel/js/core/auth_guard.js`: 
  - Ensure it checks for `token` and `role === 'beneficiary'`.
  - On failure, redirect to `/login/login.html`.
- Update `receiver_panel/js/core/api.js` to import `API_BASE_URL` from `../../../shared/js/config.js`.
- Update all HTML files in `receiver_panel/pages/` to point their `<link rel="stylesheet">` tags to `../../shared/css/styles.css`.
- Update all navigation Links (`Logout`, etc.) to point to `/login/login.html`.

### TASK 3.2 — Clean Up Sender Panel
- Delete `frontend/sender_panel/pages/login.html`, `register.html`.
- Delete `frontend/sender_panel/js/auth.js`.
- Update `sender_panel/js/core/auth_guard.js`:
  - Ensure it checks for `token` and `role === 'sender'`.
  - On failure, redirect to `/login/login.html`.
- Update `sender_panel/js/core/api.js` to import `API_BASE_URL` from `../../../shared/js/config.js`.
- Update all HTML files in `sender_panel/pages/` to point their CSS links to `../../shared/css/styles.css`.
- Update all navigation Links (`Logout`, etc.) to point to `/login/login.html`.

---

## PHASE 4 — Deployment Updates

### TASK 4.1 — Update Makefile
- Remove `start-receiver` and `start-sender` targets.
- Create a single `start-frontend` target:
  ```makefile
  start-frontend:
      bash -c "cd frontend && python3 -m http.server 3000"
  ```
- Update `start-all` to run `start-frontend` alongside `start-backend`.

### TASK 4.2 — Update README.md
- Revise the Startup Instructions to reflect the new unified `make start-frontend` command.
- Note that the entry point is now `http://127.0.0.1:3000/login/login.html`.
