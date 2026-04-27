#!/usr/bin/env bash
# Regenerate the per-language HANDBOOK files at the repo root from the
# bilingual source at docs/a-newsprint/HANDBOOK.md (which the website reads).
#
# Run after editing the bilingual handbook to keep HANDBOOK.md (EN) and
# HANDBOOK.pt.md (PT) — the files casual readers see on GitHub — in sync.
#
# MANIFESTO and README do NOT have a bilingual source: edit MANIFESTO.md +
# MANIFESTO.pt.md (and README.md + README.pt.md) directly, in pairs.

set -euo pipefail

cd "$(dirname "$0")/.."

python3 scripts/build-monolingual.py \
  docs/a-newsprint/HANDBOOK.md \
  HANDBOOK.md \
  HANDBOOK.pt.md \
  HANDBOOK.md \
  HANDBOOK.pt.md
