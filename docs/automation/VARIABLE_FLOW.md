# Automation Variable Flow

## Scope
This folder contains the repo's local automation entry points:
- `scripts/start_frontend.py`
- `scripts/cron_simulator.sh`

## Real Variables
- `START` and `END` in `start_frontend.py` define the port search range `8001..8010`.
- `SCRIPT_DIR` in `cron_simulator.sh` resolves the script location before sourcing `.env`.
- `API_BASE_URL` comes from the repository `.env` file and is used for curl requests.
- `UPCOMING_BILLS` and `EXPIRED_BILLS` store formatted alert output from the API responses.
- `PATH` is reset in the shell script so standard tools like `curl` and `jq` resolve predictably.

## Flow
1. `start_frontend.py` loops through the port range and starts `ThreadingHTTPServer` on the first free port.
2. `cron_simulator.sh` sources `.env`, then calls `/bills/upcoming?days=3` and `/bills/expired`.
3. The shell script formats results with `jq` and prints either an alert block or a clean status message.
4. The scripts exit with non-zero status when no free port is available or if the process is interrupted.

## Notes
Keep this file focused on runtime variables and script inputs/outputs, not business logic.