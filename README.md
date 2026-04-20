# Family Support Scheduler 
Remittance isn't just about sending money; it's about fulfilling obligations. Migrant
workers frequently need to ensure specific bills back home (like rent, school tuition, or medical
bills) are paid on strict deadlines. Missing a date can have severe consequences.

---

## Objective
- Build a calendar-based scheduling tool specifically designed for
recurring family bills
- It allows users to: -
    - log upcoming expenses
    - categorize them
    - set strict due dates
    - manage their status (Paid vs. Unpaid)

---

## Functional Requirements
- Users log upcoming bills with strict due dates and Paid/Unpaid states.
- Bash script triggers backend API to alert for unpaid bills due in < 3 days.

---

## Tech stack
- Frontend: JavaScript (React Native), HTML5, CSS3.
- Backend: Python 3.10.20 (FastAPI v0.135.3).
- Database: MySQL (8.0.45)
- Automation: Native Linux Bash shell scripting

---

## Data Flow Architecture

```mermaid
flowchart TD
    A["Bash Script (Cron Job)"]
    B["Python API (Queries Dates)"]
    C{"Date < 3 Days?"}
    D["MySQL DB (Bills Table)"]
    E["Terminal Alert Generated"]

    A -->|Triggers| B
    B --> C
    C -->|Check| D
    D -->|Alerts| E

    %% Styling
    classDef primary fill:#6C5CE7,stroke:#3B3B98,color:#ffffff,stroke-width:2px;
    classDef secondary fill:#00CEC9,stroke:#008B8B,color:#ffffff,stroke-width:2px;
    classDef decision fill:#FDCB6E,stroke:#E17055,color:#2d3436,stroke-width:2px;
    classDef database fill:#55EFC4,stroke:#00B894,color:#2d3436,stroke-width:2px;
    classDef alert fill:#FF7675,stroke:#D63031,color:#ffffff,stroke-width:2px;

    class A primary;
    class B secondary;
    class C decision;
    class D database;
    class E alert;
```

---
