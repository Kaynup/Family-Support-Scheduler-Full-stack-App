# Automation Classes and Functions

## Scope
This area is script-driven. There are no custom classes here; the useful units are the executable entry points and their helper calls.

## Key Functions and Behaviors
- `ThreadingHTTPServer(...)` in `scripts/start_frontend.py` opens a static server on the first available port.
- `SimpleHTTPRequestHandler` serves the repository files directly from the current working directory.
- `server.serve_forever()` keeps the frontend server alive until interrupted.
- `source "$SCRIPT_DIR/../.env"` loads the API base URL for the shell alert script.
- `curl -s --max-time 2` fetches upcoming and expired bill lists with a short timeout.
- `jq -r` formats the API payloads into human-readable alert lines.

## Responsibilities
- `start_frontend.py` handles local hosting only; it does not transform frontend assets.
- `cron_simulator.sh` acts as a lightweight status reporter for due bills.
- Both scripts should stay small and should reuse the app's real API endpoints instead of duplicating logic.

## Notes
If the automation layer later grows reusable Python or shell helpers, document the new callables here with the same level of detail.