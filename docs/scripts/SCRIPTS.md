# Scripts Sub-system

## Environment and Technology

The Scripts sub-system is built entirely on native Linux Bash shell scripting.
It requires a UNIX-like environment such as standard Linux distributions, macOS,
or Windows Subsystem for Linux (WSL).

The primary tools utilized within this environment are:
- `bash`: The Bourne Again SHell, which serves as the interpreter and execution engine.
- `curl`: The command-line tool used to transfer data across the network, specifically
  utilized here to make HTTP requests to the FastAPI backend.
- `jq`: A lightweight and flexible command-line JSON processor. It is used extensively
  to parse the JSON responses from the backend API, extract specific fields, and
  format the output into human-readable strings.
- `awk`: Used for simple text processing and string manipulation, particularly for
  extracting command arguments in the interactive shell.

There are no external dependencies beyond these standard UNIX utilities, meaning
the scripts are highly portable and do not require Python, Node.js, or any other
runtime environments to be installed globally.

## Architecture

The scripting layer serves two distinct purposes:
1. **Passive Automation**: Alerting the user of critical financial obligations
   without requiring active intervention.
2. **Active Management**: Providing a Command-Line Interface (CLI) to perform
   CRUD (Create, Read, Update, Delete) operations directly from the terminal.

These two purposes are reflected in the directory structure and file separation.
The passive automation logic is contained in a single script (`cron_simulator.sh`),
while the active management logic is split into an orchestrator (`main.sh`) and
several modular command scripts located in the `commands/` subdirectory.

The architecture is explicitly decoupled from the backend logic. The scripts do
not interact with the MySQL database directly. Instead, they act as HTTP clients,
exactly like the web frontend, communicating solely through the exposed REST API.
Ensure that all business logic (validation and soft deletion) 
remains centralized in the backend service layer.

## Connection Model

The scripts communicate with the backend via HTTP. The target endpoint is defined
in the root `.env` file of the project:

    API_BASE_URL="http://127.0.0.1:8000"

All script files resolve their absolute path and source this root environment
variable file. By isolating the base URL in a configuration file, the scripts
can be easily repointed from a local development server to a remote production
server without modifying any code.

This `.env` file is shared with the backend. The scripts dynamically compute
the path to the root `.env` to prevent redundant configuration files, ensuring
a single source of truth for all API routing.

## Automation Trigger Strategy

The `cron_simulator.sh` script is designed to run automatically. While it could
be scheduled using the standard Linux `cron` daemon, the preferred integration
strategy for this project is to execute it upon shell login.

By adding the script execution path to the user's `~/.bashrc` or `~/.profile`:
    
    # In ~/.bashrc
    /path/to/InternshipProject/scripts/cron_simulator.sh

The script runs synchronously every time the user opens a new terminal window or
tab. This guarantees high visibility -- developers and power users live in the
terminal, so they are virtually guaranteed to see the alert output during their
daily workflow.

This approach avoids the complexity of background process management and ensures
that alerts are delivered exactly when the user is looking at the screen, rather
than attempting to send system notifications that might be missed or suppressed.

## Extensibility

The CLI architecture in `main.sh` uses a simple `case` statement to route user
input to specific shell scripts. Because each command is isolated in its own file
within the `commands/` directory, adding new functionality is trivial.

To implement a new feature (e.g., searching bills by category):
1. Create a new file `commands/search.sh`.
2. Add a new `case` match in `main.sh` that calls the new file.
3. Update the menu output string to list the new command.

This plugin-style architecture prevents `main.sh` from growing into an
unmaintainable monolith and keeps the responsibility of parsing user input
separate from the responsibility of making HTTP requests.
