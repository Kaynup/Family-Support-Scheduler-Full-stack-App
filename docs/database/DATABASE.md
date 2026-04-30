# Database Sub-system

## Engine

MySQL 8.0.45 running on WSL (Ubuntu-24.04).
Single database instance named `family_supp_sche`.

## Architecture

- Relational model with a single core table (`bills`).
- Connection pooling via `mysql.connector.pooling.MySQLConnectionPool`.
- Pool size is configurable through the `DB_CONN_POOLING` environment variable.
- All credentials (host, user, password, database name) are loaded from `.env` at startup.

## Connection Model

The system does not open ad-hoc connections per request.
Instead, a fixed-size pool is initialized once when the backend starts.
Every database operation checks out a connection from this pool, executes its query, and returns the connection immediately.

This avoids the overhead of repeated TCP handshakes with the MySQL server,
which matters when the frontend is making multiple rapid API calls (calendar rendering, search, status updates).

## Schema Management

The schema is managed through a single SQL file (`database/schema.sql`).
Running this file drops and recreates the table, then seeds it with test data.
There is no migration tool -- the schema file is the canonical source of truth.
