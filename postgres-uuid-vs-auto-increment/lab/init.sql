-- Runs once when each database server starts for the first time (docker-entrypoint-initdb.d).
CREATE ROLE ana LOGIN PASSWORD 'Crate-Digger-45';
GRANT pg_checkpoint TO ana;
CREATE DATABASE records OWNER ana;
