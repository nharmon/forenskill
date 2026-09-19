# Conventions — Methodology Log, Subject ID, Notes Files

*(Phases 2 and 5)*

These are not one-time phases. They are running conventions that apply
through the whole engagement. The Hard Rules in [SKILL.md](SKILL.md) apply
here as everywhere. Not every item in every phase applies to every case
(e.g. no encrypted volume, no GPS photos) — mark those N/A with a reason
rather than skipping them silently.

## Phase 2 — Methodology Logging & Tool Validation

Record as you go, not at the end.

- Confirm the Tool Inventory results (SKILL.md) are logged in
  `notes/methodology.md`.
- List every tool used and its version (`tool --version`) **as you use
  it** — this is much harder to reconstruct accurately after the fact.
- Every non-trivial command sequence goes into `methodology.md` as you
  run it — command, tool version, purpose, and outcome. For each
  non-obvious or multi-step technique (e.g. decrypting a volume without
  root, recovering a password, carving a file by hand), write down the
  exact commands/approach while it's fresh: this becomes the report's
  methodology section and must be reproducible by another examiner.
- Confirm and note that no step wrote to the original evidence file.
- If any tool/process behaved unexpectedly (crashed, hung, produced
  incomplete output), note it immediately with enough detail to assess
  later whether that tool's results are complete or partial.
- For any finding that is central to the case conclusions (not routine
  housekeeping), corroborate it with a second, independently-coded tool
  where practical, and record what each tool reported (note in
  `methodology.md` which was primary and which corroborating). Treat
  agreement between two tools as corroboration, not proof — both can share
  the same underlying misinterpretation of a format (NIST CFTT guidance on
  forensic tool testing/validation).
- Prefer tools that have published test results or are in general
  forensic use over unvalidated/one-off scripts for any finding that will
  be reported as fact. If only an unvalidated method is available, say so
  explicitly in the methodology.

## Phase 5 — Subject Identification (running list)

Build this incrementally as you find each item. Update
`notes/subject_id.md` continuously through Phases 6–15 — do not wait until
the end to reconstruct it.

Every item below found in any later phase gets a line in `subject_id.md`:
`<value> | <source file/artifact/field> | <phase>`.

- Every name or alias appearing on any document, image, or metadata
  field, and which specific file it came from.
- Every address appearing anywhere, and which file/field it came from.
- Every phone number, and which file/field it came from.
- Every date of birth, physical description, or other identifying
  biographical detail, and its source file.
- Every username, computer name, account name, or device identifier
  (from volume labels, encryption metadata, cloud-sync artifacts, etc.).
- Any ID/certificate/account/invoice number that recurs across more
  than one document — these are high-value cross-correlation points.
- Once the list is built (and periodically before then), identify which
  items corroborate each other (same phone number on two aliases'
  documents, etc.) and note the linkage. This becomes the report's Subject
  Identification Summary and Cross-Correlation findings.
- If a real-world identity theory presents itself (e.g. the case
  resembles a known public case/persona), state it explicitly as an
  investigative lead, **not** a confirmed fact, and note how it could be
  verified independently.

## Other running notes files

- **`notes/timeline.md`** — every dated event you encounter, appended as
  found. Timestamps carry their time zone/UTC offset (Hard Rule 8) and are
  normalized to the Phase 4 time zone. Consolidated in Phase 17.
- **`notes/exhibits.md`** — every volume, exported item, parsed
  hive/database, and carved item: path, allocation status, size, and exact
  byte offset for carved items. Verified for completeness in Phase 18.
- **`notes/anomalies.md`** — anything flagged for follow-up or STOP:
  hash mismatches, custody gaps, timestomping indicators, ADS, log
  clearing, timestamp inconsistencies. Cite the specific evidence, never a
  bare conclusion.
- **`notes/chain_of_custody.md`** — custody transfers you perform or
  observe (who, what, when, why).
- **`evidence/hashes.txt`** — every hash you compute, with source and
  timestamp.
