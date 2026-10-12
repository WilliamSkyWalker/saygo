# Saygo 0.4.14 — Restore package update notifications

Package installations previously bypassed update checking and returned only a
pipx management message, so clients could not see a newer available version.
Version checking and notification now work independently of automatic upgrades.

- Check public PyPI in the background on package MCP startup. Report stable,
  non-yanked newer releases with their version, URL and pipx upgrade command.
- Refresh absent, expired or invalid caches from `device_sessions`, including
  when an older copied launcher still bypasses startup checks. The initial
  result may say `checking: true`; the completed result appears on a later call.
- Make package `saygo update --check` perform a real lookup. Keep automatic
  installation disabled; ignore stale managed-runtime upgrade flags.
- Remove reminders for versions already installed. Contain offline, metadata,
  cache-write and worker failures without blocking device operations.
- Consolidate ordinary documentation in `docs`, retaining runtime Markdown
  resources in their required locations. Add a 186-item project requirement
  baseline, 633 automated BDD contracts and 66 environment acceptance scenarios.

## Upgrade

```sh
pipx upgrade saygo-agent-control
```

Restart the Agent client. Package installations already bound to their pipx
interpreter do not need repeated setup. Pre-package copied-runtime installations
still need a one-time `saygo setup --client codex` migration (or their selected
client). Editing a checkout alone does not update installed 0.4.12 runtimes.

The browser extension stays at 0.4.13: this release does not change extension
files or require a browser reconnect. Existing managed GitHub installations
retain their checksum verification and opt-in update controls.

## Validation boundary

The added 633 tests run offline, including real worker threads, on-disk cache
handling and the MCP `device_sessions` result path. The 66 BDD environment
acceptance scenarios are specifications, not a claim of completed hardware runs.
See `docs/testing/results.md` and the release workflows for scoped results.
Python publishing is gated on Linux, Windows and macOS wheel installation and
repeat setup. Store review status remains separate from package publication.
In-progress desktop application changes in the shared development workspace are
not part of this release.
