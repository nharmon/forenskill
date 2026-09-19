# Phases 12 and 16 — Encrypted Volumes and Password Recovery

Phase 12 identifies and tries to defeat protection without cracking;
Phase 16 is the cracking fallback and **requires a user go-ahead** (Hard
Rule 7 in [SKILL.md](SKILL.md)).

## Phase 12 — Encrypted or Protected Volumes, Files, and Archives
*(if an encrypted volume was flagged in Phase 3, **or** any password-protected
file, archive, or document turns up in any later phase; otherwise mark N/A
after checking — e.g. `file`/`7z l`/`zipinfo` over the exported files)*

- Identify the encryption type/product (BitLocker, LUKS, VeraCrypt,
  APFS encrypted, etc.) and extract whatever metadata is readable without a
  password: algorithm, volume/recovery GUIDs, associated host/device name
  or description, encryption-enabled timestamp.
- Search the **entire** image (not just the encrypted volume, which you
  can't read yet) for a plaintext copy of a password, recovery key, or key
  file. Full-text string extraction — including UTF-16LE on Windows-sourced
  evidence — across unallocated space and file slack is often productive.
  Build a candidate list systematically: every string near words such as
  "password", "pass", "pw", "key", "code", "PIN", from `strings` output,
  slack, unallocated clusters, and document text. Record each candidate with
  its offset.
- Test each candidate against **each** protected item. Passwords found on the
  evidence are not interchangeable: two containers can have two different
  passwords. A short candidate list drawn from the evidence is not a Phase 16
  attack and needs no go-ahead. Verification recipes:
  - Zip: `zipinfo -v <file>` identifies ZipCrypto vs AES; `unzip -tP
    '<candidate>' <file>` tests every member and reports CRC results.
  - 7-Zip: `7z t -p'<candidate>' <file>`. If file names are not header-
    encrypted, `7z l -slt` lists members and CRCs without a password; compare
    a member's CRC32 with a loose copy elsewhere on the image *before*
    decrypting — a match is useful corroboration.
  - Record which candidate opened which item, and how the result was verified
    (CRC match, valid structure), not just "opened."
- Key material found **without** its volume (a BitLocker recovery-key file, a
  `.BEK` startup key, a VeraCrypt key file for a volume not in the image) is
  an investigative lead, not a decryption: record its identifiers (key/
  protector GUIDs, embedded FILETIME timestamps), state that the corresponding
  volume or device is not in the image, and note that another device
  probably exists.
- If a memory image or hibernation file (Phases 7/8,
  [memory.md](memory.md)) is available from a period when the volume was
  mounted, search it for a resident decryption key before resorting to
  password recovery — this is often faster and more reliable than cracking.
- If a candidate key/password is found, verify its identifier/checksum
  against the volume's metadata **before** assuming it's correct.
- Document the exact decryption method used, including any workaround
  required by tool/permission limitations in your environment, in enough
  detail that another examiner can reproduce it.
- Once decrypted, treat the resulting volume like any other — route it
  back through Phases 3 and 6–11. Decrypted files and archive members
  re-enter Phases 13–14 and Phase 15 (see the loop note in SKILL.md); hash
  them into `extracted/manifest.sha1`. It is not a separate category of
  analysis.
- If decryption is **not** achieved, record every method attempted (so
  the next examiner doesn't repeat failed work) and your assessment of what
  would be needed to succeed.

## Phase 16 — Password / Encryption Recovery Attempts
*(for any remaining protected archive, document, or volume — propose the plan and get user go-ahead before large/slow attacks, per Hard Rule 7)*

- Identify the exact protection scheme (e.g. ZipCrypto vs. AES for a
  zip); this determines which tools and attack speeds are viable.
- Build a case-specific dictionary from every name/alias/address/phone
  number/date/ID number/keyword in `subject_id.md`, including plausible
  variants (case, common suffixes, concatenations); record the final
  candidate count.
- Attempt, in order: the case-specific dictionary → that dictionary
  with a mutation rule set → a general leaked-password wordlist if
  available → reasonable brute-force ranges (record exact character sets
  and length ranges tried, and whether each was exhausted or cut short) →
  a trained/Markov-style smart brute force if the tooling supports it.
- For each attempt, record: method, tool, candidate count or keyspace
  size, elapsed time/rate, and result (found / exhausted-no-match /
  stopped-early-reason). Don't just write "tried and failed" — the
  candidate counts are what let a future examiner judge what's left.
- Before committing to a large/slow attack (e.g. a mask-based or
  GPU-oriented method), sanity-check the achievable rate against **this**
  specific hash/cipher type. Generic time-budget guidance calibrated for
  fast hashes can be wildly wrong for slow ones (anything requiring full
  decompression or a memory-hard KDF per guess); computing the real
  keyspace size is quick and prevents wasting hours or days.
- If unsuccessful, record a clear recommendation for next steps
  (obtain the password from the subject / a linked account / a seized
  device, known-plaintext attack, extended compute, deprioritize, etc.).
