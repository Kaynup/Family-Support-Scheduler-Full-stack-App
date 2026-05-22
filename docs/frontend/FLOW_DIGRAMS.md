# Frontend Flow Digrams

## Login Flow
```mermaid
flowchart TD
  A[Open login.html] --> B[Load shared CSS]
  B --> C[Submit credentials]
  C --> D[POST /auth/login]
  D --> E[Store token, role, username]
  E --> F[Redirect to sender or receiver dashboard]
```

## Sender Dashboard Flow
```mermaid
flowchart TD
  A[Open sender dashboard] --> B[guardRoute requires sender]
  B --> C[Load shared UI helpers]
  C --> D[Fetch bills, upcoming bills, and beneficiaries]
  D --> E[Render calendar and bills table]
  E --> F[Select bill]
  F --> G[Open pay modal]
  G --> H[POST /remittance/pay]
  H --> I[Refresh bills and history]
```

## Receiver Dashboard Flow
```mermaid
flowchart TD
  A[Open receiver dashboard] --> B[guardRoute requires beneficiary]
  B --> C[Fetch bills]
  C --> D[Render calendar and beneficiary bill table]
  D --> E[Search, create, or delete bills]
  E --> F[Open action modal or success modal]
  F --> G[Refresh table after mutation]
```

## Notes
Keep the diagrams tied to the actual page scripts, especially when the sender and receiver dashboards diverge.