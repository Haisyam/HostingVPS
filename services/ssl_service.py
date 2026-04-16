from config import LETSENCRYPT_LIVE


import subprocess
from ui.menu import info, error

def install_ssl(domain: str, proxied: bool) -> bool:
    mode = "Full (strict)" if proxied else "Direct / DNS only"
    cert_path = LETSENCRYPT_LIVE / domain / "fullchain.pem"
    key_path = LETSENCRYPT_LIVE / domain / "privkey.pem"
    
    info("1. Pastikan DNS domain sudah mengarah ke IP VPS.")
    info("2. Untuk proses awal certbot, disarankan set record ke DNS only terlebih dahulu.")
    print("Mempersiapkan instalasi Certbot...")
    
    try:
        subprocess.run(["apt-get", "update"], check=True)
        subprocess.run(["apt-get", "install", "certbot", "python3-certbot-nginx", "-y"], check=True)
        
        print("\n=== MENJALANKAN CERTBOT ===")
        print("Silakan ikuti instruksi pengisian email dan redirect di bawah ini secara manual:")
        subprocess.run(["certbot", "--nginx", "-d", domain], check=True)
        
        info(f"Sertifikat berhasil diinstal di {cert_path}")
        if proxied:
            info(f"Karena Anda memakai Cloudflare, pastikan set SSL/TLS mode di Cloudflare ke: {mode}")
        return True
    except subprocess.CalledProcessError as exc:
        error(f"Gagal menginstal SSL: {exc}")
        return False
