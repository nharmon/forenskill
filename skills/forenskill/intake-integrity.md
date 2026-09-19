# Phases 0–1 — Intake, Chain of Custody, Evidence Integrity

## Phase 0 — Setup, Legal Scope, Chain of Custody

### Before you start
- Confirm you are working against a copy of the evidence, never the
  original acquisition, and record the copy's own hash if it differs from
  the original's documented hash.
- Record in `notes/methodology.md`: case/item number, examiner name,
  examination date, and an evidence description (what the item physically
  is and where it came from).
- Locate any hash-verification document provided with the evidence and
  note its exact file name (you verify against it in Phase 1).
- Note the examination platform/OS and confirm write-blocking or
  read-only mounting is in place (or that you are working from a raw file
  copy).
- Confirm the legal authority for the examination (warrant, consent
  form, corporate policy, etc.) and note any scope limitation it imposes
  (date range, user account, file type, specific allegation). Do not
  examine or report on data outside an explicitly bounded scope without
  flagging the issue to the requesting party first (Hard Rule 7).
- If you personally received the physical item (rather than only an
  image), record its condition on receipt in `notes/chain_of_custody.md`:
  tamper-evident seal/bag number and whether intact, physical damage, and
  power state (on/off/unknown) at the time of receipt.
- If the item was received or found powered **on**, do not shut it down
  or begin imaging assumptions before considering whether volatile
  evidence (RAM, running processes, open encrypted volumes, network
  connections) needs to be captured first — see Phase 8
  ([memory.md](memory.md)). Pulling the plug on a running system destroys
  anything that was only ever in memory (RFC 3227 order of volatility).

### Chain of custody
- Confirm a chain-of-custody record exists covering the item from
  seizure/receipt through to your examination, with no gaps in time or
  possession.
- For every transfer of custody you can see in the record (or that you
  yourself perform), confirm it states: a unique identifier for the item,
  the date and time of transfer, the name of the person releasing it, the
  name of the person receiving it, and the purpose of the transfer (SWGDE
  Best Practices for Digital Evidence Collection). Log each in
  `notes/chain_of_custody.md`.
- Record where the working copy/image and all extracted/exported files
  are stored during your examination, and confirm this location is
  access-controlled and distinct from the original evidence storage.
- If you find any gap, inconsistency, or unexplained interval in the
  chain of custody, flag it explicitly in `notes/anomalies.md` rather than
  assuming it is immaterial — a broken chain can be used to challenge
  admissibility regardless of how sound the technical analysis is.
- Confirm your own actions are logged in a way a third party could
  audit: what you did, when, with what tool/version, and why (ACPO
  Principle 3 — an independent examiner should be able to follow your
  actions and reach the same conclusions). `notes/methodology.md` is where
  this lives.

## Phase 1 — Evidence Identification & Integrity

```bash
# Identify and size the image
file evidence/image_copy/<image>
ls -l evidence/image_copy/<image>

# Hash the image file itself — do this before any other command touches it
sha1sum evidence/image_copy/<image> | tee -a evidence/hashes.txt
md5sum  evidence/image_copy/<image> | tee -a evidence/hashes.txt
```

- Record the exact file name, size (bytes), and format of the image
  (raw/dd, E01, AFF, etc.) being examined.
- Compute **MD5 and SHA1** of the image file itself (both).
- If a companion package (zip, split archive, etc.) was provided,
  compute its hashes too and compare against any provided hash sheet.
  Record MATCH/MISMATCH explicitly in `evidence/hashes.txt` and
  `notes/methodology.md` — do not just write "verified."
- **If hashes mismatch anything documented: STOP, flag it in
  `notes/anomalies.md`, and tell the user before proceeding.** Do not
  silently continue as if everything is fine.
- For E01/EWF images, use `ewfinfo` to pull acquisition metadata
  (examiner, acquisition tool/version, source hash recorded at acquisition
  time, and any reported read errors) and compare its recorded hash
  against your own.
- If the acquisition log/report is available, check it for read
  errors, bad sectors, or incomplete-transfer warnings during imaging, and
  note whether any portion of the source was inaccessible to the original
  acquisition.
- Check whether the acquisition addressed the Host Protected Area
  (HPA) or Device Configuration Overlay (DCO) on the source drive (fields
  reporting native vs. reported/accessible sector counts). If native
  capacity exceeds accessible capacity and this was not resolved during
  acquisition, note that hidden sectors may exist that are absent from the
  image under examination.
