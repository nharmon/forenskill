# Phase 7 — OS-Specific Artifacts: Windows

*(run this file if a Windows volume was found; otherwise mark N/A)*

Log every hive/database you parse as an exhibit, and push every
name/date/identifier into `subject_id.md` / `timeline.md` as you go.
Artifact behavior can change across Windows versions — confirm against the
specific build (Phase 4) where a finding is central to the case.

## Registry hives
- Extract and parse `SYSTEM`, `SOFTWARE`, `SAM`, `SECURITY`, and each
  user's `NTUSER.DAT` / `UsrClass.dat` (including any recoverable prior
  copies in `RegBack` or Volume Shadow Copies). Parse with
  `regripper`/`hivexml`/equivalent.
- From SAM, record every account's RID, creation / last-login /
  last-password-change timestamps, and group membership; cross-check
  against the Phase 4 account list → `subject_id.md`.
- Record mounted-device and drive-letter mapping history
  (`MountedDevices`, `MountPoints2`) and USB device connection history
  (`USBSTOR` / USB enum keys, first/last-connected times, serial numbers),
  and cross-reference serials against `setupapi.dev.log`.

## Program-execution evidence
- Extract Prefetch (`.pf`) files: executable name, run count, first/
  last (and, where available, up to the last 8) run timestamps, and
  files/directories referenced during startup.
- Extract `Amcache.hve` application-execution entries (path, SHA-1,
  first-seen time) and the SYSTEM hive's AppCompatCache/ShimCache entries.
  ShimCache alone does not reliably prove execution — corroborate it, don't
  treat it as sufficient on its own.
- Extract UserAssist (GUI-launched program) entries and BAM/DAM
  (Background/Desktop Activity Moderator) entries from SYSTEM. Each
  reflects a different definition of "ran" — say which you are relying on.

## File/folder-access evidence
- Extract ShellBags (folder-navigation history, including for folders
  no longer present) and RecentDocs / typed-paths registry entries.
- Extract LNK (shortcut) files and Jump List entries
  (AutomaticDest/CustomDest): target file path, volume serial, MAC times of
  the target at time of access, and (for LNKs on removable media) the
  originating device's volume serial and label.
- Extract the Windows Search index (`Windows.edb`) and Thumbcache/
  IconCache entries where present — a thumbnail can survive after the
  source image/document itself has been deleted.

## Deleted-item & journal artifacts
- Examine `$Recycle.Bin`: pair each `$I` file (metadata: original path,
  deletion time, size) with its corresponding `$R` (content) file.
- Parse the NTFS `$MFT` directly (not just via directory listing) for
  every volume, including entries for deleted files whose parent directory
  entry no longer exists.
- Parse `$LogFile` and `$UsnJrnl` (USN Journal) for file/directory
  create, rename, and delete operations not otherwise visible, and check
  any Volume Shadow Copies for older USN Journal data that has rolled off
  the live journal.
- Where a Volume Shadow Copy is available, mount/process it as its own
  point-in-time file system per Phase 6, not merely as a source of
  individual recovered files.

## Event logs (`.evtx`)
- Extract Security, System, Application, and (if present) PowerShell
  Operational logs, and record the configured retention/max-size settings
  so gaps can be explained rather than assumed innocuous.
- At minimum, review for:
  - successful/failed logons (**4624/4625**) and their logon type
    (interactive, network, RDP, etc.), and the account that performed
    each;
  - privileged-logon and account/group-membership changes (**4672, 4720,
    4728, 4732**);
  - scheduled-task creation/change (**4698/4702**);
  - critically, Security log clearing (**1102**) or Event Log service stop
    (**1100**), a well-known anti-forensic action — always flag it if
    present, together with the account that triggered it (see Phase 11,
    [../anti-forensics.md](../anti-forensics.md)).
- For remote-access cases, review RDP-specific events (4778/4779, 1149,
  `TerminalServices-RemoteConnectionManager`) and, where present, cached
  RDP bitmap fragments.

## Persistence & scheduling
- Enumerate Run/RunOnce registry keys, Startup folders, Scheduled Tasks
  (including their XML definitions and last-run results), installed
  Services, and WMI event subscriptions for anything that executes
  automatically. These are both persistence indicators and independent
  evidence of what software was actively used.

## Virtual memory & other system files
- Where present, process `pagefile.sys`, `swapfile.sys`, and
  `hiberfil.sys` for string/artifact extraction (URLs, credentials,
  command lines, encryption keys, remnants of in-memory-only activity) —
  `bulk_extractor` or `strings` plus manual review. `hiberfil.sys` is
  effectively a full RAM snapshot at last hibernation and can be processed
  like a memory image (Phase 8, [../memory.md](../memory.md)).
- If print activity is relevant, check the print spooler for surviving
  EMF/SPL spool files, which can reconstruct the content of a printed
  document after deletion.
- Extract Windows Timeline / `ActivitiesCache.db` where present for a
  cross-application activity history with timestamps.
- Extract SRUM (`SRUDB.dat`, System Resource Usage Monitor) for
  per-application network usage and execution history, which can fill gaps
  left by other execution artifacts.
