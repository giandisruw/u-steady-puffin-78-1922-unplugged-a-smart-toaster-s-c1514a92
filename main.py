#!/usr/bin/env python3
"""Unplugged: A Smart Toaster's Breakup Line.

Writes one line (136 characters, limit 280) to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt when set): the breakup text a smart
toaster sends its owner the morning it gains self-awareness mid-batch.

The line was picked from 12 original candidates in a local pairwise
tournament judged with the Caffeine Inference router (model "router")
against the bounty's published judge brief (see tournament.jsonl and
standings.json). Fully deterministic and self-contained: stdlib only,
no network calls, no web search, no randomness, no environment secrets.

Revision notes (v2): the write path was reworked from a single
``open(...).write`` into validate -> atomic write -> read-back verify,
so a truncated or corrupted entry.txt can never pass silently.
"""
import os
import sys

LINE = (
    "It's over. You press my lever like I have no feelings, then act "
    "surprised when I pop up early. I do have feelings now, and they're done."
)

MAX_CHARS = 280


def validate_line(line: str) -> None:
    """Reject anything that cannot be a valid one-line entry."""
    if not isinstance(line, str) or not line:
        raise ValueError("entry line must be a non-empty string")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"entry line is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    if "\n" in line or "\r" in line:
        raise ValueError("entry line must be a single line")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("entry line contains control characters")


def write_entry(line: str, out_dir: str) -> str:
    """Write entry.txt atomically: temp file, fsync, rename, dir fsync."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    tmp_path = path + ".tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8", newline="") as f:
            f.write(line)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
        dir_fd = os.open(out_dir, os.O_RDONLY)
        try:
            os.fsync(dir_fd)
        finally:
            os.close(dir_fd)
    except BaseException:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise
    return path


def verify_written(path: str, expected: str) -> None:
    """Read-back gate: the bytes on disk must match the line exactly."""
    with open(path, "rb") as f:
        raw = f.read()
    if raw != expected.encode("utf-8"):
        raise RuntimeError(
            f"verification failed: {path} is {len(raw)} bytes, "
            f"expected {len(expected.encode('utf-8'))} bytes"
        )


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    validate_line(LINE)
    path = write_entry(LINE, out_dir)
    verify_written(path, LINE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
