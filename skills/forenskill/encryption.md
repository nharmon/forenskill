# Phases 12 and 16 — Encrypted Volumes and Password Recovery

Phase 12 identifies and tries to defeat protection without cracking;
Phase 16 is the cracking fallback and **requires a user go-ahead** (Hard
Rule 7 in [SKILL.md](SKILL.md)).

## Phase 12 — Encrypted or Protected Volumes
*(if any were flagged in Phase 3; otherwise mark N/A)*

- Identify the encryption type/product (BitLocker, LUKS, VeraCrypt,
  APFS encrypted, etc.) and extract whatever metadata is readable without a
  password: algorithm, volume/recovery GUIDs, associated host/device name
  or description, encryption-enabled timestamp.
- Search the **entire** image (not just the encrypted volume, which you
  can't read yet) for a plaintext copy of a password, recovery key, or key
  file. Full-text string extraction — including UTF-16LE on Windows-sourced
  evidence — across unallocated space is often productive.
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
  back through Phases 3 and 6–11. It is not a separate category of
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
