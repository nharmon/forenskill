# Phases 17–19 — Correlation, Exhibit Tracking, Report

## Phase 17 — Cross-Correlation & Timeline

- Explicitly list every fact appearing in more than one place (shared
  identifiers, matching dates, matching phone numbers/addresses/ID
  numbers) in `notes/anomalies.md` or a dedicated cross-correlation note.
  These are usually the strongest evidentiary links in the case and belong
  prominently in the report.
- Consolidate `timeline.md` into a full chronological list of every
  dated event found across all phases (document creation/edit dates, photo
  dates, encryption dates, file-system timestamps, registry/execution
  artifacts, event log entries), normalized to a single time zone/UTC per
  Phase 4.
- Note anything that ties an artifact to a specific external machine,
  account, or service (host names, volume/search GUIDs, cloud-sync device
  files). These are the leads most likely to yield a subject's real
  identity or location through follow-up outside this exam.

## Phase 18 — Exhibit / Items-Recovered Tracking
*(should already be current if you updated `exhibits.md` throughout; verify completeness now)*

- Confirm `exhibits.md` is a running list of every item extracted for
  review, grouped by volume and by allocation status (allocated,
  deleted-but-intact, carved/orphaned), each with its path or offset
  identifier.
- Confirm the extracted-copy storage location is recorded, is separate
  from the original evidence, and does not modify it.

## Phase 19 — Report Generation

- Re-verify every hash, size, offset, date, and count you plan to cite
  by re-running the command that produced it — don't rely on memory or
  earlier notes. Transcription and rounding errors are the most common
  defect in an otherwise-correct examination.
- Re-hash the working image and confirm it still matches the Phase 1
  hash (Hard Rule 2).
- Confirm every referenced artifact has its real file name/path cited
  (or, for orphaned items, its exact volume-relative offset) — never an
  internal tool ID that means nothing outside this session.
- Confirm Subject Identification findings (Phase 5) are complete and
  given prominent placement — this is usually the single most important
  output of the examination and should not be buried in narrative.
- Confirm every timestamp states or implies its time zone/UTC offset
  (Phase 4) and that conversions were applied consistently.
- If feasible, have a second examiner (technical/peer reviewer) check
  key findings and methodology before finalizing — independent review is
  standard practice for reducing single-examiner error and strengthens the
  report's defensibility.
- Cut work-log-only content (blow-by-blow narration of failed attempts,
  tool debugging detail, session/environment quirks unrelated to the
  findings) from the report. Summarize outcomes; keep only the methodology
  detail needed for reproducibility.
- Follow `template.txt` (in this skill's directory, or supplied with
  the case materials) for the report's structure and write the
  report to `report/findings_report.txt`. Read the whole template first;
  its bracketed text is instructions to you, not report content — no
  brackets or instruction text may remain in the finished report. Use
  the mapping below. Only if no template exists, write
  `report/findings_report.md` with at least: Evidence Summary,
  Methodology, Subject Identification Summary, Findings by
  Section/Phase, Cross-Correlation & Timeline, Recommendations/Next
  Steps, and Exhibit List.
- Check every internal section cross-reference in the report resolves
  to the section you actually mean, especially after any reorganization —
  including the template's own references (e.g. "Section 9",
  "Section 10", "Section 4/11"), which must be updated after any
  renumbering or omitted section.

### Mapping phases to template sections

| Template section | Populate from |
|---|---|
| Header, 1 Evidence Summary & Integrity | Phases 0–1: `evidence/hashes.txt`, `notes/chain_of_custody.md` |
| 2 Examination Environment & Methodology | `notes/methodology.md` (tool + version per line, in order first used) |
| 3 Partition / Volume Layout | Phase 3 |
| 4 Subject Identification Summary | `notes/subject_id.md` — **write last**, after all other sections |
| 5 File System Contents (one per volume) | Phase 6 listings; offsets are volume-relative bytes |
| 6 Encrypted volume (if any) | Phases 12, 16 |
| 7 Document & Image Analysis | Phase 13 |
| 8 Photos — EXIF/GPS (if any) | Phase 14 |
| 9 Unallocated-Space Carving | Phase 15 |
| 10 Password Recovery (only if unresolved) | Phase 16 |
| 11 Items Recovered | Phase 18 / `notes/exhibits.md` |
| 12 Conclusions & Next Steps | Phase 17 |

### Findings the template has no section for

The template predates the OS, memory, user-activity, virtualization,
anti-forensics, baseline, and timeline phases. Do not drop those findings
and do not stretch an unrelated section to hold them. Add sections, in the
template's own format (numbered heading, dashed rule, plain text):

- **System baseline & time zone** (Phase 4): add to Section 2 or 3 —
  OS/version, install date, configured time zone and UTC offset, clock
  anomalies. Every later timestamp depends on this.
- **New numbered sections after Section 9**, one per phase that produced
  findings, omitting those with none: OS-specific artifacts (Phase 7),
  memory (Phase 8), network/communication/cloud (Phase 9), virtual
  machines (Phase 10), anti-forensics indicators (Phase 11).
- **Timeline** (Phase 17): a new section immediately before Conclusions,
  in UTC with local time zone noted.

Renumber the sections that follow and fix every cross-reference (see the
last item in the list above). Where a phase was performed and found nothing, say so in
one line in the relevant section rather than omitting it; mark
not-performed phases N/A (Hard Rule 6). Omit template sections marked
"only if applicable" (6, 8, 10) when they don't apply.

Never edit `template.txt` itself; fill in a copy.
