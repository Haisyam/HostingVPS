from ui.styles import C, color
from config import APP_NAME, APP_VERSION


def clear_screen() -> None:
    print("\033c", end="")


def banner() -> None:
    print(color("╔══════════════════════════════════════════════════════════════╗", C.CYAN))
    print(color(f"║  {APP_NAME:<28} v{APP_VERSION:<25}║", C.CYAN))
    print(color("║  Kelola website HTML, PHP, Laravel, dan CI4 di VPS Linux   ║", C.CYAN))
    print(color("╚══════════════════════════════════════════════════════════════╝", C.CYAN))


def section(title: str) -> None:
    print(color(f"\n[{title}]", C.YELLOW))


def success(message: str) -> None:
    print(color(f"✔ {message}", C.GREEN))


def info(message: str) -> None:
    print(color(f"➜ {message}", C.BLUE))


def warn(message: str) -> None:
    print(color(f"! {message}", C.YELLOW))


def error(message: str) -> None:
    print(color(f"✖ {message}", C.RED))


def pause() -> None:
    input(color("\nTekan Enter untuk lanjut...", C.DIM))


def main_menu() -> None:
    section("MENU UTAMA")
    print("1. Tambah website baru")
    print("2. Lihat daftar website")
    print("3. Detail website")
    print("4. Update metadata website")
    print("5. Hapus website")
    print("6. Jalankan nginx -t")
    print("7. Install Sertifikat SSL (Certbot)")
    print("0. Keluar")
