#!/usr/bin/env python3
"""Memory health check for long-running Agent memories.

Prints per-file stats: entry count, chars, capacity %, and flags for
suspicious entries (contains a year => stale-prone; >300 chars => overlong).
Pure stdlib, no dependencies. Exit 0 always (watchdog-friendly).

RUNTIME ADAPTATION NOTE: Default behavior is calibrated for Hermes conventions —
it reads MEMORY.md + USER.md from ~/.hermes/memories, splits entries on the
section marker '\u00a7', and uses Hermes char limits. Other runtimes
(OpenClaw, etc.) can override paths, files, limits, and delimiter via
command-line options.

Capacity thresholds (<85% healthy / 85-95% review / >95% urgent) and the
year + overlong signals remain valid across runtimes.
"""
import argparse
import os
import re
import sys

MEM_DIR = os.path.expanduser("~/.hermes/memories")
DEFAULT_LIMITS = {"memory_char_limit": 4000, "user_char_limit": 2500}
DEFAULT_FILES = {"MEMORY.md": "memory_char_limit", "USER.md": "user_char_limit"}
DEFAULT_DELIMITER = "\n\u00a7"


def read_limits(cfg_path):
    limits = dict(DEFAULT_LIMITS)
    if not cfg_path:
        return limits
    try:
        with open(cfg_path, encoding="utf-8") as f:
            txt = f.read()
        for key in limits:
            m = re.search(rf"{key}\s*:\s*(\d+)", txt)
            if m:
                limits[key] = int(m.group(1))
    except OSError:
        pass
    return limits


def parse_files(files_arg):
    """Parse --files FILE:LIMIT_KEY,FILE:LIMIT_KEY into a dict."""
    result = {}
    for part in files_arg.split(","):
        if ":" not in part:
            raise ValueError(f"--files entry must be FILE:LIMIT_KEY, got: {part}")
        fname, lkey = part.split(":", 1)
        result[fname.strip()] = lkey.strip()
    return result


def parse_limits(limits_arg):
    """Parse --limits LIMIT_KEY=VALUE,LIMIT_KEY=VALUE into a dict."""
    result = dict(DEFAULT_LIMITS)
    if not limits_arg:
        return result
    for part in limits_arg.split(","):
        if "=" not in part:
            raise ValueError(f"--limits entry must be KEY=VALUE, got: {part}")
        key, value = part.split("=", 1)
        result[key.strip()] = int(value.strip())
    return result


def analyze(path, limit, delimiter):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        content = f.read()
    entries = [e.strip() for e in content.split(delimiter) if e.strip()]
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
    return {
        "file": os.path.basename(path),
        "entries": len(entries),
        "chars": total,
        "limit": limit,
        "pct": pct,
        "flags": flags,
    }


def build_parser():
    parser = argparse.ArgumentParser(
        description="Check memory file health (capacity, stale flags, overlong entries)."
    )
    parser.add_argument(
        "--mem-dir",
        default=MEM_DIR,
        help="Directory containing memory files (default: ~/.hermes/memories).",
    )
    parser.add_argument(
        "--files",
        default=None,
        help='Comma-separated FILE:LIMIT_KEY pairs, e.g. "MEMORY.md:memory_char_limit,USER.md:user_char_limit".',
    )
    parser.add_argument(
        "--limits",
        default=None,
        help='Comma-separated KEY=VALUE limit overrides, e.g. "memory_char_limit=4000".',
    )
    parser.add_argument(
        "--config",
        default=os.path.expanduser("~/.hermes/config.yaml"),
        help="Path to config file from which to read limit overrides (default: ~/.hermes/config.yaml).",
    )
    parser.add_argument(
        "--delimiter",
        default=DEFAULT_DELIMITER,
        help=r"Entry delimiter (default: newline + section sign). Use \\n for newline.",
    )
    parser.add_argument(
        "--no-config",
        action="store_true",
        help="Do not read limits from --config; use --limits or defaults only.",
    )
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    files = parse_files(args.files) if args.files else dict(DEFAULT_FILES)
    delimiter = args.delimiter.replace("\\n", "\n")

    if args.no_config:
        limits = parse_limits(args.limits) if args.limits else dict(DEFAULT_LIMITS)
    else:
        limits = read_limits(args.config)
        if args.limits:
            limits.update(parse_limits(args.limits))

    results = []
    for fname, lkey in files.items():
        limit = limits.get(lkey)
        if limit is None:
            print(f"UNKNOWN_LIMIT_KEY: {lkey}", file=sys.stderr)
            continue
        r = analyze(os.path.join(args.mem_dir, fname), limit, delimiter)
        if r:
            results.append(r)

    if not results:
        print("NO_MEMORY_FILES")
        return 0

    for r in results:
        print(
            f"[{r['file']}] {r['entries']} entries | "
            f"{r['chars']}/{r['limit']} chars | {r['pct']}%"
        )
        for e, fl in r["flags"]:
            print(f"  FLAG: {fl} -> {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
