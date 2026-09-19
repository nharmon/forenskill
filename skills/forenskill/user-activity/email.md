# Phase 9 — Email Artifacts

*(Other Phase 9 families: [browsers.md](browsers.md), [chat.md](chat.md),
[cloud-sync.md](cloud-sync.md))*

- Locate and process local mail stores (Outlook PST/OST, Thunderbird
  mbox/Maildir, Apple Mail, or standalone EML/MSG files); extract **full**
  headers, not just the displayed sender/recipient/subject.
- From the full headers, record the actual originating/relay path
  (`Received:` chain) and authentication results (SPF/DKIM/DMARC) where
  present, rather than trusting the display "From" name alone.
- Note attachments separately and process them per Phases 13/14 as
  applicable ([../content-analysis.md](../content-analysis.md)).
- Check deleted-items/trash folders and, where the mail-store format
  supports it, recover deleted-but-not-purged messages.

Push every address, alias, and identifier into `subject_id.md`, and dated
events into `timeline.md`.
