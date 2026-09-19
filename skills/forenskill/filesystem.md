# Phases 6 and 15 — File System Contents and Carving

Sleuth Kit tools operate on the **image** with `-o <sector_offset>` (the
start sector from `mmls`, not a byte offset — see
[volumes-baseline.md](volumes-baseline.md)). They do not take a mounted
directory as input.

## Phase 6 — File System Contents (per volume)

```bash
# Allocated + deleted listing (path list)
fls -r -p -o <sector_offset> evidence/image_copy/<image> > notes/fls_vol_<slot>.list

# Same listing as a MAC-time body file, for timeline work.
# <mount_prefix> is the path prefix written into the body file (e.g. C: or /)
# WARNING: on FAT-family media (FAT/exFAT) the times in this file are local
# times, not UTC, and can carry different offsets across the volume —
# convert them first (volumes-baseline.md, Phase 4) before using them.
fls -r -m <mount_prefix> -o <sector_offset> evidence/image_copy/<image> > notes/fls_vol_<slot>.body

# Export everything (allocated and deleted-but-intact) preserving paths
tsk_recover -e -o <sector_offset> evidence/image_copy/<image> extracted/vol_<slot>/
```

For E01/EWF, point the commands at `evidence/ewf_mount/ewf1` instead of the
image path.

- Run a recursive listing (allocated **and** deleted) for every volume;
  record path, allocation status, size, and MAC timestamps.
- Refer to every item with a genuine filename by its **path** in notes
  and the report — never an internal tool ID (inode number, MFT record
  number, etc.), which is meaningless outside this examination and this
  tool's output.
- For volumes/files you will also carve (Phase 15), record each item's
  volume-relative starting byte offset now (first data block/cluster from
  `istat` × block size), so carved (nameless) items can be referenced
  consistently alongside named ones later. Do not present a fabricated or
  rounded offset for entries with no data location (volume-label entries,
  zero-length stubs).
- Recover and examine the contents of every deleted-but-intact item,
  not just allocated ones. **Validate every deleted-file export before
  trusting it** — a recovered file is only as good as its clusters:
  - Compare the exported size with the size in the directory entry
    (`fls`/`istat`). A smaller export is truncated or partly overwritten.
  - Check whether the file's first data unit still belongs to it:
    `ifind -d <block> -o <sector_offset> <image>` reports the owner of a
    block. If the clusters were reallocated to another file or directory,
    the export contains that other data (e.g. a "recovered" shortcut that is
    really a directory listing). Mark the item "content overwritten."
  - Confirm the file type and structure match the name (`file`, `exiftool`).
  - Do not rely on `istat`'s sector list for FAT-family files: it can be
    incomplete for large files. Derive contiguity from the first cluster plus
    size, or from the FAT chain, and confirm against `blkstat`/`ifind`.
- For files whose extension doesn't match the actual type, note the
  mismatch explicitly: `file --mime-type` or `exiftool -FileType` across
  the extracted tree, diffed against extension.
- Check standard OS housekeeping locations for context (System Volume
  Information / Recycle Bin on Windows-formatted volumes, Spotlight /
  `.Trash` on macOS, etc.). Note what is routine vs. unusual for the
  record, but don't over-report routine housekeeping files in the final
  report.
- Check for NTFS Alternate Data Streams (ADS) on files of interest —
  standard listings do not display them, and they can hide an entire
  second payload on an otherwise unremarkable file (`dir /r` equivalent:
  `icat` each `$MFT` data attribute, or an ADS-aware tool). Note any in
  `anomalies.md`.
- **Sweep the file slack of every file** (space between the logical file end
  and the end of the last allocated cluster), distinct from unallocated
  clusters. Do not restrict this to files that look interesting — evidence
  has been found in the slack of an unremarkable stock image. The
  volume-wide check is cheap, and it tells you whether the per-file work is
  needed:

  ```bash
  # All slack on the volume, concatenated; count non-zero bytes
  blkls -s -o <sector_offset> evidence/image_copy/<image> > extracted/vol_<slot>_slack.bin
  tr -d '\0' < extracted/vol_<slot>_slack.bin | wc -c
  strings -a -n 6 extracted/vol_<slot>_slack.bin; strings -a -el -n 6 extracted/vol_<slot>_slack.bin
  # If non-zero, find which files hold it. `icat -s` prints the file's
  # content FOLLOWED BY its slack, so skip the first <size> bytes:
  size=$(icat -o <sector_offset> evidence/image_copy/<image> <inum> | wc -c)
  icat -s -o <sector_offset> evidence/image_copy/<image> <inum> \
    | tail -c +$((size + 1)) | tr -d '\0' | wc -c
  ```

  Run the per-file check over every allocated file (`fls -r -F`), report
  the files with non-zero slack, and examine their content. Directories have
  slack too. Record the negative result as well (e.g. "N of M files had zero
  slack"). Non-zero slack on
  a heavily used volume is often just leftover data from earlier files:
  triage by looking for readable text, credentials, headers of known types,
  and content that relates to the case rather than reporting every byte. If
  the file system doesn't support the option, mark this N/A with that
  reason. On exFAT, also compare each file's ValidDataLength with its
  DataLength and note any difference.
- **Check that every allocated cluster has an owner.** A file with no
  surviving directory entry can still have its clusters marked allocated
  (the allocation bitmap/FAT wasn't cleared), so it is invisible both to
  listings and to a scan of unallocated space. For each run of allocated
  blocks (`blkstat` shows a block's allocation status), confirm
  `ifind -d <block>` returns an owner rather than "Inode not found".
  Investigate (a) allocated blocks with no owner and (b) non-zero content
  in unallocated
  blocks (`blkls -A -o <sector_offset> <image> | tr -d '\0' | wc -c` gives
  the quick non-zero total; map the runs to block numbers to examine them).
  Sanity-check any derived count against an independent tool's count before
  using it — a parsing slip (for example, skipping files in subfolders)
  produces plausible but wrong "unowned" totals. If you script this, follow
  the scripts rule in SKILL.md.
- For file systems that support them, check for prior point-in-time
  copies (Windows Volume Shadow Copies, macOS APFS snapshots / Time
  Machine, ZFS/Btrfs snapshots) and note their presence and date range
  even if you don't fully process every one — they can hold deleted or
  modified files no longer visible on the live file system. Windows VSC
  and USN Journal detail is in Phase 7 ([os/windows.md](os/windows.md)).
- Log every exported item in `notes/exhibits.md` (path, allocation
  status, size, offset if carved later).

## Phase 15 — Unallocated-Space / Signature Carving

```bash
bulk_extractor -o extracted/carved/bulk_out evidence/image_copy/<image>
# and/or
foremost -i evidence/image_copy/<image> -o extracted/carved/foremost_out
binwalk --dd='.*' evidence/image_copy/<image>
```

Whole-image signature and feature scanning is the **backstop** for anything
the structure-based checks in Phase 6 (ownership, slack) missed, so it is
worth running as soon as the image is verified rather than saving it for
last — on small images it takes seconds to minutes; on large ones,
estimate the run time first and tell the user. Running `bulk_extractor` is
not the same as reviewing it: read at least the `email`, `telephone`,
`ccn`, `url`, `domain`, `gps`, `exif`, `rfc822`, and `aes_keys` feature
files, and log what each contained (including "empty"). Whole-image
`strings -a` in both ASCII and UTF-16LE (`-el`) is a companion sweep.
Offsets that these tools report point you at a location — resolve each one
against the Phase 6 listing and the ownership check before deciding whether
it is a known file, slack, or an orphan.

- Run a byte-level file-signature scan (JPEG/PNG/PDF/ZIP/GIF/Office/
  archive magic headers at minimum) across the **full** content of every
  volume. Directory-listing recovery alone is not enough — files with no
  surviving directory entry never appear there.
- Cross-reference every signature hit against the Phase 6 file listing
  by volume-relative offset to determine whether it is already accounted
  for (the file's own header, an embedded thumbnail/embedded object) or
  genuinely orphaned. Whole-image tools report image-relative offsets:
  subtract the volume's start byte offset (`sector_size × start_sector`).
- Carve and examine every orphaned hit. For each:
  - Determine whether it is a real, structurally valid file or coincidental
    noise: check for a valid trailer/EOF marker, sane parsed structure, and
    metadata that makes sense. Garbage headers with nonsensical
    dimensions/parameters are a red flag for a false positive. Record
    ruled-out hits as a negative result with the evidence.
  - If real, extract its full content and metadata exactly as in Phases
    13/14 ([content-analysis.md](content-analysis.md)).
  - Record its volume-relative offset as its identifier (it has no
    filename) — the **exact** byte offset the signature was found at, not
    a sector- or cluster-rounded approximation, since orphaned data is not
    guaranteed to be aligned to any boundary.
- If a second tool (e.g. `binwalk`) is used to corroborate, record
  exactly how much of each volume it actually finished scanning before
  citing it as confirmation. A partial/interrupted scan that happens to
  cover the interesting region is not a completed independent sweep, and
  the report must say which one you have.
- Record what each carver *missed* as well as what it found (e.g. it
  extracted only an embedded thumbnail, or a run cut short of the file's
  end). Where a structure-based method (ownership map, allocation bitmap)
  recovered a file a signature carver did not, prefer the whole file and
  say which method produced it.
- For a high-entropy block with no recognizable header: record its offset,
  length, and entropy; check whether it matches a header or repeats elsewhere
  in the image; consider whether it could be a fragment of a known encrypted
  container on the volume; and record it as unresolved with the reason
  rather than dropping it.
- Every carved or recovered item goes into `notes/exhibits.md` **and**
  `extracted/manifest.sha1`. Anything new that a carve produces re-enters
  Phases 12–14 (see the loop note in SKILL.md).
