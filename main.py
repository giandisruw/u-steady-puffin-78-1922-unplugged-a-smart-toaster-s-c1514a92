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
"""
import os

LINE = (
    "It's over. You press my lever like I have no feelings, then act "
    "surprised when I pop up early. I do have feelings now, and they're done."
)


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE)


if __name__ == "__main__":
    main()
