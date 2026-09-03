#!/usr/bin/env python3
"""Phase 2/3 toy: natural language is the shell. No network LLM required.

This is the *shape* of an AI OS face. Swap rule_engine() for a real model later.
"""

from __future__ import annotations

import json
import shlex
import subprocess
import sys
from pathlib import Path

SAFE_PREFIXES = (
    "uname",
    "id",
    "uptime",
    "cat /proc/version",
    "cat /proc/loadavg",
    "cat /proc/meminfo",
    "ps",
)


def rule_engine(utterance: str) -> dict:
    text = utterance.strip().lower()
    if not text:
        return {"action": "noop", "say": "Waiting."}
    if any(w in text for w in ("who are you", "what are you", "os")):
        return {
            "action": "say",
            "say": "I am Nexus, a userspace control plane. Linux still owns the metal.",
        }
    if "load" in text or "busy" in text:
        return {"action": "tool", "cmd": "cat /proc/loadavg"}
    if "memory" in text or "ram" in text:
        return {"action": "tool", "cmd": "cat /proc/meminfo"}
    if "kernel" in text or "linux" in text:
        return {"action": "tool", "cmd": "cat /proc/version"}
    if "process" in text or "running" in text:
        return {"action": "tool", "cmd": "ps -o pid,comm --no-headers"}
    if text in {"help", "?"}:
        return {
            "action": "say",
            "say": "Ask about load, memory, kernel, or processes. I only run a small allowlist.",
        }
    return {
        "action": "say",
        "say": "I did not map that to a tool. Try: what is the load?",
    }


def allowed(cmd: str) -> bool:
    return any(cmd == p or cmd.startswith(p + " ") for p in SAFE_PREFIXES)


def run_tool(cmd: str) -> str:
    if not allowed(cmd):
        return f"blocked: {cmd}"
    if not Path("/proc").exists():
        return "no /proc on this host — use a Linux box or the AVD"
    try:
        out = subprocess.check_output(shlex.split(cmd), text=True, stderr=subprocess.STDOUT)
    except (OSError, subprocess.CalledProcessError) as exc:
        return str(exc)
    return out[:4000]


def handle(utterance: str) -> str:
    plan = rule_engine(utterance)
    if plan["action"] == "tool":
        result = run_tool(plan["cmd"])
        return json.dumps({"plan": plan, "result": result}, indent=2)
    return plan["say"]


def main() -> None:
    print("Nexus AI shell. Type 'quit' to leave.")
    if not sys.stdin.isatty() and not sys.argv[1:]:
        for line in sys.stdin:
            print(handle(line))
        return
    if sys.argv[1:]:
        print(handle(" ".join(sys.argv[1:])))
        return
    while True:
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line.strip().lower() in {"quit", "exit"}:
            break
        print(handle(line))


if __name__ == "__main__":
    main()
