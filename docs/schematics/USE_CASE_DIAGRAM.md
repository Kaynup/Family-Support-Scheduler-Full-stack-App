# System Use Cases

This document defines the primary actors and their interactions with the
Family Support Scheduler system.

## Use Case Diagram

```mermaid
usecaseDiagram
    actor FamilyMember as "Family Member\n(Browser User)"
    actor SystemAdmin as "System Admin\n(Terminal User)"
    actor CronDaemon as "Cron/System Timer\n(Automation)"
    
    package "Family Support Scheduler System" {
        usecase "View Calendar Dashboard" as UC1
        usecase "Add New Bill" as UC2
        usecase "Update Bill Status\n(Mark as Paid)" as UC3
        usecase "Delete Bill" as UC4
        usecase "Search Bills by Name" as UC5
        usecase "Trigger Auto-Recurrence" as UC6
        usecase "Receive Upcoming/Expired Alerts" as UC7
    }
    
    %% Browser User Interactions
    FamilyMember --> UC1
    FamilyMember --> UC2
    FamilyMember --> UC3
    FamilyMember --> UC4
    FamilyMember --> UC5
    
    %% Admin Interactions
    SystemAdmin --> UC2
    SystemAdmin --> UC3
    SystemAdmin --> UC4
    SystemAdmin --> UC7
    
    %% Automated Interactions
    CronDaemon --> UC7
    
    %% Internal System Includes
    UC3 ..> UC6 : "<<includes>> (If recurring)"
```

### Actor Descriptions

1. **Family Member (Browser User)**: The primary end-user interacting with the graphical interface. They rely on visual cues (the calendar) to manage the household budget.
2. **System Admin (Terminal User)**: A power-user interacting directly with the Bash scripts (`main.sh`) to quickly alter state without needing a web browser.
3. **Cron/System Timer**: An automated actor responsible for executing `cron_simulator.sh` at set intervals to push notifications to the host machine regarding upcoming dues.

### Key Use Cases

- **Trigger Auto-Recurrence**: This is a backend-driven use case. When a user executes "Update Bill Status", the system automatically checks if the bill is recurring. If so, it silently creates the next cycle's bill.
- **Receive Alerts**: Driven by the automation actor, surfacing critical financial deadlines directly to the system's terminal/stdout.
