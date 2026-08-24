#!/usr/bin/env python3
"""Memory health check for Hermes memories (MEMORY.md + USER.md).

Prints per-file stats: entry count, chars, capacity %, and flags for
suspicious entries (contains a year => stale-prone; >300 chars => overlong).
Pure stdlib, no dependencies. Exit 0 always (watchdog-friendly).
"""
import os
import re
import sys

MEM_DIR = os.path.expanduser("~/.hermes/memories")
DEFAULTS = {"memory_char_limit": 4000, "user_char_limit": 2500}
FILES = {"MEMORY.md": "memory_char_limit", "USER.md": "user_char_limit"}


def read_limits():
    limits = dict(DEFAULTS)
    cfg = os.path.expanduser("~/.hermes/config.yaml")
    try:
        with open(cfg, encoding="utf-8") as f:
            txt = f.read()
        for key in limits:
            m = re.search(rf"{key}\s*:\s*(\d+)", txt)
            if m:
                limits[key] = int(m.group(1))
    except OSError:
        pass
    return limits


def analyze(path, limit):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        content = f.read()
    entries = [e.strip() for e in content.split("\n§") if e.strip()]
    total = len(content)
    pct = round(total / limit * 100, 1) if limit else 0.0
    flags = []
    for e in entries:
        marks = []
        m = re.search(r"(20\d\d)", e)
        if m:
            marks.append(f"含日期{m.group(1)}")
        if len(e) > 300:
            marks.append("超长>300")
        if marks:
            flags.append((e[:40].replace("\n", " "), ",".join(marks)))
    return {"file": os.path.basename(path), "entries": len(entries),
            "chars": total, "limit": limit, "pct": pct, "flags": flags}


def main():
    limits = read_limits()
    results = []
    for fname, lkey in FILES.items():
        r = analyze(os.path.join(MEM_DIR, fname), limits[lkey])
        if r:
            results.append(r)
    if not results:
        print("NO_MEMORY_FILES")
        return
    for r in results:
        print(f"[{r['file']}] {r['entries']} entries | {r['chars']}/{r['limit']} chars | {r['pct']}%")
        for e, fl in r["flags"]:
            print(f"  FLAG: {fl} -> {e}")


if __name__ == "__main__":
    main()
