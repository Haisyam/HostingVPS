import subprocess
import shutil
from ui.menu import info, error

def is_php_installed() -> bool:
    return shutil.which("php") is not None

def install_php() -> bool:
    info("Menginstall PHP dan dependensi yang dibutuhkan...")
    try:
        subprocess.run(["apt-get", "update"], check=True)
        # Menyesuaikan dengan versi php 8.3 karena dibutuhkan nginx
        subprocess.run([
            "apt-get", "install", "-y", 
            "php8.3", "php8.3-fpm", "php8.3-mysql", 
            "php8.3-curl", "php8.3-gd", "php8.3-mbstring", 
            "php8.3-xml", "php8.3-bcmath", "php8.3-zip"
        ], check=True)
        return True
    except subprocess.CalledProcessError as exc:
        error(f"Gagal menginstall PHP: {exc}")
        return False
