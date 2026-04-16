from config import LETSENCRYPT_LIVE


def ssl_instructions(domain: str, proxied: bool) -> str:
    mode = "Full (strict)" if proxied else "Direct / DNS only"
    cert_path = LETSENCRYPT_LIVE / domain / "fullchain.pem"
    key_path = LETSENCRYPT_LIVE / domain / "privkey.pem"
    return f"""
Langkah SSL untuk {domain}
=========================
1. Pastikan DNS domain sudah mengarah ke IP VPS.
2. Untuk proses awal certbot, disarankan set record ke DNS only terlebih dahulu.
3. Jalankan:
   sudo apt update
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d {domain}
4. Saat ditanya redirect, pilih Redirect agar HTTP otomatis ke HTTPS.
5. Setelah berhasil, cek file sertifikat:
   {cert_path}
   {key_path}
6. Kalau memakai Cloudflare proxied, set SSL/TLS mode ke: {mode}
7. Uji konfigurasi:
   sudo nginx -t
   sudo systemctl reload nginx
   sudo ss -tulpn | grep ':80\\|:443'
""".strip()
