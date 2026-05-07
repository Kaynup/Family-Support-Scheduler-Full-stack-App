You are refactoring and redesigning an existing full-stack bill management application into a scalable, maintainable, multi-user remittance platform. Your primary objective is NOT feature expansion first — it is reducing redundancy, improving architectural clarity, separating responsibilities properly, and making the codebase easy to navigate and extend.

The project already has an existing frontend design and UI identity. While refactoring the architecture completely, you MUST preserve the current frontend tone, UI style, look and feel, user experience patterns, visual simplicity, and overall aesthetic consistency. Do NOT redesign the UI unnecessarily.

========================================================
CORE PRIORITIES
========================================================

1. Refactor the full-stack architecture to eliminate redundancy.
2. Reduce frontend-heavy logic.
3. Create clean modular architecture with high cohesion and low coupling.
4. Preserve the current frontend design language and UX.
5. Avoid overly complex logic, deeply nested abstractions, or unnecessarily advanced patterns.
6. Make the project beginner-friendly, maintainable, readable, scalable, and easy to debug.
7. Prepare the application for real-world remittance workflows involving multiple family members.

========================================================
ENGINEERING PRINCIPLES (VERY IMPORTANT)
========================================================

Apply these principles strictly during refactoring:

1. High Cohesion
   - Keep related logic grouped together.
   - Each module/file should have one clear responsibility.
   - Example:
     - bill creation logic stays together
     - authentication logic stays together
     - remittance transaction logic stays together

2. Low Coupling
   - Modules should remain as independent as possible.
   - Changing one module should not break unrelated modules.
   - Avoid tight dependencies between frontend pages or backend services.

3. Simplicity First
   - Do NOT use unnecessarily complex patterns.
   - Avoid overengineering.
   - Prefer readable and explicit code over clever abstractions.
   - Keep functions small and understandable.
   - Keep state management minimal.

4. Minimalistic but Proper
   - Build clean architecture without making the project enterprise-overcomplicated.
   - Focus on maintainability and clarity.

========================================================
PHASE 1 — STRUCTURAL BACKEND REFACTORING
========================================================

Refactor the backend BEFORE implementing advanced remittance functionality.

Backend Refactor Requirements:

1. Create a `core/` module:
   - `config.py`
   - `exceptions.py`

2. Create `constants.py`
   - Store reusable constants and magic strings
   - Example:
     STATUS_UNPAID = "UNPAID"

3. Replace monolithic query architecture:

Replace:
db/queries.py

With:
queries/
├── insert.py
├── select.py
├── update.py
└── delete.py

4. Implement database connection context manager:

Create:
db/connection.py

Responsibilities:
- open connection
- cursor handling
- commit/rollback
- safe cleanup
- close connection

5. Refactor all DB operations to use the context manager.

6. Modularize tests:

tests/
├── test_db/
├── test_services/
└── test_api/

========================================================
PHASE 2 — DUAL PANEL REMITTANCE ARCHITECTURE
========================================================

The application must support TWO independent frontend panels running on different ports for demo purposes.

Example:
- receiver panel → localhost:3000
- sender panel → localhost:3001

This simulates multiple users using the application simultaneously.

========================================================
REAL-WORLD REMITTANCE SCENARIO
========================================================

Scenario:
- A family is located in India.
- Multiple family members can exist in the system.
- One user acts as the Sender/Remitter (possibly abroad).
- Other users act as Beneficiaries/Family Members.
- Beneficiaries create bills.
- Sender views and pays those bills using remittance flow.
- Multiple users should be able to login simultaneously during demo/testing.

The architecture should support this cleanly and minimally.

========================================================
FRONTEND STRUCTURE
========================================================

frontend/
├── receiver_panel/
│   ├── pages/
│   ├── css/
│   └── js/
│       ├── config.js
│       └── core/
│
└── sender_panel/
    ├── pages/
    ├── css/
    └── js/
        ├── config.js
        └── core/

========================================================
PANEL RESPONSIBILITIES
========================================================

Receiver Panel (Beneficiaries / Family Members):
- Login/Register
- Create bills
- Edit/Delete bills
- Manage bills/calendar
- View payment history
- View remittance status

Sender Panel (Remitter):
- Login/Register
- View beneficiary bills
- View calendar/history
- Pay bills through remittance flow
- Cannot create bills

========================================================
AUTHENTICATION REQUIREMENTS
========================================================

The current authentication UI may already exist but is NOT connected to the backend yet.

You may either:
- enhance the existing auth flow properly
OR
- rebuild it minimally and cleanly

Requirements:
- Proper backend-connected authentication
- Login functionality
- Signup/Register functionality
- Session/token-based authentication
- Multiple users can login simultaneously
- Role distinction:
   - sender
   - beneficiary

Backend Requirements:
- users table
- password hashing
- role management
- authentication APIs
- protected routes where necessary

Keep the implementation simple, clean, and maintainable.

========================================================
REMITTANCE & STABLECOIN FLOW
========================================================

The remittance system should conceptually support stablecoin-based transfers.

The implementation does NOT need overly complex blockchain infrastructure unless necessary.

Goal:
- Simulate or structure a remittance payment flow where:
   Sender → pays bill → remittance transaction recorded

Suggested approach:
- Abstract stablecoin/remittance layer cleanly
- Keep it modular for future expansion
- Avoid overengineering blockchain logic right now

Suggested DB Table:
remittance_transactions

Fields:
- transaction_id
- bill_id
- sender_user_id
- beneficiary_user_id
- amount
- currency/stablecoin_type
- transaction_status
- payment_method
- created_at

========================================================
PHASE 3 — CONVERT SPA TO MULTI-PAGE APPLICATION
========================================================

The current frontend is too stuffed with logic.

Convert it from SPA-style hidden sections into a clean Multi-Page Application (MPA).

Required Pages:
- index.html
- login.html
- register.html
- dashboard.html
- bills.html
- create.html
- history.html

Requirements:
- Each page loads ONLY the JS it needs
- Remove giant dashboard.js files
- Avoid excessive hide/show div logic
- Use real browser navigation

Example:
create.html should only load:
- form validation
- bill creation logic

========================================================
PHASE 4 — FRONTEND VS BACKEND RESPONSIBILITY SPLIT
========================================================

The application is currently frontend-heavy.

Move ALL heavy business logic to backend APIs.

========================================================
BACKEND RESPONSIBILITIES
========================================================

The backend should handle:

1. Filtering
   Example:
   /bills?month=May&sort=desc

2. Sorting

3. Aggregations
   Example:
   SQL SUM() for totals

4. Complex validations
   - prevent deleting paid bills
   - validate remittance amounts

5. Pagination

6. Role-based access checks

7. Remittance transaction handling

========================================================
FRONTEND RESPONSIBILITIES
========================================================

The frontend should ONLY handle:

1. Basic input validation
2. UI rendering
3. Modals/loading states
4. Calendar rendering
5. Navigation/routing
6. Small local UI states

Avoid:
- large frontend data processing
- frontend-heavy filtering/sorting
- duplicated business rules

========================================================
REFACTORING RULES
========================================================

1. Avoid duplicated logic everywhere.
2. Keep functions short and readable.
3. Prefer modular files over giant files.
4. Keep architecture scalable but simple.
5. Maintain existing UI tone and aesthetics.
6. Reduce cognitive overload in the codebase.
7. Use backend-centric business processing.
8. Avoid unnecessary dependencies.
9. Make variables/functions easy to locate instantly.
10. Improve developer ergonomics and debugging experience.

========================================================
EXPECTED FINAL OUTCOME
========================================================

The final project should:

- Preserve the current frontend appearance and feel
- Be modular and easy to navigate
- Have minimal redundancy
- Use clean high-cohesion low-coupling architecture
- Support multiple simultaneous users
- Support sender-beneficiary remittance workflow
- Have backend-connected authentication
- Support stablecoin/remittance transaction structure
- Use lightweight frontend logic
- Be easy to debug, extend, and maintain
- Be scalable for future production-level growth
- Remain simple enough to understand and demo confidently