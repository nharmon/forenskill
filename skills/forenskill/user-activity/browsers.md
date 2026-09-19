# Phase 9 — Browser Artifacts

*(repeat per browser/profile: Chrome/Edge/Brave/other Chromium-based,
Firefox, Safari. Other Phase 9 families: [email.md](email.md),
[chat.md](chat.md), [cloud-sync.md](cloud-sync.md))*

```bash
sqlite3 History     ".headers on" "select * from urls;"
sqlite3 Cookies      ".headers on" "select * from cookies;"
```

- Extract history, download history, and search/typed-URL entries, with
  timestamps converted to the time zone recorded in Phase 4.
- Extract cookies, saved form/autofill data, and stored/saved
  credentials where recoverable (note the encryption dependency on OS user
  credentials, e.g. Windows DPAPI).
- Extract the browser cache and examine it even where history has been
  cleared — users very often clear history without separately clearing the
  cache, and cache entries carry their own access timestamps.
- Enumerate installed extensions and note anything that could affect
  interpretation of browsing activity (ad blockers, VPN/proxy extensions,
  download managers).
- Note whether private/incognito browsing was used or is configured by
  default. Private-mode activity is not written to the on-disk history
  database by design, so its absence there does not mean the activity did
  not occur — if it matters to the case, check memory (Phase 8), pagefile
  (Phase 7), and DNS/network artifacts for corroboration.

Push every account name, email address, and identifier into
`subject_id.md`, and dated events into `timeline.md`.
