# Frontend Refactor Design

## Objective
The current frontend architecture duplicates authentication forms and logic across the `receiver_panel` and `sender_panel`. The objective is to unify the authentication flow into a single, common entry point (`frontend/login/`) and establish a single frontend server to simplify deployment and routing.

## Architectural Changes

### 1. Unified Authentication (`login/`)
Instead of separate login/register pages inside each panel, we will create a dedicated `login` module.
- **Dynamic Routing**: The unified `auth.js` will handle the login request. Upon a successful API response, it will inspect the `role` returned in the JWT payload (or API response body).
    - If `role === 'beneficiary'`, the script redirects the user to `/receiver_panel/pages/dashboard.html`.
    - If `role === 'sender'`, the script redirects the user to `/sender_panel/pages/dashboard.html`.
- **Role Registration**: The registration page will include a UI toggle or select dropdown allowing the user to choose whether they are signing up as a Sender or a Beneficiary.

### 2. Single Frontend Server
Currently, the `Makefile` attempts to serve the receiver panel on port 3000 and the sender panel on port 3001. This makes navigating between the unified login and the separate panels cumbersome (requiring hardcoded port jumping).
- **Solution**: We will serve the entire `frontend/` directory from a single `http.server` on **port 3000**.
- Users will navigate to `http://localhost:3000/login/login.html` to start.
- Panel boundaries are enforced purely by the directory path and the client-side `auth_guard.js`, rather than separate ports.

### 3. Shared Resources (Optional but Recommended)
To fully embrace DRY (Don't Repeat Yourself), we should extract identical configuration and CSS into a `frontend/shared/` directory.
- `shared/css/`: Common styles used by login, receiver, and sender.
- `shared/js/config.js`: The single definition for `API_BASE_URL`.

## Security Enforcement
The `auth_guard.js` script inside each panel will remain. 
- The Receiver Panel guard will verify `token` exists and `role === 'beneficiary'`.
- The Sender Panel guard will verify `token` exists and `role === 'sender'`.
If validation fails, the user is instantly redirected back to `/login/login.html`.
