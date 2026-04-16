from db import init_db
from services.project_service import create_site, delete_site
from services.site_service import (
    SiteRecord,
    create_site_record,
    delete_site_record,
    get_site_by_id,
    list_sites,
    update_site_metadata,
)
from services.nginx_service import test_nginx, reload_nginx
from services.ssl_service import install_ssl
from ui.menu import banner, clear_screen, error, info, main_menu, pause, section, success, warn
from utils.validators import is_valid_domain, yes_no


def prompt_site_type() -> str:
    choices = {"1": "html", "2": "php", "3": "laravel", "4": "ci4"}
    while True:
        section("PILIH JENIS WEBSITE")
        print("1. HTML statis")
        print("2. PHP biasa")
        print("3. Laravel")
        print("4. CodeIgniter 4")
        value = input("Pilihan: ").strip()
        if value in choices:
            return choices[value]
        error("Pilihan tidak valid.")


def add_site_flow() -> None:
    section("TAMBAH WEBSITE BARU")
    domain = input("Masukkan domain (contoh: info.haisyam.dev): ").strip().lower()
    if not is_valid_domain(domain):
        error("Format domain tidak valid.")
        return

    site_type = prompt_site_type()

    if site_type in {"php", "laravel", "ci4"}:
        from services.php_service import is_php_installed, install_php
        if not is_php_installed():
            if yes_no(input("PHP belum terinstall. Apakah Anda ingin menginstallnya sekarang? [y/n]: ")):
                install_php()
            else:
                warn("PHP tidak diinstall. Website mungkin tidak berfungsi tanpa PHP.")

    notes = input("Catatan opsional: ").strip() or None

    try:
        paths, available, enabled = create_site(domain, site_type)
        site_id = create_site_record(
            SiteRecord(
                id=None,
                domain=domain,
                site_type=site_type,
                root_path=str(paths.project_root),
                nginx_available_path=str(available),
                nginx_enabled_path=str(enabled),
                notes=notes,
            )
        )
        success(f"Website berhasil dibuat dengan ID {site_id}.")
        info(f"Folder project : {paths.project_root}")
        info(f"Web root      : {paths.public_root}")
        info(f"Nginx config  : {available}")
        info("Langkah berikutnya: cek DNS domain, jalankan nginx -t, lalu reload nginx.")
    except Exception as exc:
        error(f"Gagal membuat website: {exc}")



def display_sites_table() -> bool:
    rows = list_sites()
    if not rows:
        warn("Belum ada website tersimpan.")
        return False
    print(f"{'ID':<4} {'DOMAIN':<28} {'TYPE':<10} {'SSL':<5} {'CF':<5}")
    print("-" * 62)
    for row in rows:
        print(f"{row.id:<4} {row.domain:<28} {row.site_type:<10} {row.ssl_enabled:<5} {row.cloudflare_proxied:<5}")
    print()
    return True

def list_sites_flow() -> None:
    section("DAFTAR WEBSITE")
    display_sites_table()



def detail_site_flow() -> None:
    section("DETAIL WEBSITE")
    if not display_sites_table():
        return
    try:
        site_id = int(input("Masukkan ID website: ").strip())
    except ValueError:
        error("ID harus angka.")
        return
    row = get_site_by_id(site_id)
    if not row:
        error("Website tidak ditemukan.")
        return
    print(f"ID                : {row.id}")
    print(f"Domain            : {row.domain}")
    print(f"Jenis             : {row.site_type}")
    print(f"Root path         : {row.root_path}")
    print(f"Nginx available   : {row.nginx_available_path}")
    print(f"Nginx enabled     : {row.nginx_enabled_path}")
    print(f"SSL aktif         : {row.ssl_enabled}")
    print(f"Cloudflare proxy  : {row.cloudflare_proxied}")
    print(f"Catatan           : {row.notes or '-'}")
    print(f"Dibuat            : {row.created_at}")
    print(f"Diupdate          : {row.updated_at}")



def update_site_flow() -> None:
    section("UPDATE METADATA WEBSITE")
    if not display_sites_table():
        return
    try:
        site_id = int(input("Masukkan ID website: ").strip())
    except ValueError:
        error("ID harus angka.")
        return

    row = get_site_by_id(site_id)
    if not row:
        error("Website tidak ditemukan.")
        return

    ssl_enabled = 1 if yes_no(input(f"SSL aktif? [y/n] (saat ini {row.ssl_enabled}): ")) else 0
    cf_enabled = 1 if yes_no(input(f"Cloudflare proxied? [y/n] (saat ini {row.cloudflare_proxied}): ")) else 0
    notes = input(f"Catatan baru (kosong = hapus, lama: {row.notes or '-'}): ").strip() or None
    update_site_metadata(site_id, ssl_enabled, cf_enabled, notes)
    success("Metadata website berhasil diupdate.")



def delete_site_flow() -> None:
    section("HAPUS WEBSITE")
    if not display_sites_table():
        return
    try:
        site_id = int(input("Masukkan ID website yang akan dihapus: ").strip())
    except ValueError:
        error("ID harus angka.")
        return

    row = get_site_by_id(site_id)
    if not row:
        error("Website tidak ditemukan.")
        return

    warn(f"Website {row.domain} akan dihapus permanen dari VPS.")
    confirm = input("Ketik DELETE untuk konfirmasi: ").strip()
    if confirm != "DELETE":
        warn("Dibatalkan.")
        return

    try:
        backups = delete_site(row.root_path, row.nginx_available_path, row.nginx_enabled_path, row.domain)
        delete_site_record(site_id)
        success("Website berhasil dihapus bersih.")
        if backups:
            info("Backup file penting disimpan di folder data/backups.")
    except Exception as exc:
        error(f"Gagal menghapus website: {exc}")



def nginx_test_flow() -> None:
    section("TEST NGINX")
    result = test_nginx()
    if result.returncode == 0:
        success("nginx -t sukses.")
        print(result.stdout.strip() or result.stderr.strip())
        reload = input("Reload nginx sekarang? [y/n]: ").strip().lower()
        if reload in {"y", "yes"}:
            rr = reload_nginx()
            if rr.returncode == 0:
                success("Nginx berhasil direload.")
            else:
                error(rr.stderr.strip() or rr.stdout.strip())
    else:
        error(result.stderr.strip() or result.stdout.strip())



def install_ssl_flow() -> None:
    section("INSTALL SSL (CERTBOT)")
    if not display_sites_table():
        return
    try:
        site_id = int(input("Masukkan ID website: ").strip())
    except ValueError:
        error("ID harus angka.")
        return
    row = get_site_by_id(site_id)
    if not row:
        error("Website tidak ditemukan.")
        return
    install_ssl(row.domain, bool(row.cloudflare_proxied))



def main() -> None:
    init_db()
    while True:
        clear_screen()
        banner()
        main_menu()
        choice = input("\nPilih menu: ").strip()
        clear_screen()
        banner()
        if choice == "1":
            add_site_flow()
        elif choice == "2":
            list_sites_flow()
        elif choice == "3":
            detail_site_flow()
        elif choice == "4":
            update_site_flow()
        elif choice == "5":
            delete_site_flow()
        elif choice == "6":
            nginx_test_flow()
        elif choice == "7":
            install_ssl_flow()
        elif choice == "0":
            print("Sampai jumpa.")
            break
        else:
            error("Menu tidak valid.")
        pause()


if __name__ == "__main__":
    main()
