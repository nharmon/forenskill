# Phases 3–4 — Volume Layout and System Baseline

## Phase 3 — Partition / Volume Layout

```bash
mmls evidence/image_copy/<image>
```

**Two different offset units are in play — don't mix them up:**

- Sleuth Kit tools (`fsstat`, `fls`, `icat`, `istat`, `tsk_recover`, …) take
  `-o <sector_offset>`: the **start sector** exactly as `mmls` reports it.
- `mount ... offset=` takes **bytes**: `byte_offset = sector_size × start_sector`
  (`mmls` prints the sector size in its header).

For raw/dd images, mount each volume read-only using the byte offset:

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
- Record installed applications (name, version, install date where
  available) relevant to the case. This supports later artifact
  interpretation and can itself be evidentiary (e.g. presence of
  encryption, wiping, or remote-access software).
