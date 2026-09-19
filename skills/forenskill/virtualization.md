# Phase 10 — Virtual Machine & Container Evidence

*(if any VM/container artifacts are found; otherwise mark N/A)*

- Identify virtual machine disk files (VMDK, VHD/VHDX, QCOW2, etc.),
  configuration files (`.vmx` and similar), snapshot files
  (`.vmsn`/`.vmsd`), and suspended-state files (`.vmss`) on the host
  volume.
- Treat each virtual disk as its own item of evidence: hash it (Phase
  1, [intake-integrity.md](intake-integrity.md)), determine its internal
  partition/volume layout (Phase 3,
  [volumes-baseline.md](volumes-baseline.md)), and process its contents
  through Phases 4–15 like a physical volume. Do not assume VM contents are
  out of scope.
- For snapshots, note the parent/child relationship between disk
  states and which snapshot represents which point in time. Examine more
  than the most current state if intermediate snapshots exist — data
  deleted in the host's view may still exist in an earlier snapshot's
  child-disk chain.
- Note that a virtual disk can itself contain data carried over from
  the host at creation time (e.g. thin-provisioned sparse disks sometimes
  retain host-disk remnants in unallocated regions). Do not assume every
  byte found within a VMDK originated inside the guest.
- Treat any `.vmss`/`.vmem` suspended-state file as a memory image
  (Phase 8, [memory.md](memory.md)).
- Identify container runtime evidence (Docker/Podman image and
  container storage, container logs) and note image names, container IDs,
  creation times, and any bind-mounted host paths.
