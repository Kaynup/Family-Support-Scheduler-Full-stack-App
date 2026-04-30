# Full Stack Architecture

This document illustrates the high-level system architecture and the full-stack
approach used by the Family Support Scheduler.

## System Level Architecture Diagram

```mermaid
flowchart TB
    subgraph Frontend ["Frontend Architecture (Vanilla JS)"]
        UI[HTML/CSS DOM]
        State[State Manager\nstate.js]
        API_Wrapper[API Fetch Wrapper\nrequestJson]
        Projection[Projection Engine\nutils.js]
        
        UI <--> State
        State --> Projection
        State <--> API_Wrapper
    end

    subgraph Backend ["Backend Architecture (FastAPI)"]
        Router[API Endpoints\napi_endpoints.py]
        Services[Business Logic\nbill_*.py]
        DAO[Data Access Object\nqueries.py]
        Pool[Connection Pool\nconnection.py]
        
        Router <--> Services
        Services <--> DAO
        DAO <--> Pool
    end

    subgraph Database ["Database Layer (MySQL)"]
        MySQL[(MySQL Engine)]
        BillsTable[bills Table]
        
        MySQL --> BillsTable
    end

    subgraph Automation ["Automation & Scripts (Bash)"]
        Cron[Cron Simulator\ncron_simulator.sh]
        CLI[Terminal UI\nmain.sh]
    end

    %% External Connections
    User((User)) -->|Browser Interacts| UI
    User -->|Terminal Interacts| CLI
    
    API_Wrapper <-->|HTTP JSON REST| Router
    CLI <-->|cURL REST| Router
    Cron -->|cURL REST| Router
    
    Pool <-->|TCP port 3306| MySQL
```

### Flow Explanation
1. **User Interaction**: The user can interact with the system via the browser UI or the terminal CLI.
2. **Frontend State**: The Vanilla JS frontend manages state centrally and calculates future recurring bills on-the-fly using the projection engine.
3. **Backend Routing**: FastAPI handles incoming HTTP requests from both the browser and the automation scripts.
4. **Service Isolation**: The backend relies heavily on service layers to separate HTTP routing from database operations.
5. **Persistence**: MySQL handles data persistence, accessed exclusively via a pooled connection manager.
