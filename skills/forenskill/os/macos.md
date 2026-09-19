# Phase 7 — OS-Specific Artifacts: macOS

*(run this file if a macOS volume was found; otherwise mark N/A)*

Log every hive/database you parse as an exhibit, and push every
name/date/identifier into `subject_id.md` / `timeline.md` as you go.
Artifact behavior can change across macOS versions — confirm against the
specific build (Phase 4) where a finding is central to the case.

- Extract FSEvents records (per-volume, root-privileged) for a
  file-system activity history that survives even after the files
  themselves are deleted or the volume is reformatted (entries persist
  across some operations that would erase other artifacts).
- Extract `KnowledgeC.db` (application focus/usage) and, where present,
  Biome data for an application- and document-level activity timeline.
- Extract the Quarantine database (`QuarantineEventsV2`, per user) for
  a record of every file downloaded from the internet or received via
  AirDrop, including source URL and download time — this record persists
  even if the downloaded file itself was later deleted.
- Extract `TCC.db` (per-user and system) for a record of which
  applications were granted access to sensitive resources (camera,
  microphone, location, full disk access, etc.).
- Parse relevant plist files (LaunchAgents/LaunchDaemons for
  persistence, Login Items, recent items, and per-application preference
  plists) for configuration and usage history.
- Check for and process APFS snapshots and Time Machine backups (local
  or attached) as additional point-in-time sources per Phase 6.
- Review the Unified Log (`.tracev3`, if collected/exported at
  acquisition time) for OS- and application-level event detail. It is
  high-volume and typically has a limited retention window, so its absence
  is not itself suspicious.
- Note Keychain presence/lock state, but do not attempt to break its
  encryption outside the process documented in Phases 12/16
  ([../encryption.md](../encryption.md)).
