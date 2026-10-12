# Saygo 0.4.16 — Shared browser bridge and native desktop connections

Windows desktop and WSL previously selected different native-host directories.
An extension connected to one could appear offline to the other, even after a
PyPI upgrade. Both clients now discover the browser OS's registered and live host.

## Browser connection and upgrade repair

- Share one Windows bridge between desktop, Windows Python and WSL. New installs
  use `%LOCALAPPDATA%/Saygo/browser-bridge`; a working legacy directory is retained.
- Probe the host before reporting it connected. Report multiple live hosts,
  incompatible extension identities and unresponsive hosts without choosing a
  different browser silently.
- Check actual registration and the live directory on package startup, including
  when the Python version has not changed. Repair registration drift without
  disconnecting the running extension.
- Preserve saved page bindings. Create an explicitly named session and select
  its intended page when recovering an obsolete binding.
- Bound retries for Windows status-file sharing violations so a concurrent reader
  does not immediately terminate the host. Browser actions are never replayed.
- Display the actual connection failure instead of always asking users to connect
  the extension again. Native-host diagnostics now identify version `0.4.16`.

## Desktop application

- Add a first-use welcome flow, automatic native computer connection, launchable
  application inventory and whole-computer control on Windows/macOS.
- Observe browser resources when the task needs them; preserve resource choices
  across task recovery. Pause automatic rebinding while a task owns the resource.
- Improve model configuration, masked token management and actionable connection
  errors. Minimize the controller during whole-computer tasks and restore it when
  the task finishes or needs human input.
- Include Windows runner resources in the packaged application. Desktop archives
  are built on their target operating systems and are unsigned beta builds.

## Upgrade and component versions

```sh
pipx upgrade saygo-agent-control
```

Restart the Agent client to load the new Python code. Package installations keep
their pipx interpreter. Existing connections stay alive; an already running host
keeps its current code until the user reconnects. No automatic disconnect occurs.
Desktop users download the matching `SaygoDesktop-0.4.16-*` release asset after
the desktop build has completed; desktop updates are not automatic.

The Python package, managed installer and newly built native host use `0.4.16`.
The browser extension remains `0.4.13`, with the same protocol and extension ID.
Its files have not changed, so this release needs no new extension upload.
Version `0.4.15` was previously withdrawn and is not reused.

## Validation boundary

Regression coverage includes real native-host subprocesses with a synthetic
extension peer, shared-directory discovery, same-version upgrade repair and
Windows file-sharing failures. The isolated real Chrome suite starts two separate
MCP servers, verifies page discovery and returned PNGs, and checks actual input
after a restart. The release gate also runs the CLI Playwright browser suite.

PyPI publishing is gated on clean wheel installation and repeat setup on Linux,
Windows and macOS. Desktop builds run Qt tests and startup checks; these do not
establish complete GUI task acceptance on all operating systems. Android/iOS
hardware acceptance is not part of this release. See the tagged workflows and
`docs/testing/release-0.4.16.md` for actual results and outstanding checks.
