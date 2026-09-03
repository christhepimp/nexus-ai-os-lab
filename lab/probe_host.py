#!/usr/bin/env python3
"""Phase 1 sense: snapshot the machine the way an AI OS would."""

from __future__ import annotations

import json
import os
import platform
from pathlib import Path


def _read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def linux_snapshot() -> dict:
    proc = Path("/proc")
    snap = {
        "ok": True,
        "platform": platform.platform(),
        "uname": platform.uname()._asdict(),
        "pid": os.getpid(),
        "uid": os.getuid() if hasattr(os, "getuid") else None,
        "meminfo": _read(proc / "meminfo"),
        "loadavg": _read(proc / "loadavg"),
        "version": _read(proc / "version"),
        "cmdline": _read(proc / "cmdline"),
        "top_processes": [],
    }
    for entry in list(proc.iterdir())[:400]:
        if not entry.name.isdigit():
            continue
        comm = _read(entry / "comm")
        status = _read(entry / "status")
        if not comm:
            continue
        snap["top_processes"].append(
            {
                "pid": int(entry.name),
                "comm": comm.strip() if comm else None,
                "state_line": None if not status else next(
                    (ln for ln in status.splitlines() if ln.startswith("State:")),
                    None,
                ),
            }
        )
        if len(snap["top_processes"]) >= 25:
            break
    return snap


def fallback_snapshot() -> dict:
    return {
        "ok": False,
        "reason": "/proc is not a Linux procfs here. Run on Linux or inside the AVD.",
        "platform": platform.platform(),
        "uname": platform.uname()._asdict(),
    }


def main() -> None:
    snap = linux_snapshot() if Path("/proc/version").exists() else fallback_snapshot()
    print(json.dumps(snap, indent=2))


if __name__ == "__main__":
    main()
