# Phase 9 — Cloud-Sync Client Artifacts

*(Other Phase 9 families: [browsers.md](browsers.md), [email.md](email.md),
[chat.md](chat.md))*

- Identify installed sync clients (OneDrive, Google Drive, Dropbox,
  iCloud Drive, Box, etc.) and their local configuration/log/database
  files (e.g. Dropbox's SQLite databases, Google Drive's `Cloud_graph.db`
  and `Sync_log.log`, OneDrive's per-account settings files).
- Record the synchronized account email/identifier and the list of
  synced file names with modification times and hashes where stored
  locally. Distinguish files that are cloud-only ("on demand" /
  placeholder) from those fully present in the local copy — the image may
  hold only the metadata, not the content, for the former.
- Check sync-client logs and local cache/thumbnail folders for evidence
  of files that have since been deleted from, or never fully downloaded
  to, the examined device.
- Cross-reference account identifiers and device names into
  `subject_id.md`.
