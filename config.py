from pathlib import Path

APP_NAME = "VPS Website Manager"
APP_VERSION = "1.0.0"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "sites.db"
BACKUP_DIR = DATA_DIR / "backups"

WEB_ROOT_BASE = Path("/var/www")
NGINX_AVAILABLE = Path("/etc/nginx/sites-available")
NGINX_ENABLED = Path("/etc/nginx/sites-enabled")
LETSENCRYPT_LIVE = Path("/etc/letsencrypt/live")

SUPPORTED_SITE_TYPES = ["html", "php", "laravel", "ci4"]

HTML_INDEX_TEMPLATE = BASE_DIR / "templates" / "pages" / "html_index.html"
PHP_INDEX_TEMPLATE = BASE_DIR / "templates" / "pages" / "php_index.php"

DATA_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)
