# Frontend Structure Plan

## Goal

Keep frontend small, clear, and enough for current backend integration.

## Recommended Build Order

1. API client
2. Bills list page
3. Create bill form
4. Update status + delete actions
5. Basic loading/error states

## Proposed Hierarchical Structure

```text
frontend/
  src/
    api/
      client.js
      bills.js
    components/
      BillForm.jsx
      BillsTable.jsx
    features/
      bills/
        BillsPage.jsx
        useBills.js
    utils/
      format.js
    main.jsx
    App.jsx
    index.css
```

## File and Folder Explanations

### `api/`

- client.js: base request helper (`get`, `post`, `put`, `del`).
- bills.js: bill-specific API wrappers (`getBills`, `createBill`, `updateBillStatus`, `deleteBill`).

### `components/`

- BillForm.jsx: create bill form UI.
- BillsTable.jsx: render list of bills and action buttons.

### `features/bills/`

- BillsPage.jsx: compose list + form + actions in one screen.
- useBills.js: state and handlers for fetch/create/update/delete.

### `utils/`

- format.js: small formatters (date/amount) only if needed.

### `.`

- main.jsx: entrypoint mounts React app.
- App.jsx: top-level app container.
- index.css: minimal global styles.

## Rules to Keep It Clean

1. Keep API logic in `api/`, not inside JSX.
2. Keep one feature page first (`BillsPage.jsx`) until full CRUD works.
3. Extract reusable components only when duplication appears.
4. Avoid over-splitting files too early.