from pathlib import Path
from dataclasses import dataclass
from config import WEB_ROOT_BASE, HTML_INDEX_TEMPLATE, PHP_INDEX_TEMPLATE, BACKUP_DIR, NODEJS_APP_TEMPLATE, PM2_ECOSYSTEM_TEMPLATE
from utils.fs import ensure_dir, write_text, remove_path, backup_files
from services.nginx_service import write_http_config


@dataclass
class ProjectPaths:
    domain: str
    site_type: str
    project_root: Path
    public_root: Path


HTML_SAMPLE = HTML_INDEX_TEMPLATE.read_text(encoding="utf-8")
PHP_SAMPLE = PHP_INDEX_TEMPLATE.read_text(encoding="utf-8")
NODEJS_SAMPLE = NODEJS_APP_TEMPLATE.read_text(encoding="utf-8")
PM2_SAMPLE = PM2_ECOSYSTEM_TEMPLATE.read_text(encoding="utf-8")


def build_paths(domain: str, site_type: str) -> ProjectPaths:
    project_root = WEB_ROOT_BASE / domain
    if site_type in {"laravel", "ci4"}:
        public_root = project_root / "public"
    else:
        public_root = project_root
    return ProjectPaths(domain, site_type, project_root, public_root)


def create_project_files(domain: str, site_type: str, port: int = None) -> ProjectPaths:
    paths = build_paths(domain, site_type)
    ensure_dir(paths.public_root)

    if site_type == "html":
        write_text(paths.project_root / "index.html", HTML_SAMPLE.replace("{{ domain }}", domain))
    elif site_type == "php":
        write_text(paths.project_root / "index.php", PHP_SAMPLE.replace("{{ domain }}", domain))
    elif site_type == "laravel":
        write_text(paths.project_root / "README_SETUP.txt", laravel_notes(domain))
        write_text(paths.public_root / ".gitkeep", "")
    elif site_type == "ci4":
        write_text(paths.project_root / "README_SETUP.txt", ci4_notes(domain))
        write_text(paths.public_root / ".gitkeep", "")
    elif site_type == "nodejs":
        write_text(paths.project_root / "README_SETUP.txt", nodejs_notes(domain, port))
        write_text(paths.project_root / "app.js", NODEJS_SAMPLE.replace("{{ port }}", str(port)).replace("{{ domain }}", domain))
        write_text(paths.project_root / "ecosystem.config.cjs", PM2_SAMPLE.replace("{{ domain }}", domain))

    return paths


def create_site(domain: str, site_type: str, port: int = None) -> tuple[ProjectPaths, Path, Path]:
    paths = create_project_files(domain, site_type, port)
    available, enabled = write_http_config(domain, str(paths.public_root), site_type, port)
    return paths, available, enabled


def delete_site(root_path: str, nginx_available_path: str, nginx_enabled_path: str, domain: str) -> list[Path]:
    backups = backup_files(
        [Path(nginx_available_path), Path(root_path) / "README_SETUP.txt"],
        BACKUP_DIR,
        domain,
    )
    remove_path(Path(nginx_enabled_path))
    remove_path(Path(nginx_available_path))
    remove_path(Path(root_path))
    return backups


def laravel_notes(domain: str) -> str:
    return f"""Laravel placeholder untuk {domain}\n\nLangkah lanjutan:\n1. Upload / clone project Laravel ke {WEB_ROOT_BASE / domain}\n2. Pastikan document root mengarah ke folder public\n3. Install PHP, Composer, dan extension yang dibutuhkan\n4. Jalankan nginx -t lalu reload nginx\n5. Pasang SSL dengan certbot bila domain sudah resolve\n"""


def ci4_notes(domain: str) -> str:
    return f"""CodeIgniter 4 placeholder untuk {domain}\n\nLangkah lanjutan:\n1. Upload / clone project CI4 ke {WEB_ROOT_BASE / domain}\n2. Pastikan web root mengarah ke folder public\n3. Install PHP, Composer, dan extension yang dibutuhkan\n4. Jalankan nginx -t lalu reload nginx\n5. Pasang SSL dengan certbot bila domain sudah resolve\n"""

def nodejs_notes(domain: str, port: int) -> str:
    return f"""Node.js placeholder untuk {domain}\n\nLangkah lanjutan:\n1. Pastikan Node.js dan PM2 terinstall.\n2. Upload / clone project Node.js Anda ke {WEB_ROOT_BASE / domain}.\n3. Buka terminal, masuk ke direktori tersebut.\n4. Jalankan `npm install` jika ada dependencies.\n5. Jalankan `pm2 start ecosystem.config.cjs`.\n6. Jalankan `pm2 save` untuk menyimpan konfigurasi.\n7. Jalankan nginx -t lalu reload nginx.\n8. Pasang SSL dengan certbot bila domain sudah resolve.\n"""
