# Quick Command Reference

`<sector_offset>` is the **start sector** from `mmls`, used with Sleuth Kit
`-o`. Only `mount ... offset=` takes bytes (`sector_size × start_sector`).
See [../volumes-baseline.md](../volumes-baseline.md).

| Purpose | Tool | Example |
|---|---|---|
| Partition table | Sleuth Kit | `mmls image.dd` |
| Volume info | Sleuth Kit | `fsstat -o <sector_offset> image.dd` |
| Directory listing (alloc+deleted) | Sleuth Kit | `fls -r -p -o <sector_offset> image.dd` |
| MAC-time body file | Sleuth Kit | `fls -r -m <mount_prefix> -o <sector_offset> image.dd` |
| Export files | Sleuth Kit | `tsk_recover -e -o <sector_offset> image.dd out/` |
| Read specific file by inode | Sleuth Kit | `icat -o <sector_offset> image.dd <inum> > out` |
| File slack, whole volume | Sleuth Kit | `blkls -s -o <sector_offset> image.dd` |
| File slack, one file | Sleuth Kit | `icat -s -o <sector_offset> image.dd <inum>` (prints content **then** slack — skip the file's size) |
| Unallocated blocks | Sleuth Kit | `blkls -A -o <sector_offset> image.dd` |
| Block allocation status / owner | Sleuth Kit | `blkstat -o <sector_offset> image.dd <block>`; `ifind -d <block> -o <sector_offset> image.dd` |
| Mount E01 | libewf | `ewfmount image.E01 mnt/` |
| Metadata (docs/images) | ExifTool | `exiftool -a -G1 -s file` |
| String/artifact sweep | bulk_extractor | `bulk_extractor -o out/ image.dd` |
| File carving | foremost/scalpel/photorec | `foremost -i image.dd -o out/` |
| Embedded-file scan | binwalk | `binwalk --dd='.*' image.dd` |
| Registry parsing | RegRipper/hivex | `regripper -r SYSTEM -p system` |
| SQLite artifact DBs | sqlite3 | `sqlite3 History "select * from urls;"` |
| Memory analysis | Volatility 3 | `vol.py -f mem.raw windows.pslist` |
| Super-timeline | Plaso | `log2timeline.py out.plaso image.dd` |
| PDF text / metadata | poppler | `pdftotext file.pdf -`; `pdfinfo file.pdf` |
| Zip protection / test password | unzip | `zipinfo -v f.zip`; `unzip -tP '<pw>' f.zip` |
| 7-Zip list CRCs / test password | 7z | `7z l -slt f.7z`; `7z t -p'<pw>' f.7z` |
| Password recovery | John/Hashcat | `john --wordlist=case.txt hashes.txt` |
| Hashing | coreutils | `sha1sum`, `md5sum` |

## When a command returns nothing

- `mmls` empty or `fdisk -l` shows bogus partitions: look at sector 0 with
  `xxd -l 96` and try `fsstat` with no `-o` (partition-less media) — see
  [../volumes-baseline.md](../volumes-baseline.md).
- `blkls -s` empty: the file system may not support slack listing, or every
  file's slack may be zero-filled; check with `tr -d '\0' | wc -c`, and
  note which it was.
- `ifind -d` says "Inode not found" for an *allocated* block: the block has
  no owner — treat it as a lead, not a tool error.
- `fls -m` times on FAT/exFAT look wrong or all in one zone: they are local
  times — see the FAT-family paragraph in Phase 4.

If a listed tool isn't installed and can't reasonably be installed in
this environment, note the gap in `notes/methodology.md`, identify the
closest available substitute, and flag in the final report which items
relied on a substitute tool.
