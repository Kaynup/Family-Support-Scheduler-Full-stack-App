# Automation and Command Line Interface

This document covers the structural design and interface points of the
terminal-based features provided by the scripts sub-system.

---

## 1. The Automation Output Format

The `cron_simulator.sh` script produces text output intended for terminal
consumption. The design philosophy of this output is **high contrast and
immediate readability**.

### Structure of the Alert

The output is framed by dashed lines to visually separate it from other
terminal text (like shell initialization messages or the command prompt).

    --------------------------------------------------------------------------
    [FAMILY SUPPORT SCHEDULER] ALERT: BILLS NEED ATTENTION!
    
    [!!! EXPIRED BILLS !!!]
    Water Bill was due on 2026-04-30 | Rs.300.75
    
    [Upcoming Due Bills]
    Internet Bill due on 2026-05-01 | Rs.999.00
    --------------------------------------------------------------------------

The alert is strictly categorized.
- The `[!!! EXPIRED BILLS !!!]` section uses aggressive punctuation to draw the eye.
  These bills have already passed their deadline and require immediate action.
  The phrasing "was due on" emphasizes the past tense.
- The `[Upcoming Due Bills]` section is informational. These bills are within
  the 3-day warning window but are not yet overdue.
  The phrasing "due on" emphasizes the impending deadline.

### Positive Reinforcement State

If the backend reports that there are zero expired bills AND zero upcoming bills,
the script does not remain silent. Silent success is ambiguous -- the user
cannot distinguish between "everything is fine" and "the script failed to run."

Instead, it prints a positive confirmation message:

    [FAMILY SUPPORT SCHEDULER] All caught up! No upcoming or expired bills found.

This structural decision ensures confidence in the system's operational status.

---

## 2. The Interactive CLI (`main.sh`)

The `main.sh` script provides a text-based, infinite-loop menu system.
It acts as a complete alternative to the web-based `dashboard.html`.

### Menu Presentation

Upon execution, the user is greeted with an ASCII-art style box displaying
the available commands:

    ============ Bill Management System ============
    
    [Health Check]
    { ... backend status JSON ... }
    +--------------------------------------------+
    
    [Commands]
    +--------------------------------------------+
    | all            - View all bills            |
    | upcoming <n>   - Upcoming bills in n days  |
    | add            - Create new bill           |
    | delete         - Delete a bill             |
    | change         - Change bill status        |
    | q / exit       - Quit                      |
    +--------------------------------------------+

### Command Execution Loop

The script drops the user into an interactive prompt:

    Enter command:

The input string is evaluated against a fixed set of patterns.
- Explicit keywords (`all`, `add`, `delete`, `change`) trigger specific modules.
- Wildcard prefixes (`upcoming*`) allow for argument passing.
- Exit keywords (`q`, `exit`) break the loop and terminate the script.
- Unrecognized input prints an "Invalid command" warning and reprints a compact
  version of the menu.

Because the loop uses the `read` command, the interface blocks and waits indefinitely
for user input. It does not consume CPU cycles while waiting.

### Argument Parsing Structure

The `upcoming` command demonstrates the sub-system's argument parsing strategy:

    upcoming <n>

The user inputs the command and the argument as a single string (e.g., "upcoming 7").
The `main.sh` loop captures this entire string into the `$input` variable.
To separate the argument, it pipes the string into `awk`:

    days=$(echo "$input" | awk '{print $2}')

This extracts the second word from the string. The extracted variable is then passed
as a positional parameter (`$1`) to the `commands/upcoming.sh` script.
If the user omits the argument (types just "upcoming"), `awk` returns an empty string,
and the downstream script applies a default value.

---

## 3. The Command Modules

The scripts in the `commands/` directory follow a consistent interface pattern
designed for terminal interaction.

### Informational Modules (`list_all.sh`, `upcoming.sh`)

These modules do not require interactive input. They execute immediately when called.
They produce bulleted lists designed for quick scanning:

    [All Bills]
     * ID : 1       Electricity Bill       ₹1200.5          due: 2026-04-29
     * ID : 2       Water Bill             ₹300.75          due: 2026-04-30

The output format is heavily standardized across the system. It aligns columns
using spaces and uses the Indian Rupee symbol (₹) for currency, which differs
from the frontend's "Rs." prefix.

### Interactive Modules (`add_bill.sh`, `change_status.sh`, `delete_bill.sh`)

These modules perform destructive or mutative actions (Create, Update, Delete).
Therefore, they pause execution and prompt the user for data using `read -p`.

Example from `add_bill.sh`:
    Bill Name:
    Amount:
    Due Date (YYYY-MM-DD):
    Category of bill:

This sequential prompting simulates an HTML form submission workflow within the CLI.
The user must type the value and press Enter for each field.

### Dependency Injection

A structural feature of the `change_status.sh` script is that it executes
another script before prompting the user:

    bash -e "commands/upcoming.sh"

This is a form of functional composition. By running the upcoming bills script
first, it provides context. The user immediately sees the list of bills and their
IDs, eliminating the need to memorize or look up an ID before entering it into
the prompt.

### The JSON Parsing Pattern

The sub-system relies entirely on `jq` to bridge the gap between Bash and the
FastAPI backend.

When reading data, it pipes the `curl` output into `jq` with the `-r` (raw) flag:
    jq -r '.data[] | " * \(.name) due on \(.due_date)"'

This extracts the array, iterates over every object, interpolates specific fields
into a string format, and prints the result without JSON quotes.

When writing data, it uses `jq -n` (null input) to construct a JSON payload
from bash variables:
    jq -n --arg name "$name" '{name: $name}'

This technique is vastly superior to manually concatenating strings in Bash,
as `jq` automatically handles proper quoting, escaping, and type conversion
(like `|tonumber`), preventing malformed JSON errors from crashing the backend.
