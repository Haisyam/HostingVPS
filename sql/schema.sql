CREATE TABLE IF NOT EXISTS sites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT NOT NULL UNIQUE,
    site_type TEXT NOT NULL,
    root_path TEXT NOT NULL,
    nginx_available_path TEXT NOT NULL,
    nginx_enabled_path TEXT NOT NULL,
    ssl_enabled INTEGER NOT NULL DEFAULT 0,
    cloudflare_proxied INTEGER NOT NULL DEFAULT 0,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
