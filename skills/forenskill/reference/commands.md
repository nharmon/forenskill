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
| Mount E01 | libewf | `ewfmount image.E01 mnt/` |
| Metadata (docs/images) | ExifTool | `exiftool -a -G1 -s file` |
| String/artifact sweep | bulk_extractor | `bulk_extractor -o out/ image.dd` |
| File carving | foremost/scalpel/photorec | `foremost -i image.dd -o out/` |
| Embedded-file scan | binwalk | `binwalk --dd='.*' image.dd` |
| Registry parsing | RegRipper/hivex | `regripper -r SYSTEM -p system` |
| SQLite artifact DBs | sqlite3 | `sqlite3 History "select * from urls;"` |
| Memory analysis | Volatility 3 | `vol.py -f mem.raw windows.pslist` |
| Super-timeline | Plaso | `log2timeline.py out.plaso image.dd` |
| Password recovery | John/Hashcat | `john --wordlist=case.txt hashes.txt` |
| Hashing | coreutils | `sha1sum`, `md5sum` |

If a listed tool isn't installed and can't reasonably be installed in
this environment, note the gap in `notes/methodology.md`, identify the
closest available substitute, and flag in the final report which items
relied on a substitute tool.
