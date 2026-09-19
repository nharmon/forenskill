# Phases 3–4 — Volume Layout and System Baseline

## Phase 3 — Partition / Volume Layout

```bash
mmls evidence/image_copy/<image>
```

**If `mmls` prints nothing (or nonsense), the media may have no partition
table.** USB sticks, SD cards, and camera media are often formatted as a
single volume starting at sector 0 ("superfloppy"). Do not stop and do not
trust `fdisk -l` here — on an all-`0xFF` or zeroed MBR area it can invent
bogus partitions. Instead:

```bash
xxd -l 96 evidence/image_copy/<image>     # look at the boot sector
fsstat evidence/image_copy/<image>         # no -o: try the file system at sector 0
```

Look for a file system signature at sector 0 (`EXFAT   `, `NTFS    `, FAT
`FAT32   `/`FAT16   `, or an ext superblock at byte 1080). If one is there,
record the layout as "single volume at sector 0, no partition table" and use
offset 0 (omit `-o`) for the rest of the exam. If nothing is recognizable,
flag the image for Phase 12 (possible encrypted or wiped volume) and log it in
`notes/anomalies.md`.

**Two different offset units are in play — don't mix them up:**

- Sleuth Kit tools (`fsstat`, `fls`, `icat`, `istat`, `tsk_recover`, …) take
  `-o <sector_offset>`: the **start sector** exactly as `mmls` reports it.
- `mount ... offset=` takes **bytes**: `byte_offset = sector_size × start_sector`
  (`mmls` prints the sector size in its header).

Mounting is optional when Sleuth Kit covers the file system (and it needs
root, which may not be available). If you don't mount, say so in
`methodology.md` and work through Sleuth Kit against the image. If you do
mount, for raw/dd images use the byte offset, read-only:

```bash
mkdir -p mount/vol_<slot>
mount -o ro,loop,offset=<byte_offset> evidence/image_copy/<image> mount/vol_<slot>
```

Add a journal-suppression option where the file system has one, so the
mount can't replay the journal (a write): `noload` for ext3/ext4,
`norecovery` for XFS. NTFS/FAT/exFAT need nothing beyond `ro`. If `mount`
rejects an option, don't drop `ro` to get around it — note the failure in
`methodology.md` and fall back to Sleuth Kit against the image.

For E01/EWF, mount the EWF layer first, then treat the resulting raw
device the same way:

```bash
mkdir -p evidence/ewf_mount
ewfmount evidence/image_copy/<image>.E01 evidence/ewf_mount
mmls evidence/ewf_mount/ewf1
```

- Record every partition from `mmls`: slot, start sector, end sector,
  length, and type.
- For each volume, run `fsstat -o <sector_offset>` and record in
  `methodology.md`: file system type, volume label, volume serial/ID, OEM
  name/formatting-tool signature, and cluster/sector size.
- Note anything about how a volume was formatted that could identify
  the originating OS/toolchain (e.g. a Linux OEM string on a Windows-style
  file system).
- If multiple physical disks or a RAID/spanned volume set is present,
  confirm you have identified and imaged **all** members before analyzing
  any single member's file system — a striped/spanned volume examined from
  one disk alone will appear corrupt or incomplete.
- Check that the disk geometry reported by the partition table is
  consistent with the full addressable size of the image; a discrepancy
  can indicate an HPA/DCO area was not captured (Phase 1) or that the
  image itself is truncated.
- Flag encrypted, unrecognized, or unmountable volumes for the
  handling in Phase 12 ([encryption.md](encryption.md)).
- Log every volume as an exhibit in `notes/exhibits.md`.

## Phase 4 — System Baseline & Time Zone

Do this before building any timeline elsewhere in the exam — every dated
finding in later phases depends on knowing what clock produced it.

- Record the OS name, edition, version/build number, and installed
  service pack/patch level for each bootable volume (registry
  `SOFTWARE\Microsoft\Windows NT\CurrentVersion`, `/etc/os-release`,
  `/System/Library/CoreServices/SystemVersion.plist`).
- Record the computer/host name and, where available, the OS
  installation date.
- Record every local user account found (name, SID/UID, account
  creation date, last logon, administrator/standard privilege level) in
  `subject_id.md`, and cross-check against Phase 7's SAM/registry/passwd
  findings.
- Determine each system's configured time zone (Windows
  `SYSTEM\CurrentControlSet\Control\TimeZoneInformation`; macOS
  `/etc/localtime` or the `com.apple.timezone` preference; Linux
  `/etc/timezone` or the `/etc/localtime` symlink target) and record it
  explicitly in `methodology.md`. Every timestamp you cite elsewhere is
  understood relative to this, and to UTC.
- Where possible, sanity-check the system clock against an independent
  time anchor (a file with a known-correct creation time, a network log
  with server-side timestamps, metadata embedded by a third-party service)
  to catch a clock that was wrong, drifting, or deliberately altered. Do
  not assume the system clock was accurate throughout the device's
  operational life.
- **FAT-family time handling (FAT12/16/32, exFAT).** These file systems
  store *local* time, not UTC. FAT/FAT32 record no zone at all. exFAT
  records a UTC-offset byte per timestamp (create, modify, access — bytes
  0x16–0x18 of the File directory entry per the Microsoft exFAT
  specification; bit 7 = offset valid, low 7 bits = signed offset in 15-minute
  units). Sleuth Kit versions have been seen displaying these local times
  labeled `(UTC)`; check how your version treats the entry by comparing its
  output with the raw directory entry (`xxd`) for one file before trusting it.
  Consequences:
  - Do not use `fls`/`istat` timestamps or an `fls -m` body file for
    FAT-family media as UTC without converting them. Parse the stored offset
    (or, for FAT/FAT32, state that the zone is unknown and derive it from an
    anchor below).
  - The offset can differ between timestamps: a device that moved between
    zones or crossed a DST change will show different offsets across its
    files. Record the offsets you find and where they change; do not assume
    a single zone for the whole volume.
  - Corroborate the file-system offset with a time embedded independently of
    the file system (Office `ModifyDate` in Z, PDF creation date, a
    BitLocker BEK FILETIME, EXIF with offset). Agreement to within a minute
    or so supports both the offset and an unaltered clock.
  - Other zone-less sources: ZIP/DOS timestamps, some `.lnk`/INFO2 fields,
    EXIF `DateTimeOriginal` without an offset tag. List them as "zone
    unknown" rather than guessing.

### Volumes with no operating system (data-only media)

If no OS is present (no registry hives, `/etc/os-release`, or user
profiles), most of the checklist above has no answer. Say so, then record
what is available instead:

- **Originating-platform indicators:** OEM name and formatting-tool
  signature, `System Volume Information` contents (`IndexerVolumeGuid`,
  `WPSettings.dat` imply a Windows-formatted or Windows-used volume),
  `.Trashes`/`.fseventsd`/`.Spotlight-V100` (macOS), `.Trash-<uid>` (Linux).
- **Formatting/first-use time:** the volume serial (FAT/exFAT serials are
  often derived from the format time) and the oldest file-system
  timestamps, stated as an inference.
- **User and application names:** from document metadata (Office
  `Creator`/`LastModifiedBy`, application/version strings), not from an
  account database — mark them as metadata-derived, not account-derived.
- **Time zone:** from the file-system offsets or embedded time anchors (see
  above), not from a system setting.
- **Device identifiers:** volume serial/GUIDs, and any portable-device
  artifacts on the volume (Phase 7 does not apply, but note them).
- Record installed applications (name, version, install date where
  available) relevant to the case. This supports later artifact
  interpretation and can itself be evidentiary (e.g. presence of
  encryption, wiping, or remote-access software).
