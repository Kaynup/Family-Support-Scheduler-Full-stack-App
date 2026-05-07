# API Endpoints and Schemas

## Schemas
Found in `app/schemas/`:
- **Auth**: `RegisterRequest`, `LoginRequest`, `TokenResponse`, `UserResponse`
- **Bills**: `BillCreateRequest`, `BillUpdateRequest`, `BillResponse`, `BillListResponse`
- **Remittance**: `RemittanceCreateRequest`, `RemittanceResponse`

## Routes
### Auth (`/auth`)
- `POST /register`: Registers a new user.
- `POST /login`: Authenticates and returns a JWT.

### Bills (`/bills`)
- `POST /new`: Create a bill (requires `beneficiary` role).
- `GET /search`: Search bills by name.
- `GET /all`: List all bills. Filterable by `upcoming_only` or `expired_only`.
- `PUT /{bill_id}`: Update bill status.
- `DELETE /{bill_id}`: Soft delete a bill (requires `beneficiary` role).

### Remittance (`/remittance`)
- `POST /pay`: Sender pays a bill via stablecoin (requires `sender` role).
- `GET /history`: Sender views outgoing payment history (requires `sender` role).
