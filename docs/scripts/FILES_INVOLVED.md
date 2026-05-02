# Files Involved in the Scripts Sub-system

This document provides a detailed breakdown of every file located within the
`scripts/` directory, detailing its purpose, structural elements, and specific
execution context.

---

## 1. Top-Level Configuration and Orchestration

### `scripts/.env`

The environmental configuration file for the script layer.
- **Lines**: 1
- **Purpose**: Defines the `API_BASE_URL` variable.
- **Content**: `API_BASE_URL="http://127.0.0.1:8000"`
- **Usage**: Sourced by every executable script in the system using the
  `source` command. It decouples the API host and port from the execution logic,
  making the scripts portable across different development and production
  environments without requiring code edits.

### `scripts/main.sh`

The interactive Command-Line Interface (CLI) orchestrator.
- **Lines**: 66
- **Purpose**: Provides a menu-driven, interactive loop for managing bills
  directly from the terminal.
- **Execution Context**: Executed manually by the user (e.g., `bash scripts/main.sh`).
- **Structural Elements**:
  - `source ".env"`: Loads the API URL configuration.
  - `bash "commands/health.sh"`: Automatically performs an API health check
    immediately upon startup to verify backend connectivity.
  - Interactive Menu: Uses `echo` to print an ASCII-formatted menu listing commands
    (all, upcoming, add, delete, change, q/exit).
  - Infinite Loop (`while true`): Blocks execution and waits for user input using
    `read -r input`.
  - Command Routing (`case` statement): Evaluates the user input against string
    literals and routes execution to the corresponding script inside the
    `commands/` directory using `bash "commands/<script>.sh"`.
  - Argument Passing: For the `upcoming*` pattern, it uses `awk '{print $2}'`
    to extract the numerical argument and passes it to the underlying script.
- **Dependencies**: Depends entirely on the files located in the `commands/` directory.

### `scripts/cron_simulator.sh`

The headless automation and alert generator.
- **Lines**: 35
- **Purpose**: Silently fetches bill data and outputs a formatted alert to the terminal
  only when action is required, or a positive confirmation if clear.
- **Execution Context**: Executed autonomously, typically invoked by a shell profile
  hook (like `.bashrc`) upon login, or potentially by a system cron daemon.
- **Structural Elements**:
  - Path Safety: Exports a rigid `PATH` string to ensure `curl` and `jq` commands
    resolve correctly regardless of the environment's state.
  - Directory Resolution: Computes its own absolute path (`SCRIPT_DIR`) to
    reliably `source` the `.env` file even when executed from an arbitrary working directory.
  - Dual HTTP Requests: Executes two separate `curl` commands sequentially against
    the `/bills/upcoming?days=3` and `/bills/expired` endpoints. Implements a strict
    2-second timeout (`--max-time 2`) on both requests to prevent blocking terminal login.
  - Conditional Output: Checks string variables (`$EXPIRED_BILLS`, `$UPCOMING_BILLS`)
    using bash's `-n` test operator. It outputs distinct structural blocks based on
    which data is present, prioritizing expired bills.
  - Fallback Logging: Prints an "All caught up" message if the API returns no bills,
    providing positive confirmation that the script successfully executed.

---

## 2. Command Modules

These files reside in the `scripts/commands/` directory and implement specific
API interactions. They are predominantly invoked by the `main.sh` orchestrator.

### `scripts/commands/add_bill.sh`

Implements the creation workflow.
- **Lines**: 18
- **Purpose**: Prompts the user for details and creates a new bill record.
- **Execution Context**: Executed interactively via `main.sh`.
- **Workflow**:
  - Uses `read -p` to sequentially prompt the user for "Bill Name", "Amount",
    "Due Date", "Category", and "Recurring Interval".
  - Constructs a JSON payload using `jq -n` to safely interpolate the bash variables.
    Critically, it applies the `|tonumber` filter to convert the amount string into
    a JSON numeric type.
  - Executes a `curl -X POST` request to `/bills/new`, passing the payload as the data body.
  - Pipes the API response into `jq` for pretty-printing.

### `scripts/commands/change_status.sh`

Implements the status update workflow.
- **Lines**: 15
- **Purpose**: Modifies the payment status of an existing bill.
- **Execution Context**: Executed interactively via `main.sh`.
- **Workflow**:
  - Executes `bash -e "commands/upcoming.sh"` immediately upon startup. This
    provides the user with contextual information (bill IDs) before prompting.
  - Prompts the user for "Bill ID" and "Change Status (paid/unpaid)".
  - Constructs a minimal JSON payload containing only the `status` field.
  - Executes a `curl -X PUT` request to `/bills/$id`, matching the backend's
    strict requirement for this endpoint.

### `scripts/commands/delete_bill.sh`

Implements the deletion workflow.
- **Lines**: 6
- **Purpose**: Soft-deletes a specific bill record.
- **Execution Context**: Executed interactively via `main.sh`.
- **Workflow**:
  - Prompts the user for "Bill ID".
  - Executes a `curl -X DELETE` request to `/bills/$id` without a JSON body.
  - Pipes the API response into `jq` for pretty-printing.

### `scripts/commands/health.sh`

Implements the connectivity diagnostic check.
- **Lines**: 5
- **Purpose**: Verifies that the FastAPI backend server is reachable.
- **Execution Context**: Executed automatically during `main.sh` startup, or manually.
- **Workflow**:
  - Prints a "[Health Check]" header.
  - Executes a simple `curl` GET request to the `/health` endpoint.
  - Pipes the `{ "message": "backend is live" }` JSON response through `jq`.

### `scripts/commands/list_all.sh`

Implements the full dataset retrieval workflow.
- **Lines**: 6
- **Purpose**: Retrieves and formats all active bills in the system.
- **Execution Context**: Executed interactively via `main.sh`.
- **Workflow**:
  - Executes a `curl` GET request to `/bills/all`.
  - Uses a complex `jq` filter to iterate over `.data[]` and format the fields
    into a structured string containing the ID, name, total amount (prefixed
    with the ₹ symbol), and due date.

### `scripts/commands/upcoming.sh`

Implements the filtered dataset retrieval workflow.
- **Lines**: 9
- **Purpose**: Retrieves bills due within a specific time window.
- **Execution Context**: Executed interactively via `main.sh`, or invoked internally
  by `change_status.sh`.
- **Workflow**:
  - Defines the `$DAYS` variable using parameter expansion `DAYS=${1:-3}` to provide
    a default lookahead window of 3 days if no argument is supplied.
  - Prints a dynamic header incorporating the lookahead window: "[Upcoming Bills in N days]".
  - Executes a `curl` GET request to `/bills/upcoming?days=$DAYS`.
  - Formats the output using `jq` into strings detailing the name, due date, and amount.
