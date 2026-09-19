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
- For every image: extract full EXIF metadata, not just what's visible
  — software/editor tags, ICC profile timestamps, and any embedded
  thumbnail can reveal edits or fabrication a viewer wouldn't show.
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
