#!/usr/bin/env python3
"""Split a bilingual markdown file (with <!--PT-->/<!--EN--> markers) into
two monolingual files, prepending a language navigation at the top.

Usage:
    build-monolingual.py SRC EN_OUT PT_OUT EN_NAME PT_NAME

SRC must contain <!--PT-->...<!--/PT--> and <!--EN-->...<!--/EN--> blocks.
Anything outside markers is treated as shared (kept in both outputs).

EN_NAME and PT_NAME are the basenames used in the language nav links
(e.g. "README.md" and "README.pt.md").
"""

import re
import sys
from pathlib import Path


def filter_lang(src: str, lang: str) -> str:
    """Keep blocks for `lang`, drop opposite-lang blocks, strip own markers."""
    keep = lang
    drop = "EN" if lang == "PT" else "PT"
    # Drop opposite-language blocks entirely. Markers must be at the start of
    # their own line (column 0) — this prevents matching literal mentions of
    # the markers inside backticks or prose. Consume only the marker block plus
    # an optional trailing newline so blank lines around the block are
    # preserved (this keeps EN- and PT-only extractions symmetric).
    out = re.sub(
        rf"(?m)^<!--{drop}-->\n.*?\n^<!--/{drop}-->\n?",
        "",
        src,
        flags=re.DOTALL,
    )
    # Strip own-lang markers, keep content.
    out = re.sub(rf"(?m)^<!--{keep}-->\n", "", out)
    out = re.sub(rf"(?m)^<!--/{keep}-->\n?", "", out)
    # Collapse runs of >2 blank lines into 2.
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip() + "\n"


def lang_nav(active: str, en_name: str, pt_name: str) -> str:
    """Return a one-line language nav for the top of the file."""
    en_link = f"[English]({en_name})" if active != "EN" else "**English**"
    pt_link = f"[Português]({pt_name})" if active != "PT" else "**Português**"
    return f"{en_link} · {pt_link}\n\n---\n\n"


def main() -> None:
    if len(sys.argv) != 6:
        print(__doc__)
        sys.exit(2)
    src_path, en_out, pt_out, en_name, pt_name = sys.argv[1:6]
    src = Path(src_path).read_text()

    en = lang_nav("EN", en_name, pt_name) + filter_lang(src, "EN")
    pt = lang_nav("PT", en_name, pt_name) + filter_lang(src, "PT")

    Path(en_out).write_text(en)
    Path(pt_out).write_text(pt)
    print(f"wrote {en_out} ({len(en.splitlines())} lines)")
    print(f"wrote {pt_out} ({len(pt.splitlines())} lines)")


if __name__ == "__main__":
    main()
