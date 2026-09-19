# Phase 8 — Volatile / Memory Evidence

*(only if a RAM capture exists or the system was received powered on; otherwise mark N/A)*

- If evidence was received/found powered on, note whether volatile data
  was captured before shutdown and by whom. If you are the one capturing
  it, follow order of volatility — collect the most volatile data first
  (registers/cache, process/network state, RAM), then less volatile
  sources — and use trusted, external/read-only tooling rather than
  binaries already present on the subject system (RFC 3227).
- Record the RAM capture tool, version, and output format
  (raw/`.mem`/`.vmem`/etc.); confirm the capture was written to separate,
  write-protected media rather than back onto the subject disk.
- Hash the memory image like any other evidence (Phase 1 process,
  [intake-integrity.md](intake-integrity.md)) before analysis.
- With `volatility3`/`vol.py` (or equivalent), extract at minimum: the
  running process list (including parent/child relationships and any
  processes not matching an on-disk executable), active network
  connections, loaded modules/DLLs, and command-line arguments of running
  processes. These can reveal activity, encryption passphrases, or
  malicious code that never touched disk and so has no file-system
  artifact at all.
- Search the memory image for plaintext passwords, encryption keys, or
  decrypted content relevant to Phases 12/16
  ([encryption.md](encryption.md)). A mounted encrypted volume's key is
  very often recoverable from RAM while the system is live, and sometimes
  from a hibernation-file-derived memory snapshot (Phase 7,
  [os/windows.md](os/windows.md)) even after shutdown. Do this **before**
  attempting cracking.
- Note any indication the capture is incomplete (tool error, smear from
  continued system activity during capture, reported vs. actual physical
  memory size mismatch).
