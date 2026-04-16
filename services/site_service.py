from dataclasses import asdict, dataclass
from typing import Optional

from db import get_connection


@dataclass
class SiteRecord:
    id: int | None
    domain: str
    site_type: str
    root_path: str
    nginx_available_path: str
    nginx_enabled_path: str
    ssl_enabled: int = 0
    cloudflare_proxied: int = 0
    notes: str | None = None
    created_at: str | None = None
    updated_at: str | None = None



def create_site_record(record: SiteRecord) -> int:
    with get_connection() as conn:
        cur = conn.execute(
            """
            INSERT INTO sites (
                domain, site_type, root_path, nginx_available_path, nginx_enabled_path,
                ssl_enabled, cloudflare_proxied, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.domain,
                record.site_type,
                record.root_path,
                record.nginx_available_path,
                record.nginx_enabled_path,
                record.ssl_enabled,
                record.cloudflare_proxied,
                record.notes,
            ),
        )
        conn.commit()
        return int(cur.lastrowid)



def list_sites() -> list[SiteRecord]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM sites ORDER BY created_at DESC").fetchall()
    return [SiteRecord(**dict(row)) for row in rows]



def get_site_by_id(site_id: int) -> Optional[SiteRecord]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM sites WHERE id = ?", (site_id,)).fetchone()
    return SiteRecord(**dict(row)) if row else None



def get_site_by_domain(domain: str) -> Optional[SiteRecord]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM sites WHERE domain = ?", (domain,)).fetchone()
    return SiteRecord(**dict(row)) if row else None



def update_site_metadata(site_id: int, ssl_enabled: int, cloudflare_proxied: int, notes: str | None) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE sites
            SET ssl_enabled = ?, cloudflare_proxied = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (ssl_enabled, cloudflare_proxied, notes, site_id),
        )
        conn.commit()



def delete_site_record(site_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM sites WHERE id = ?", (site_id,))
        conn.commit()
