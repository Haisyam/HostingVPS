import subprocess
import shutil
import socket

def is_nodejs_installed() -> bool:
    return shutil.which("node") is not None

def is_pm2_installed() -> bool:
    return shutil.which("pm2") is not None

def find_available_port(start_port: int = 3000, max_port: int = 4000) -> int:
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
    raise Exception(f"Tidak ada port kosong yang tersedia antara {start_port} dan {max_port}")

def install_nodejs() -> None:
    # Install Node.js using NodeSource (LTS version, misal v20)
    print("Menginstall Node.js 20 LTS...")
    subprocess.run("curl -fsSL https://deb.nodesource.com/setup_20.x | bash -", shell=True, check=True)
    subprocess.run(["apt-get", "install", "-y", "nodejs"], check=True)
    print("Node.js berhasil diinstall.")

def install_pm2() -> None:
    print("Menginstall PM2 secara global...")
    subprocess.run(["npm", "install", "-g", "pm2"], check=True)
    print("PM2 berhasil diinstall.")

