# Saygo 0.4.13 — Reliable inactive-tab capture

Inactive tabs could return one screenshot and then stall in Chrome's screenshot
interface, preventing the next scroll from being dispatched. Screenshot requests
now briefly start a page screencast to keep rendering active, then stop it on
completion or timeout. Returned observations still use the original viewport PNG;
stream frames are acknowledged and discarded. Tabs and windows stay in place.

- Preserve pending-request guards, stale-image rejection and no automatic input replay or reconnect.
- Verify 49 screenshots, 12 alternating scrolls and 35 seconds of inactive idle through a real Windows Chrome extension and native host in an isolated profile.
- Add stream lifecycle regression tests and consecutive inactive screenshots to the browser integration gate.
- Update the shared device skill to use 85–90% of the visible list height for continuous scanning, retaining overlap and adjusting to actual movement.
- Preserve the configured browser extension ID during setup upgrades unless explicitly overridden.
- Include package-based client setup improvements already on main, so package upgrades update the managed integration without copying another runtime.

## Upgrade

```sh
pipx upgrade saygo-agent-control --index-url https://pypi.org/simple --pip-args="--no-cache-dir"
```

Restart the agent client after upgrading. Installations using an older copied
runtime need a one-time `saygo setup --client codex` migration (or their selected
client). For unpacked extensions, replace the loaded folder with the development
extension ZIP, manually reload it, and click Connect local bridge. Keep that folder.
Store installations receive the extension update after Google approves it;
upgrading the Python package alone does not update a running browser extension.

## Validation limits

The Windows check used an isolated profile; it does not establish multi-hour
endurance or minimized-window support. A timeout still retains ownership of
Chrome's outstanding command and discards late images. Desktop binaries are not
part of this release workflow. Chrome Web Store submission is distinct from
approval; consult the release workflow for the current review state.
