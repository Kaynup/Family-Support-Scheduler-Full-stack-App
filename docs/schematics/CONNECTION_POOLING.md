# Database Connection Pooling

This schematic demonstrates how connection pooling protects the MySQL database
from connection exhaustion and reduces query latency.

## Connection Lifecycle Diagram

```mermaid
sequenceDiagram
    participant API as "FastAPI Router"
    participant Pool as "ConnectionPool (Size=5)"
    participant MySQL as "MySQL Database"
    
    Note over API, MySQL: Initialization Phase (Server Startup)
    Pool->>MySQL: Open Connection 1
    Pool->>MySQL: Open Connection 2
    Pool->>MySQL: Open Connection 3
    Pool->>MySQL: Open Connection 4
    Pool->>MySQL: Open Connection 5
    Note over Pool: 5 connections held open in memory
    
    Note over API, MySQL: Request 1: User Loads Dashboard
    API->>Pool: Request connection()
    Pool-->>API: Returns Connection 1 (Instant)
    API->>MySQL: SELECT * FROM bills
    MySQL-->>API: Returns Data
    API->>Pool: Releases Connection 1 (Does NOT close)
    
    Note over API, MySQL: Request 2 & 3: Parallel Requests
    API->>Pool: Request connection (Req A)
    API->>Pool: Request connection (Req B)
    Pool-->>API: Returns Connection 1 & 2
    API->>MySQL: Concurrent Queries Executed
    MySQL-->>API: Concurrent Results
    API->>Pool: Releases Connection 1 & 2
```

### Why Pooling Helps
1. **TCP Overhead Elimination**: A standard `mysql.connector.connect()` call requires establishing a new TCP handshake and authenticating credentials. Pooling performs this expensive operation once at server startup.
2. **Concurrency Management**: If 10 users click "Add Bill" at the exact same millisecond, the connection pool prevents the database from being flooded with 10 simultaneous connection requests. It acts as a throttle, utilizing the 5 available connections and queueing the rest, preventing `Too many connections` crashes.
