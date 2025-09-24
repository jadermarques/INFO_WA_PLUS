from __future__ import annotations
import shutil
from datetime import datetime
from pathlib import Path

from src.app.config import settings


def run_backup(dest_dir: str) -> str:
    src = Path(settings.db_path)
    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = dest / f"data-{ts}.db"
    if src.exists():
        shutil.copy2(src, target)
    else:
        target.write_bytes(b"")
    return str(target)
