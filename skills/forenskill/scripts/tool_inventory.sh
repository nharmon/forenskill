#!/usr/bin/env bash
# Report presence and version of every tool the forenskill phases rely on.
# Usage: bash scripts/tool_inventory.sh | tee -a notes/methodology.md
#
# Version flags are not uniform (Sleuth Kit and libewf use -V, ExifTool uses
# -ver, most GNU tools use --version), so each is tried in turn and the first
# output line that looks like a version is kept.

tool_version() {
  local t="$1" flag out
  for flag in --version -V -version -ver; do
    out=$(timeout 5 "$t" "$flag" </dev/null 2>&1 | grep -m1 -E '[0-9]+\.[0-9]+')
    [ -n "$out" ] && { printf '%s\n' "$out"; return; }
  done
  echo "present (version not detected — record manually)"
}

for t in mmls fsstat fls icat istat tsk_recover blkls img_stat \
         ewfmount ewfinfo affuse xmount \
         exiftool file binwalk foremost scalpel photorec bulk_extractor \
         regripper hivexml sqlite3 \
         log2timeline.py psort.py \
         volatility3 vol.py vol3 \
         john hashcat \
         md5sum sha1sum sha256sum; do
  printf '%-16s ' "$t"
  if command -v "$t" >/dev/null 2>&1; then tool_version "$t"; else echo "NOT FOUND"; fi
done
