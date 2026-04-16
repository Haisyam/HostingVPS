from pathlib import Path
from dataclasses import dataclass
from config import WEB_ROOT_BASE, HTML_INDEX_TEMPLATE, PHP_INDEX_TEMPLATE, BACKUP_DIR
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


def build_paths(domain: str, site_type: str) -> ProjectPaths:
    project_root = WEB_ROOT_BASE / domain
    if site_type in {"laravel", "ci4"}:
        public_root = project_root / "public"
    else:
        public_root = project_root
    return ProjectPaths(domain, site_type, project_root, public_root)


def create_project_files(domain: str, site_type: str) -> ProjectPaths:
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

    return paths


def create_site(domain: str, site_type: str) -> tuple[ProjectPaths, Path, Path]:
    paths = create_project_files(domain, site_type)
    available, enabled = write_http_config(domain, str(paths.public_root), site_type)
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
