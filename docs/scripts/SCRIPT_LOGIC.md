# Script Logic and Execution Flow

This document details the internal logic, conditional branching, and API interactions
performed by the shell scripts. It focuses on the behavioral aspects rather than
the structural layout.

---

## 1. The Automation Engine Logic (`cron_simulator.sh`)

This script runs autonomously without user input. Its primary job is to fetch
state from the backend and determine whether an alert is necessary.

### Path Resolution

The script begins by securing its execution context:

    export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

1. **Path Export**: It hardcodes a safe `PATH`. Because this script is often run via
   `.bashrc` or potentially a system cron job, it cannot guarantee that the user's
   interactive `PATH` variables have been loaded. By explicitly defining the path,
   it ensures that standard utilities like `curl` and `jq` can be found.
2. **Directory Resolution**: It calculates the absolute path of the directory containing
   the script itself. This is critical because the script sources the `.env` file via
   `source "$SCRIPT_DIR/.env"`. If it simply used `source .env`, the script would
   crash if the user executed it from `~/` instead of from `~/InternshipProject/scripts/`.

### Network Execution and Timeouts

The script executes two identical `curl` commands against different endpoints:

    curl -s --max-time 2 "$API_BASE_URL/bills/..."

1. **Silent Mode**: The `-s` flag silences curl's progress meter, preventing it from
   printing network transfer statistics to the terminal.
2. **Hard Timeout**: The `--max-time 2` flag enforces a strict 2-second timeout on the
   network request. Because this script runs on shell login, a hanging network request
   would block the user from accessing their terminal prompt. The timeout ensures that
   even if the backend server is dead or unresponsive, the script will silently fail
   and return control to the user after exactly 2 seconds.

### Data Fetching and Evaluation

The script captures the parsed output of both API calls into Bash variables:
`$UPCOMING_BILLS` and `$EXPIRED_BILLS`.

The evaluation logic relies entirely on string length:

    if [ -n "$EXPIRED_BILLS" ] || [ -n "$UPCOMING_BILLS" ]; then

The `-n` operator tests if a string is non-empty.
If both strings are empty, it means the API returned zero results for both queries
(or the API request timed out and failed silently). In this case, the script jumps
to the `else` block and prints the "All caught up" message.

If either string contains data, the script enters the alert block. It then performs
a secondary check for each variable independently:

    if [ -n "$EXPIRED_BILLS" ]; then ... fi

This nested logic prevents the script from printing empty headers like
`[!!! EXPIRED BILLS !!!]` if there are upcoming bills but no expired bills.

---

## 2. Command Execution Logic

The command scripts in the `commands/` directory execute the active CRUD operations.

### Data Mutation: Creation (`add_bill.sh`)

This script implements the creation flow. It prompts for five variables:
`name`, `amount`, `due`, `tag` (category), and `interval` (recurrence).

**Type Coercion Logic**:
The backend API strictly requires the `total_amount` field to be a numeric float,
not a string. However, Bash `read` commands always capture input as strings.

To resolve this, the script delegates type coercion to `jq` during payload construction:

    total_amount: ($amount|tonumber)

The `|tonumber` filter instructs `jq` to parse the string variable passed via
`--arg amount "$amount"` and cast it to a JSON number type before serializing the payload.
If the user inputs "abc" instead of "500", `jq` will fail to parse it and the payload
will be invalid, protecting the backend from malformed data types.

The script then executes a POST request with the constructed payload and the
`Content-Type: application/json` header.

### Data Mutation: Update (`change_status.sh`)

This script implements the update flow. It prompts for two variables:
`id` and `status`.

The script executes the HTTP request using the PUT method, matching the
FastAPI backend's requirement for this endpoint.

    curl -s -X PUT "$API_BASE_URL/bills/$id"

FastAPI is highly strict regarding HTTP methods. By using the correct 
PUT method, the script ensures successful routing and state mutation.

### Argument Parsing and Defaults (`upcoming.sh`)

This script takes a positional parameter representing the number of days to look ahead.

**Fallback Logic**:
It uses bash parameter expansion to provide a default value:

    DAYS=${1:-3}

The `:-` operator checks if `$1` is unset or null. If it is, it assigns the default
value of `3` to the `DAYS` variable. If the user provides a value (e.g., `bash upcoming.sh 7`),
it assigns `7`.

This variable is then injected directly into the API endpoint URL:
`/bills/upcoming?days=$DAYS`.

---

## 3. Data Formatting Logic (`jq`)

The scripts do not use complex Bash string manipulation (`sed`, `grep`, `cut`) to parse
the JSON data. They offload all formatting logic to `jq`.

The standard parsing pipeline looks like this:

    jq -r '.data[] | " * \(.name) due on \(.due_date)"'

1. **Unwrapping**: `.data[]` takes the `data` array from the JSON response and unwraps
   it into a stream of individual objects.
2. **Piping**: The `|` operator inside the `jq` string passes each object in the stream
   to the formatting string.
3. **Interpolation**: `\(.fieldname)` extracts the value of the field from the object
   and inserts it directly into the string.
4. **Raw Output**: The `-r` flag tells `jq` to output the resulting strings as raw text
   without surrounding JSON quotes.

This approach is highly resilient. If the backend adds new fields to the response
in the future, the script will ignore them completely and continue formatting the output
correctly without breaking.
