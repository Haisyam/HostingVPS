from pathlib import Path
import subprocess
from config import NGINX_AVAILABLE, NGINX_ENABLED
from utils.fs import write_text


def available_config_path(domain: str) -> Path:
    return NGINX_AVAILABLE / domain


def enabled_config_path(domain: str) -> Path:
    return NGINX_ENABLED / domain


def render_http_config(domain: str, root_path: str, site_type: str) -> str:
    index_line = {
        "html": "index index.html;",
        "php": "index index.php index.html;",
        "laravel": "index index.php index.html;",
        "ci4": "index index.php index.html;",
    }[site_type]

    if site_type == "html":
        location_block = """
    location / {
        try_files $uri $uri/ =404;
    }
"""
    else:
        location_block = r"""
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php8.3-fpm.sock;
    }

    location ~ /\.ht {
        deny all;
    }
"""

    return f"""server {{
    listen 80;
    listen [::]:80;
    server_name {domain};

    root {root_path};
    {index_line}
{location_block}
}}
"""


def write_http_config(domain: str, root_path: str, site_type: str) -> tuple[Path, Path]:
    available = available_config_path(domain)
    enabled = enabled_config_path(domain)
    content = render_http_config(domain, root_path, site_type)
    write_text(available, content)
    if enabled.exists() or enabled.is_symlink():
        enabled.unlink()
    enabled.symlink_to(available)
    return available, enabled


def test_nginx() -> subprocess.CompletedProcess:
    return subprocess.run(["nginx", "-t"], capture_output=True, text=True)


def reload_nginx() -> subprocess.CompletedProcess:
    return subprocess.run(["systemctl", "reload", "nginx"], capture_output=True, text=True)
