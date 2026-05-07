# Frontend Hierarchical Structure

This outlines the new proposed directory structure for the frontend, consolidating authentication and unifying the development server.

## Legend
    [NEW]      File or directory to be created.
    [KEEP]     Existing file to be kept unchanged.
    [REFACTOR] Existing file to be modified.
    [DELETE]   Existing file to be removed.
    [MOVE]     File to be relocated.

## Proposed Structure

    frontend/
    ├── shared/                        [NEW DIR]
    │   ├── css/                       [NEW DIR]
    │   │   ├── base.css               [MOVE] from panels
    │   │   ├── layout.css             [MOVE] from panels
    │   │   ├── components.css         [MOVE] from panels
    │   │   ├── calendar.css           [MOVE] from panels
    │   │   ├── modals.css             [MOVE] from panels
    │   │   └── styles.css             [MOVE] updated to reflect new paths
    │   └── js/
    │       └── config.js              [MOVE] centralized API_BASE_URL
    │
    ├── login/                         [NEW DIR]
    │   ├── login.html                 [NEW] unified login page
    │   ├── register.html              [NEW] unified register page with role selection
    │   └── js/
    │       └── auth.js                [NEW] handles login and role-based redirects
    │
    ├── receiver_panel/                [REFACTOR DIR]
    │   ├── pages/
    │   │   ├── dashboard.html         [REFACTOR] update CSS/JS import paths
    │   │   ├── bills.html             [REFACTOR] update CSS/JS import paths
    │   │   ├── create.html            [REFACTOR] update CSS/JS import paths
    │   │   ├── history.html           [REFACTOR] update CSS/JS import paths
    │   │   ├── login.html             [DELETE]
    │   │   └── register.html          [DELETE]
    │   ├── css/                       [DELETE] moved to shared/
    │   └── js/
    │       ├── auth.js                [DELETE]
    │       ├── config.js              [DELETE]
    │       ├── core/                  
    │       │   ├── api.js             [REFACTOR] update config.js import path
    │       │   └── auth_guard.js      [REFACTOR] redirect to /login/login.html, check role='beneficiary'
    │       └── ...                    [KEEP] features and components
    │
    └── sender_panel/                  [REFACTOR DIR]
        ├── pages/
        │   ├── dashboard.html         [REFACTOR] update CSS/JS import paths
        │   ├── bills.html             [REFACTOR] update CSS/JS import paths
        │   ├── history.html           [REFACTOR] update CSS/JS import paths
        │   ├── login.html             [DELETE]
        │   └── register.html          [DELETE]
        ├── css/                       [DELETE] moved to shared/
        └── js/
            ├── auth.js                [DELETE]
            ├── config.js              [DELETE]
            ├── core/
            │   ├── api.js             [REFACTOR] update config.js import path
            │   └── auth_guard.js      [REFACTOR] redirect to /login/login.html, check role='sender'
            └── ...                    [KEEP] components

---

## Root Level Updates

    InternshipProject/
    └── Makefile                       [REFACTOR] Replace start-sender/receiver with `start-frontend` serving the `frontend/` root on port 3000.
