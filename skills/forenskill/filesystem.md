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
  not just allocated ones.
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
- Note **file slack** (space between the logical file end and the end
  of the last allocated cluster) as distinct from unallocated clusters.
  Phase 15 covers signature scanning of unallocated space; slack belonging
  to a specific allocated file should be checked when that file is of
  particular interest.
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
