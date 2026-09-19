# Phases 13–14 — Document/Image Content and Photo Geolocation

## Phase 13 — Document & Image Content Analysis

```bash
exiftool -a -G1 -s <file>      # full metadata, grouped, raw tag names
```

- For every document (PDF, DOC, etc.): extract full text and full
  metadata (author, creator/producer application, create/modify timestamps
  **with their raw timezone offset**, document/instance IDs). Use a
  dedicated metadata tool (`exiftool`) rather than trusting a generic
  tool's converted/localized timestamp display.
- Extract PDF text and metadata with `pdftotext` and `pdfinfo` (alongside
  `exiftool`) and note any disagreement between them.
- For Office documents, compare metadata **across documents**, not just
  within one: `Creator`/`LastModifiedBy` (the same name on a "third-party"
  letter and the subject's own résumé), `RevisionNumber`, `TotalEditTime`
  (a few minutes for a long document), `LastPrinted` earlier than `Created`
  (a reused template), and application/version strings. Report these as
  observations, not conclusions about intent.
- For every image: extract full EXIF metadata, not just what's visible
  — software/editor tags, ICC profile timestamps, and any embedded
  thumbnail can reveal edits or fabrication a viewer wouldn't show.
- To look at an image from a terminal session, convert it to a downsized
  JPEG in scratch space first (very large or HEIC images will not display
  otherwise), and give misnamed files the extension of their real type on the
  copy before viewing. Shell names with combining Unicode characters (e.g.
  `Resumé.docx`) may not match literally — use a glob.
- Financial identifiers: card numbers (Luhn) and routing numbers (ABA
  checksum) can be format-checked, and a scheme/BIN mismatch or a routing
  number shared by two supposedly different institutions is worth noting.
  These checks show only that a number is well-formed, not that it is
  genuine, and no card, account, or routing number is ever tested against a
  live system or looked up externally. Follow the data-handling instruction
  you were given at intake for how they appear in the report.
- Never send case content to an external service. Verification of public,
  non-case facts (e.g. an OS release date, a public routing-number
  directory) is allowed only if the user approved lookups at intake; log
  the query, source, and date. Otherwise list such points in the report as
  "not externally verified."
- For images/documents that appear digitally created or edited (not a
  scan/photo of something real), state the specific evidence for that
  conclusion (editor tag, profile timestamp, layered PDF structure, etc.)
  rather than just asserting it looks fake.
- For any professionally-produced or stock reference material found
  alongside apparent forgeries, note it separately as likely research
  material rather than conflating it with the forged items themselves.
- Cross-check every name/number/date found here against the running
  Subject Identification list (`subject_id.md`, Phase 5), and add new ones.

## Phase 14 — Photos: EXIF / GPS Geolocation
*(if photos with GPS are present; otherwise mark N/A)*

```bash
exiftool -gpslatitude -gpslongitude -gpsaltitude -gpsdatestamp -gpstimestamp -datetimeoriginal <file>
```

- For every photo, extract: capture device/software, `DateTimeOriginal`
  **with its raw offset**, and the full GPS block (lat/long converted to
  decimal degrees, altitude, GPS timestamp/date stamp if present).
- Convert GPS coordinates to a real-world location and, where feasible,
  visually confirm the location against the image content itself
  (landmarks, signage, etc.) rather than relying on coordinates alone.
- Build a timeline across all photos and cross-reference it against
  dates found elsewhere in the case (document dates, encryption-enabled
  dates, etc.) in `timeline.md`.
- Flag any internal inconsistency (e.g. GPS date stamp vs. capture
  date-time disagreeing by more than a timezone offset can explain) as an
  anomaly requiring further corroboration in `anomalies.md`. Don't
  silently "fix" it by picking whichever value seems more convenient.
- To interpret an EXIF/GPS conflict, convert the GPS UTC date-time to local
  time using the time-zone and DST rules in force *at the GPS location on
  that date*, then compare with `DateTimeOriginal` and its offset tag. Same
  clock time but a different date, or an offset label that disagrees with
  the location's DST state (e.g. labelled −07:00 where local time was −06:00
  daylight time), suggests rewritten EXIF dates. Report it as an
  inconsistency with the evidence, not as proof of tampering. Also compare
  embedded software/OS versions against image numbering and dates within
  the set (e.g. version strings that go backwards while file numbers rise).
  Checking a version against its public release date is an external lookup:
  do it only if approved, otherwise list it as not verified.
