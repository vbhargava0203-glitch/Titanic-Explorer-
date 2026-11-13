-- Run once as the database administrator. No password is stored in this file.
-- If this role already exists, inspect its privileges before reusing it.
BEGIN;
CREATE ROLE titanic_app LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;
GRANT CONNECT ON DATABASE titanic_db TO titanic_app;
GRANT USAGE ON SCHEMA titanic_project TO titanic_app;
GRANT SELECT ON ALL TABLES IN SCHEMA titanic_project TO titanic_app;
ALTER ROLE titanic_app SET search_path TO titanic_project, public;
ALTER ROLE titanic_app SET default_transaction_read_only TO on;
ALTER ROLE titanic_app SET statement_timeout TO '5s';
COMMIT;
-- Next, in an interactive psql session: \password titanic_app
