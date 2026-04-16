from pathlib import Path
import shutil
from typing import Iterable


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")


def remove_path(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
    elif path.is_dir():
        shutil.rmtree(path)


def copy_file(src: Path, dst: Path) -> None:
    ensure_dir(dst.parent)
    shutil.copy2(src, dst)


def backup_files(paths: Iterable[Path], backup_dir: Path, label: str) -> list[Path]:
    ensure_dir(backup_dir)
    saved = []
    for path in paths:
        if path.exists() or path.is_symlink():
            dst = backup_dir / f"{label}__{path.name}"
            if path.is_symlink():
                target = path.resolve()
                if target.exists():
                    shutil.copy2(target, dst)
                else:
                    dst.write_text(f"broken symlink -> {target}\n", encoding="utf-8")
            elif path.is_file():
                shutil.copy2(path, dst)
            saved.append(dst)
    return saved
