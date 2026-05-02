# Frontend Sub-system

## Technology

Vanilla JavaScript (ES6 modules) running on Node v20.20.2.
No framework. No build step. No bundler. No transpiler.
The browser loads ES6 modules natively via `<script type="module">`.

The frontend is served by Python's built-in HTTP server on port 8080,
launched through the project Makefile. There is no webpack, vite, or
any other development toolchain involved.

## Architecture

The frontend follows a modular Single-Page Application (SPA) pattern
without a router. There are two HTML pages:

    index.html       -- Login screen
    dashboard.html   -- Main application

Navigation between them is handled by standard HTML links and form
actions, not by JavaScript routing. Once inside dashboard.html, all
interactions are handled by JavaScript without page reloads.

The JavaScript layer is organized into a highly modular, enterprise-grade architecture under the `js/` directory:

    js/
        core/
            api.js         -- HTTP client (fetch wrapper)
            state.js       -- Centralized application state
            utils.js       -- Date math and bill projection engine
        components/
            ui.js          -- DOM element registry and rendering functions
            calendar.js    -- Calendar grid generation and status coloring
            modal.js       -- Modal open/close/defaults logic
        features/
            billListing.js -- Fetching, projecting, and rendering bill lists
            billStatus.js  -- Patching bill status (paid/unpaid)
            billDeletion.js-- Deletion confirmation and API call
            billCreation.js-- Form submission and creation API call
            billSearch.js  -- Search logic and rendering
        dashboard.js       -- The entry point (wiring event listeners)

The module dependency graph strictly separates concerns:

    dashboard.js imports from core, components, and features to wire events.
    features/* orchestrate the logic by importing core state and component renderers.
    components/* handle pure UI rendering, only reading from core state.
    core/* are fundamental utilities that depend on nothing else.

## Serving Model

The Makefile starts the frontend with:

    python -m http.server 8080

This serves static files from the `frontend/` directory. There is no
server-side rendering, no templating engine, and no middleware. The
browser fetches HTML, CSS, and JS files directly, then the JavaScript
communicates with the backend API at http://127.0.0.1:8000 via fetch.

## State Management

The application uses a shared mutable state object exported from
state.js. This object holds four properties:

    selectedBill   -- The currently highlighted bill object (or null).
    currentMonth   -- Integer (0-11) for the calendar's displayed month.
    currentYear    -- Integer for the calendar's displayed year.
    selectedDate   -- ISO date string (YYYY-MM-DD) or null.

All modules that need to read or write state import this same object.
Because JavaScript objects are passed by reference, mutations in one
module are visible to all others immediately. This eliminates the need
for a pub/sub event system or a state management library.

The trade-off is that there is no change detection. When state changes,
the module that changed it must explicitly call fetchBills() or
renderCalendar() to update the UI. There is no automatic re-rendering.

## Authentication

The login page (index.html) uses HTML5 form validation with hardcoded
credentials:

    Username: admin
    Password: password123

Validation is enforced by the `pattern` attribute on the input elements.
The browser itself rejects non-matching inputs before the form submits.
On success, the form navigates to dashboard.html via a standard GET
request. There is no session token, no cookie, and no server-side
authentication check.

The dashboard has a "Logout" link that navigates back to index.html.

## Design System

The visual identity is defined using a **modular CSS** architecture with no external CSS framework. The styles are split into logical modules under the `css/` directory and imported by a main manifest file.

    styles.css         -- Main manifest (imports all modules)
    css/
        base.css       -- Global resets, typography, and default element styles
        layout.css     -- Main container and dashboard grid positioning
        components.css -- Cards, tables, and buttons
        calendar.css   -- Calendar grid and status coloring logic
        modals.css     -- Modal overlay and form layout styles

### Visual Tokens

    Font:       Consolas / Courier New (monospace)
    Background: #f7f9fc (light blue-gray)
    Cards:      #f8fafc with #dbe2ea borders, 16px border-radius
    Primary:    #2563eb (blue)
    Danger:     #ef4444 (red)

The layout uses CSS Grid for the two-column dashboard and the 7-column calendar. The main container is constrained to 1200px with a responsive min() function.

