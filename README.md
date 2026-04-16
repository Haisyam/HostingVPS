# VPS Website Manager

Project Python multi-file untuk membantu mengelola website di VPS Linux dengan Nginx.

## Fitur
- Menu interaktif berbasis terminal
- Simpan data website ke SQLite
- CRUD website
- Generate folder project berdasarkan nama domain
- Generate config Nginx untuk:
  - HTML statis
  - PHP biasa
  - Laravel
  - CodeIgniter 4
- Hapus website dengan bersih:
  - folder project
  - config nginx di `sites-available`
  - symlink di `sites-enabled`
- Halaman contoh otomatis untuk HTML dan PHP
- Panduan SSL Certbot / Cloudflare

## Struktur direktori
```text
vps_site_manager/
├── app.py
├── config.py
├── db.py
├── README.md
├── requirements.txt
├── data/
│   ├── backups/
│   └── sites.db
├── services/
│   ├── nginx_service.py
│   ├── project_service.py
│   ├── site_service.py
│   └── ssl_service.py
├── sql/
│   └── schema.sql
├── templates/
│   └── pages/
│       ├── html_index.html
│       └── php_index.php
├── ui/
│   ├── menu.py
│   └── styles.py
└── utils/
    ├── fs.py
    └── validators.py
```

## Jalankan
> Disarankan dijalankan sebagai root atau memakai sudo, karena project ini menulis ke `/var/www` dan `/etc/nginx`.

```bash
cd /path/ke/vps_site_manager
python3 app.py
```

## Alur penggunaan
1. Tambah website baru
2. Masukkan domain
3. Pilih jenis website
4. Aplikasi membuat:
   - folder project
   - file contoh sesuai tipe website
   - config nginx
   - symlink enable site
   - record SQLite
5. Jalankan menu `nginx -t`
6. Reload nginx
7. Arahkan DNS domain ke IP VPS
8. Jalankan certbot bila domain sudah resolve

## Catatan penting
- Untuk HTML dan PHP, file contoh otomatis dibuat.
- Untuk Laravel dan CI4, dibuat folder kosong + catatan setup.
- Config PHP memakai socket default:
  `/run/php/php8.3-fpm.sock`
  Ubah bila versi PHP kamu berbeda.
- Untuk SSL, gunakan menu panduan SSL.

## Saran deployment
- Domain di Cloudflare sebaiknya `DNS only` dulu saat menjalankan Certbot.
- Setelah sertifikat berhasil, ubah ke `Proxied` dan set mode SSL/TLS ke `Full (strict)`.
