# Phase 11 — Anti-Forensics / Counter-Forensic Indicators

- Check for installed or previously-installed wiping/cleaning software
  (via the Phase 7 program-execution and install history). The presence of
  such a tool is itself potentially significant even before determining
  what, if anything, it was used on.
- For files/timestamps material to the case, compare NTFS
  `$STANDARD_INFORMATION` timestamps against `$FILE_NAME` timestamps for
  the same `$MFT` record. User-mode timestomping tools typically alter
  only `$STANDARD_INFORMATION`, so a mismatch is a strong indicator of
  manipulation. Known limitation: if the file was later renamed or moved
  on the same volume, Windows copies the altered `$SI` values into `$FN`
  and the mismatch disappears — absence of a mismatch does not rule out
  timestomping. Corroborate with `$UsnJrnl`/`$LogFile` entries for the same
  file where available.
- Check Windows Security event logs for log-clearing events (1102) or
  the Event Log service being stopped (1100/1104), and note the account
  responsible (see Phase 7, [os/windows.md](os/windows.md)).
- Check for NTFS Alternate Data Streams on files of interest (Phase 6,
  [filesystem.md](filesystem.md)) — a common method of concealing a second
  payload.
- Note any large blocks of unallocated space containing
  high-entropy/random-looking data with no recoverable file structure,
  which can indicate secure deletion/wiping rather than ordinary deletion.
  Ordinary deletion typically leaves recognizable file remnants;
  overwritten/wiped space generally does not.
- Note any mismatch between a file's apparent age/usage (per
  surrounding artifacts) and an unusually "clean" or absent history for
  that same item elsewhere (e.g. no Prefetch/UserAssist entry for software
  you otherwise have strong evidence was used). This pattern can indicate
  selective artifact removal rather than the software simply never having
  run.
- For every anti-forensic conclusion, describe the specific evidence
  (specific mismatch, specific log entry, specific tool artifact) in
  `anomalies.md` and in the report — never assert "evidence of
  anti-forensic activity" as a bare conclusion.
