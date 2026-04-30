# UI Components and Layout

This document covers the structural HTML, the component hierarchy,
and the visual design tokens used across the frontend.

---

## Page Structure

### index.html -- Login Page

A minimal authentication screen with two input fields and a submit button.
The page uses the same styles.css as the dashboard but only renders a
single centered card (`.login-card` inside `.login-page`).

HTML structure:

    body
      main.login-page
        section.login-card
          h1 "Log In"
          form.login-form (action="dashboard.html", method="get")
            label + input#username (pattern="admin")
            label + input#password (pattern="password123")
            button[submit] "Submit"

The form uses HTML5 `pattern` attributes for client-side validation.
No JavaScript is involved on this page. The form submits as a standard
GET request, navigating to dashboard.html on success.

### dashboard.html -- Main Application

The primary interface. Contains the calendar, bill lists, search panel,
action buttons, and two modal dialogs.

HTML structure (top level):

    body
      main
        h1 "Bill Management System"
        div.controls (Logout link)
        div#status (status bar)
        div.dashboard-grid
          div.col-left
            aside.left-panel (Calendar)
            section.section-card (Due Bills)
          div.col-right
            aside.action-panel (Search + Actions)
            section.section-card (Paid Bills)
        div#create-modal.modal.hidden
        div#delete-modal.modal.hidden
      script[module] -> js/dashboard.js

---

## Dashboard Layout

The dashboard uses a two-column CSS Grid layout:

    .dashboard-grid
        grid-template-columns: 1fr 1fr

Left column:
- Calendar panel with month navigation, 7-column day grid, and status legend.
- Due Bills table showing UNPAID bills for the selected date.

Right column:
- Search panel with text input and search button.
- Action panel showing selected bill details and Mark PAID / Delete buttons.
- Paid Bills table showing PAID bills for the selected date.

Both columns use `align-items: start` so cards align to the top
rather than stretching to match the tallest sibling.

---

## Component Reference

### Status Bar (#status)

A single-line text element below the page title.
Updated dynamically by `ui.showStatus()` to display loading messages,
success confirmations, error descriptions, and contextual hints.

Located at: dashboard.html line 17.

### Calendar Panel

Contains three sub-components:

1. Calendar Header: Month/year label with previous and next buttons.
   The month label is updated by calendar.js on every render.
   Buttons trigger `calendar.changeMonth()` which modifies
   state.currentMonth and state.currentYear, then re-renders.

2. Calendar Grid (#calendar-grid): A 7-column CSS Grid.
   Generated entirely by JavaScript. Contains:
   - 7 header cells (S M T W T F S)
   - Empty padding cells for the first week offset
   - Day cells with click handlers, status classes, and glow effects

3. Calendar Legend: A row of colored dots with labels.
   Defined in static HTML. Five categories:

   | Color | Class | Dot Background | Dot Border | Label |
   | ----- | ----- | -------------- | ---------- | ----- |
   | Blue | .today | #eff6ff | #3b82f6 | Today |
   | Red | .glow | #fee2e2 | #ef4444 | Due |
   | Green | .glow-paid | #dcfce7 | #22c55e | Paid |
   | Orange | .glow-mixed | #ffedd5 | #f97316 | Both |
   | Black | .glow-expired | #f3f4f6 | #111827 | Expired |

### Bill Tables

Two identical table structures rendered by `ui.renderList()`:

- Due Bills (#bills): Shows UNPAID bills for the selected date.
  Includes a "+" add button row at the bottom that opens the create modal.

- Paid Bills (#paid-bills): Shows PAID bills for the selected date.
  No add button.

Table columns:

| Header | Data Source | Format |
| ------ | ---------- | ------ |
| Name | bill.name | Plain text |
| Category | bill.category | Plain text or "-" |
| Amount | bill.total_amount | "Rs." prefix |
| Due (Calendar) | bill.due_date | ISO date string |

Rows are clickable. Clicking a row calls `selectBill()` which updates
the action panel and highlights the row with the `.selected` class.

When no bills exist for a date, a single row spanning all 4 columns
displays the empty text message.

### Action Panel

Contains two sub-sections:

1. Search Panel: Text input (#search-input) and Search button (#search-btn).
   Results appear in #search-results-list using the same table format
   as the bill tables. Supports Enter key submission.

2. Bill Actions: A text paragraph (#selected-text) showing the selected
   bill's details, and two action buttons:
   - Mark PAID (#mark-paid): Toggles between PAID and UNPAID.
     Label changes dynamically based on current bill status.
   - Delete (#delete-bill): Opens the delete confirmation modal.
   Both buttons start disabled and are enabled when a real (non-projected)
   bill is selected.

### Create Bill Modal (#create-modal)

A centered overlay dialog with a form for creating new bills.
Contains five input fields:

| Field | Input Type | Name Attribute | Required | Notes |
| ----- | ---------- | -------------- | -------- | ----- |
| Name | text | name | YES | Placeholder: "Electricity Bill" |
| Amount | number | total_amount | YES | min=0, step=0.01 |
| Due Date | date | due_date | YES | min set to today by modal.js |
| Category | text | category | NO | Placeholder: "optional" |
| Recurring | select | recurring_interval | NO | Options: None, Weekly, Monthly |

The modal is shown by removing the `.hidden` class and hidden by adding it.
Clicking outside the modal content (on the backdrop) also closes it.
The close button (x) in the top-right corner is a separate click target.

When the modal opens, `setDueDateDefaults()` sets the due date input's
minimum to today and its default value to 3 days from today. The name
input receives focus automatically.

### Delete Confirmation Modal (#delete-modal)

A smaller centered overlay with:
- A heading "Delete Bill"
- A confirmation paragraph that dynamically includes the bill name
- Two buttons: Cancel (gray) and Delete (red)

The Cancel button and backdrop click close the modal without action.
The Delete button calls `handleConfirmDelete()` which executes the
API deletion and refreshes the bill list.

---

## CSS Design Tokens

### Typography

    Font family: Consolas, "Courier New", monospace
    Heading size: 1.4rem (h1), 1rem (h2), 0.9rem (calendar header)
    Body text: inherits from font shorthand

### Color Palette

    Background (page): #f7f9fc
    Background (card): #f8fafc
    Background (table header): #f1f5f9
    Background (white): #ffffff
    Text (primary): #0f172a
    Text (secondary): #64748b
    Text (link): #2563eb
    Border (default): #dbe2ea
    Border (subtle): #e2e8f0

### Spacing

    Page padding: 1.5rem
    Card padding: 1rem / 1.25rem
    Table cell padding: 0.9rem 1rem
    Button padding: 0.8rem 1rem / 0.65rem 0.9rem
    Grid gap: 1rem (dashboard), 4px (calendar)

### Border Radius

    Cards/panels: 16px
    Inputs/buttons: 12px
    Modal content: 18px
    Calendar days: 4px
    Add button: 999px (fully circular)

### Shadows

    Modal backdrop: rgba(15, 23, 42, 0.45)
    Modal content: 0 24px 60px rgba(15, 23, 42, 0.18)
    Calendar glow (due): 0 0 8px rgba(239, 68, 68, 0.6)
    Calendar glow (paid): 0 0 8px rgba(34, 197, 94, 0.6)
    Calendar glow (mixed): 0 0 8px rgba(249, 115, 22, 0.6)
    Calendar glow (expired): 0 0 8px rgba(17, 24, 39, 0.6)
    Calendar glow (today): 0 0 10px rgba(59, 130, 246, 0.8)

### Transitions

    Calendar header buttons: all 0.2s (hover state)

---

## Element ID Registry

All interactive elements are referenced by ID in ui.js.
The complete registry:

| ID | Element | Module Consumer |
| -- | ------- | --------------- |
| bills | div | ui.js (bill list container) |
| paid-bills | div | ui.js (paid list container) |
| status | div | ui.js (status bar) |
| selected-text | p | ui.js (action panel text) |
| mark-paid | button | ui.js, dashboard.js |
| delete-bill | button | ui.js, dashboard.js |
| create-bill-form | form | ui.js, dashboard.js |
| bill-due | input | ui.js, modal.js |
| create-modal | div | ui.js, modal.js, dashboard.js |
| close-create-modal | button | ui.js, dashboard.js |
| search-input | input | ui.js, dashboard.js |
| search-btn | button | ui.js, dashboard.js |
| search-results-list | div | ui.js, dashboard.js |
| calendar-grid | div | ui.js, calendar.js |
| calendar-month-year | span | ui.js, calendar.js |
| prev-month | button | ui.js, dashboard.js |
| next-month | button | ui.js, dashboard.js |
| delete-modal | div | ui.js, modal.js, dashboard.js |
| confirm-delete | button | ui.js, dashboard.js |
| cancel-delete | button | ui.js, dashboard.js |
| delete-confirm-text | p | dashboard.js (direct getElementById) |
