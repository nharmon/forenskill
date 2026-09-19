# Phase 7 — OS-Specific Artifacts: Linux

*(run this file if a Linux volume was found; otherwise mark N/A)*

Log every hive/database you parse as an exhibit, and push every
name/date/identifier into `subject_id.md` / `timeline.md` as you go.

- Extract each user's shell history file (`~/.bash_history`,
  `~/.zsh_history`, etc., and `/root/`'s). History can be disabled or
  cleared — absence of expected history is itself worth recording.
- Review `/var/log/auth.log` (Debian/Ubuntu) or `/var/log/secure`
  (RHEL/CentOS) for authentication events: SSH logins, sudo/su usage, and
  PAM events, with account and source-address detail.
- Review `/var/log/syslog` or journald (systemd-based systems) for
  general system/service/kernel activity, and correlate service start/stop
  times against the timeline from other phases.
- Enumerate cron jobs (system crontab, per-user crontabs, `/etc/cron.*`)
  and systemd timers for scheduled/persistent execution.
- Review `/etc/passwd`, `/etc/shadow` (hash presence/format only — do
  not assume you may attempt to crack it without following Phase 16,
  [../encryption.md](../encryption.md)), and group-membership files for the
  account inventory from Phase 4 → `subject_id.md`.
- Check shell/environment history and package-manager logs (e.g.
  `apt`/`dpkg` or `rpm`/`yum` history) for installed software relevant to
  the case, including forensic/anti-forensic tools.
