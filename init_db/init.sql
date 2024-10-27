CREATE TABLE IF NOT EXISTS request_counts (
    server_name TEXT PRIMARY KEY,
    request_count INTEGER
);

INSERT INTO request_counts (server_name, request_count) VALUES ('webserver1', 0) ON CONFLICT (server_name) DO NOTHING;
INSERT INTO request_counts (server_name, request_count) VALUES ('webserver2', 0) ON CONFLICT (server_name) DO NOTHING;
