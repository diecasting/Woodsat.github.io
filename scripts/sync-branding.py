#!/usr/bin/env python3
"""
sync-branding.py — Merge config/branding/*.toml into config/_default/params.toml

WHY THIS EXISTS
---------------
Hugo only auto-loads a fixed set of config filenames from config/_default/
(notably `params.toml`). Arbitrary files such as `seo.toml`, `company.toml`,
`contact.toml` or `schema.toml` are silently ignored. To keep branding in
clean, separate, human-editable source files (config/branding/) while still
feeding Hugo, this script merges those four files into the [params] namespace
of config/_default/params.toml — the one file Hugo actually reads.

The brand block inside params.toml is delimited by markers so the rest of the
file (Author, features, homepage, footer, cta) is preserved untouched.

Transformation: branding files use `[params.company]` etc. (standalone config
form). Inside params.toml the `params` namespace is implicit, so those headers
are rewritten to `[company]`. The bare `[params]` table header is dropped.

Run by: scripts/init-site.sh and .github/workflows/hugo.yml (before `hugo`).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRANDING_DIR = ROOT / "config" / "branding"
PARAMS_PATH = ROOT / "config" / "_default" / "params.toml"

BRAND_FILES = ["company", "contact", "seo", "schema"]

START_MARKER = (
    "# >>> BRANDING SYNC START (auto-generated from config/branding/*.toml; "
    "do not edit by hand) >>>"
)
END_MARKER = "# <<< BRANDING SYNC END <<<"


def build_brand_block() -> str:
    blocks = []
    for name in BRAND_FILES:
        src = BRANDING_DIR / f"{name}.toml"
        if not src.exists():
            print(f"WARNING: missing branding file {src}", file=sys.stderr)
            continue
        text = src.read_text(encoding="utf-8")
        out_lines = []
        for line in text.splitlines():
            stripped = line.strip()
            # Drop the bare `[params]` header: params.toml already IS the
            # params namespace, and a duplicate bare table would be invalid.
            if stripped == "[params]":
                continue
            # Rewrite `[params.X...]` table headers -> `[X...]`
            m = re.match(r"^(\s*)\[params\.(\S+)\]", line)
            if m:
                line = f"{m.group(1)}[{m.group(2)}]"
            out_lines.append(line)
        blocks.append("\n".join(out_lines).strip())
    return "\n\n".join(blocks)


def sync() -> None:
    brand_block = build_brand_block()
    content = (
        PARAMS_PATH.read_text(encoding="utf-8") if PARAMS_PATH.exists() else ""
    )

    if START_MARKER in content and END_MARKER in content:
        pre, _, post = content.partition(START_MARKER)
        _, _, after = post.partition(END_MARKER)
        new_content = (
            pre.rstrip()
            + "\n\n"
            + START_MARKER
            + "\n\n"
            + brand_block
            + "\n\n"
            + END_MARKER
            + after
        )
    else:
        new_content = (
            content.rstrip()
            + "\n\n"
            + START_MARKER
            + "\n\n"
            + brand_block
            + "\n\n"
            + END_MARKER
            + "\n"
        )

    PARAMS_PATH.write_text(new_content, encoding="utf-8")
    print(f"OK: branding synced into {PARAMS_PATH}")


if __name__ == "__main__":
    sync()
