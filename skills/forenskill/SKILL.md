---
name: forenskill
description: Operating procedure for forensically examining computer disk images (raw/dd, E01/EWF, AFF, VMDK/VHD) and memory captures — integrity verification and chain of custody, partition and file system analysis, deleted-file recovery and carving, Windows/macOS/Linux artifacts, browser/email/chat/cloud-sync artifacts, encrypted volumes and password recovery, timelines, and a final findings report. Use whenever the user asks to examine, triage, investigate, or analyze a disk image, forensic evidence, a DFIR case, or a suspect's drive, even if they don't say "forensic" explicitly.
---

# Forensic Disk Image Analysis — Claude Code Operating Procedure

This skill is the operating procedure for examining a computer disk image
in a Claude Code session. The work is split into numbered phases. This file
holds what applies to every phase — the Hard Rules, inputs, case directory
layout, tool inventory, and the phase map — and each phase has its own file
with the detailed steps, commands, and reasoning. Cite phase numbers in your
notes and report. The procedure follows the published standards listed in
[reference/sources.md](reference/sources.md); where a phase file and a cited
standard conflict, the standard governs.

Every step in a phase file is either done, not applicable, or flagged. Record
the result of each step you do in your notes; when a step doesn't apply (no
encrypted volume, no GPS photos), note "N/A" with a one-line reason; when a
step can't be completed, log it in `notes/anomalies.md`. Don't skip steps
silently — an unexplained gap in an examination is a defect.

Locate `template.txt` (the report template, used in Phase 19) at the start
of the engagement. If it can't be found, ask the user where it lives — do
not invent its contents.

Read the "Hard Rules" section below in full before running any command
against evidence.

## How this skill is organized

This file holds what applies to **every** phase: the Hard Rules, inputs,
case directory layout, tool inventory, and the phase map. Detail for each
phase lives in a separate file — read it when you reach that phase, not
before. Phase numbers are stable IDs: notes files, cross-references, and the
report template mapping all cite them, so never renumber.

Bundled resources (paths relative to this skill's directory):
`scripts/tool_inventory.sh` (tool presence/version check),
`reference/commands.md` (command quick reference), `reference/sources.md`
(standards), and `template.txt` (report template).

Work in numeric phase order unless a phase says otherwise. Phases 12–15 are
a loop, not a line: anything recovered in a later phase (a carved document,
a password found in slack, a decrypted archive) re-enters Phases 12–14 for
analysis. In `notes/exhibits.md`, record both the phase that *discovered* an
item and the phase that *analyzed* it. Read
[conventions.md](conventions.md) before starting Phase 0. After any context
compaction or session resume, re-read this file, `conventions.md`, and the
files in `notes/` before continuing.

Read skill and phase files one at a time with the Read tool — not several
concatenated through `cat`, which can truncate silently. If any output says
it was truncated, re-read the missing range before continuing. A phase is
"N/A" only after you have read its file and named the check that showed it
doesn't apply (e.g. "`fls` shows no `Windows/System32/config`").

At the end of every phase, append its results to the relevant `notes/` files
before starting the next one (methodology, subject list, timeline,
exhibits, anomalies). Do not batch note-taking for the end.

Any script or one-off parser that produces a number, offset, or timestamp
you report must be saved in `case_<id>/scripts/` before it is used, with the
interpreter version and the script's hash logged in `methodology.md`, and
described in the report as unvalidated unless it has been tested against a
known-good tool. Hand-written parsers are a last resort — prefer Sleuth Kit
primitives (`blkls`, `blkstat`, `ifind`, `icat -s`) where they cover the need.

---

## Hard Rules (non-negotiable, read first)

1. **Never write to the original evidence file or original media.** Every
   command in this procedure runs against a working copy or a read-only
   mount of a working copy. If a tool doesn't have a read-only/`ro` mode,
   don't use it directly on the image — mount it read-only first.
2. **Hash before you touch anything, and re-verify at the end.** If a
   hash you compute doesn't match a hash you were given, STOP and tell the
   user before proceeding further. Do not silently continue.
3. **Persist state to disk as you go, not just to conversation memory.**
   This is a long, multi-phase task and your context window will
   compact. The running notes files described below (methodology log,
   subject-ID list, timeline, exhibit list) are the actual work product —
   treat them as the source of truth, update them continuously, and
   re-read them after any compaction or when resuming a session instead
   of trying to recall prior findings.
4. **Record tool name + version for everything you run.** Append it to
   the methodology log at the time you run it, not from memory later.
5. **Check tool availability before relying on a tool.** Use
   `command -v <tool>` first. If a standard tool is missing, say so in
   the methodology log, try a reasonable substitute, and do not fabricate
   output as if the tool had run.
6. **Don't guess at findings.** If something is ambiguous, inconclusive,
   or you're not sure a signature hit is a real file, say so explicitly
   rather than asserting a clean conclusion. Mark phase items N/A
   explicitly rather than skipping them silently.
7. **Stop and ask the user (don't just proceed) when:**
   - A hash mismatch or acquisition error is found (Phase 1).
   - The legal scope of the examination is unclear or a finding appears
     to fall outside it.
   - You'd need to attempt password/encryption cracking that requires a
     time/resource decision (Phase 16) — propose the plan, get a go-ahead.
   - An action would be destructive or irreversible to anything outside
     your own working/output directory.
8. **Every timestamp you report must carry its time zone / UTC offset.**
   Determine the source system's configured time zone early (Phase 4)
   and normalize before building any timeline. More than one zone (and a
   DST change) can apply within one device's history, and some sources
   store local time with no zone at all (FAT, ZIP/DOS timestamps) — never
   assume a tool's "UTC" label is correct for these (Phase 4).

---

## Before You Start: Inputs

Confirm you have, or ask the user for:

- Path to the disk image (raw/dd, E01/EWF, AFF, VMDK/VHD, etc.) or the
  physical device if working from write-blocked hardware.
- Case/item number, examiner name (ask the user's name if not already
  known — do not invent one), examination date.
- Any provided hash-verification sheet for the evidence.
- Any statement of legal authority/scope (warrant, consent, engagement
  letter) and any scope limitation (date range, specific user, specific
  allegation).
- How to handle sensitive data in the report and whether any external
  lookups are permitted. Recovered financial account/card numbers, SSNs,
  and credentials may be the evidence, so whether to mask them (and where
  full values live, e.g. exhibit files) depends on who will read the
  report — ask, and record the answer in `notes/methodology.md`. Unless
  told otherwise, make no external lookups (web searches, public
  directories): nothing derived from the case (names, numbers, hashes,
  content) is ever sent outside the examination environment. If a lookup is
  approved, log the query, source, and date.
- Where the case working directory should live (see layout below) —
  default to `case_<id>/` in the current working directory unless told
  otherwise. Never create it inside this skill's own directory: case data
  and evidence must not end up in the skill installation or its git
  repository.

## Case Working Directory Layout

Create this structure at the start of the engagement (adjust the root
name to the case number):

```
case_<id>/
  evidence/
    image_copy/          # working copy of the image (or a note pointing
                          # to its path if too large to duplicate — never
                          # the original)
    hashes.txt            # every hash you compute, with source & timestamp
  notes/
    methodology.md         # running tool/command log (Phase 2)
    chain_of_custody.md     # transfers you perform or observe (Phase 0)
    subject_id.md             # running subject-identification list (Phase 5)
    timeline.md                 # consolidated dated-event list (Phase 17)
    exhibits.md                   # items-recovered tracking (Phase 18)
    anomalies.md                    # anything flagged for follow-up/STOP
  mount/
    <volume_label_or_offset>/        # read-only mount points, one per volume
  extracted/
    <volume_label_or_offset>/         # exported allocated + deleted files,
                                       # mirroring original paths
    carved/                            # orphaned carved items, named by
                                        # volume-relative byte offset
    manifest.sha1                       # SHA1 of every exported/carved/
                                         # decrypted item (update as you go)
  scripts/                             # any script that produced a reported
                                        # number (see above)
  report/
    findings_report.txt                  # final report, per template.txt
                                          # (Phase 19)
```

Initialize `notes/methodology.md`, `notes/subject_id.md`,
`notes/timeline.md`, and `notes/exhibits.md` as empty markdown files with
headers immediately — you will append to them throughout, not write them
once at the end.

## Tool Inventory (do this once, log the results)

Run the inventory script from this skill's `scripts/` directory (the directory
that contains this `SKILL.md`) and append its output to the methodology log:

```bash
bash <skill_dir>/scripts/tool_inventory.sh | tee -a notes/methodology.md
```

It reports the presence and version of every tool the phases rely on. Note
gaps in `notes/methodology.md` rather than failing silently — later phases say
which gaps matter. If the script can't detect a version, record it manually
from the tool's help banner.

If Sleuth Kit (`mmls`/`fls`/`icat`/etc.) is unavailable, tell the user
immediately, before continuing — most phases depend on it, and improvising
weaker substitutes for the whole exam isn't acceptable.

---

## Phase Map

Read the file for each phase when you reach it.

| Phase | Topic | Read |
|---|---|---|
| — | Notes-file formats, methodology logging, subject-ID list (Phases 2 and 5) | [conventions.md](conventions.md) |
| 0–1 | Setup, legal scope, chain of custody; evidence identification & integrity | [intake-integrity.md](intake-integrity.md) |
| 3–4 | Partition/volume layout; system baseline & time zone | [volumes-baseline.md](volumes-baseline.md) |
| 6, 15 | File system contents; unallocated-space / signature carving | [filesystem.md](filesystem.md) |
| 7 | OS-specific artifacts — read the file(s) matching the OS(es) found | [os/windows.md](os/windows.md), [os/macos.md](os/macos.md), [os/linux.md](os/linux.md) |
| 8 | Volatile / memory evidence | [memory.md](memory.md) |
| 9 | Network, communication & cloud-sync artifacts — read each family present | [user-activity/browsers.md](user-activity/browsers.md), [email.md](user-activity/email.md), [chat.md](user-activity/chat.md), [cloud-sync.md](user-activity/cloud-sync.md) |
| 10 | Virtual machine & container evidence | [virtualization.md](virtualization.md) |
| 11 | Anti-forensics / counter-forensic indicators | [anti-forensics.md](anti-forensics.md) |
| 12, 16 | Encrypted/protected volumes, files, and archives; password/encryption recovery attempts | [encryption.md](encryption.md) |
| 13–14 | Document & image content analysis; photo EXIF/GPS geolocation | [content-analysis.md](content-analysis.md) |
| 17–19 | Cross-correlation & timeline; exhibit tracking; report generation | [correlation-report.md](correlation-report.md), `template.txt` (read in full at Phase 19) |
| — | Quick command reference | [reference/commands.md](reference/commands.md) |
| — | Standards and sources the procedure is drawn from | [reference/sources.md](reference/sources.md) |
