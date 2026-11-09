The first compose.yaml Ana wrote: plain `depends_on`, no health check. With it, `docker compose up -d` starts the
app before PostgreSQL accepts connections and the app exits with "Connection refused". lab/shop/compose.yaml is the
fixed version.
