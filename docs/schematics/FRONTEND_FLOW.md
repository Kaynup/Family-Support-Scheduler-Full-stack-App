# Frontend Rendering & Logic Flow

This schematic details how the vanilla JavaScript frontend orchestrates data
fetching, state management, recurrence projections, and DOM updates.

## Interaction Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant UI as "DOM (index.html)"
    participant Orchestrator as "dashboard.js"
    participant APIClient as "api.js"
    participant State as "state.js"
    participant Engine as "utils.js (Projection)"
    participant Calendar as "calendar.js"
    
    Note over User, Calendar: Application Startup
    User->>UI: Opens localhost:8080
    UI->>Orchestrator: initDashboard()
    Orchestrator->>APIClient: fetchBills()
    APIClient-->>Orchestrator: JSON Response (Real DB Bills)
    Orchestrator->>State: setBills(data)
    
    Note over State, Calendar: The Rendering Cycle
    Orchestrator->>Calendar: renderCalendar(currentMonth)
    Calendar->>State: getBills()
    State-->>Calendar: [Real Bills Array]
    Calendar->>Engine: getProjectedBills(Real Bills, TargetMonth)
    Note over Engine: Calculates MONTHLY/WEEKLY instances<br/>for the current viewing month
    Engine-->>Calendar: [Virtual Bills Array]
    Calendar->>Calendar: Merge Real + Virtual Bills
    Calendar->>UI: Paint Days and Status Badges
    
    Note over User, Calendar: User Interaction
    User->>UI: Clicks "Mark as Paid" on a Bill
    UI->>Orchestrator: Event Listener Fired
    Orchestrator->>APIClient: putBillStatus(id, "PAID")
    APIClient-->>Orchestrator: 200 OK
    Orchestrator->>APIClient: fetchBills() (Re-sync State)
    APIClient-->>Orchestrator: Updated JSON Response
    Orchestrator->>State: setBills(Updated Data)
    Orchestrator->>Calendar: renderCalendar() (Trigger Re-render)
```

### Why This Architecture?
By centralizing state and treating the DOM purely as a reflection of that state, the application avoids "DOM-spaghetti." The calendar script doesn't know where the bills come from; it simply asks the state manager. The projection engine operates dynamically so the database never needs to store thousands of future recurring bills, saving massive amounts of disk space.
