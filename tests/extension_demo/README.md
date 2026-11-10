# Browser extension checks

Offline checks:

```sh
node --test tests/extension_demo/test_*.mjs
python3 -m unittest discover -s tests/extension_demo -p test_bridge.py -v
python3 -m unittest discover -s tests/extension_demo -p test_shared_bridge.py -v
```

`test_startup.mjs` covers the saved connection choice across fresh browser
sessions, first install/legacy defaults, Release and Chrome Cancel, host failure,
concurrent Connect, late handshake/network setup, pending debugger cleanup, and
storage failures. It uses mock Chrome APIs and does not replace browser restart
acceptance. A failed preference write reports an error and an unknown startup
state while still revoking current control on Release.

`test_startup_live.py` uses a disposable profile and a real installed extension,
native host and CLI. It connects and enters text in its own localhost fixture,
closes and restarts Chromium, checks automatic reconnect and rejection of the old
page ID, explicitly selects the new page and checks fresh screenshots/input,
then releases and restarts again to check that control stays off. It never
injects a synthetic startup event. Run with `SAYGO_TEST_CHROME` and
`SAYGO_TEST_HEADED=1` under Xvfb with `xdotool` installed; the headed CI runner
includes this test. The browser's Load unpacked directory picker installs the
extension persistently. Command-line `--load-extension` treats it as a new
installation each launch and cannot validate the normal startup event.

Startup validation on 2026-10-14 (unreleased source):

- Linux/WSL, Chrome for Testing 153.0.8010.12: the final persistent-install test
  reproduced the old source's failure after browser restart, then passed with
  the fix. The headed run used the real popup, native host and CLI, verified PNG
  screenshots and English/Chinese fixture input, and retained the closed state
  after Release and another restart. The final screenshot was also inspected.
- 73 Node checks passed, including 22 startup/revocation regressions; 17 bridge
  and 14 shared-bridge checks passed with synthetic extension peers.
- All four existing real-extension cases passed in headless Chromium, including
  CLI/network payload and MCP client restart checks. This is separate from the
  headed browser restart case above.
- Chrome Cancel and storage/connection fault cases have mock coverage only.
  Windows/macOS restart acceptance and the Openbox CI runner were not run locally.
  No installed user extension was reloaded or upgraded.

```sh
SAYGO_TEST_CHROME=/path/to/chrome SAYGO_TEST_HEADED=1 \
  xvfb-run -a -s '-screen 0 1600x1000x24' \
  python3 -m unittest discover -s tests/extension_demo -p test_startup_live.py -v
```

Shared-bridge regression tests reproduce the desktop/WSL split installation,
both installation orders, stale defaults/registration, multiple live hosts,
identity migration, and preservation of explicit page bindings. They run real
native-host subprocesses and file IPC with a synthetic framed extension peer;
Windows directory/registry layout is injected. They do not replace real Chrome
acceptance.

The same native-host tests run on Windows in CI. Concurrent status readers on
Windows can cause `os.replace` to fail with WinError 5 or 32. Status publication
retries the same temporary file for at most one second; it never replays a browser
action. Regression tests cover successful retry and bounded failure with the
previous status preserved.

The live suite also runs `test_mcp_restart_preserves_connection_and_selected_page`:
a real Chrome extension and native host remain connected while two independent
MCP stdio servers start and exit. Each discovers the saved page, returns a
decodable PNG, clicks the test input and inserts text. The browser fixture checks
the final text and the same selected page; the existing headed CI gate runs this
case along with the background capture/scroll cases.

`test_cli_page_selection_preserves_foreground_window` requires headed Chromium.
It uses the same isolated profile, real extension and native host, with a separate
window kept in front. Real CLI requests select an inactive tab, select it again,
and connect with an explicit page ID. Each must bind the intended page while
preserving the visible active tabs and leaving the other window focused. On Linux, the test also checks the actual X11
active window and stacking order through `xprop`; run it under Xvfb with a window
manager. This covers selection separately from background capture and input.

`test_selection.mjs` verifies that logical page selection leaves every tab's
activity and window state unchanged, while background creation preserves existing
tabs. Stale page IDs, invalid URLs and disconnected calls must fail without changes.

`test_focus_mac_live.mjs` is an opt-in macOS check with a disposable browser
profile, extension copy, randomly named native host and an owned AppKit window.
It checks frontmost application PID and window order during real CLI selection,
creation, screenshots, input and `open_link_background` on an ordinary
`target="_blank"` anchor. The driver reads only the hyperlink URL at the observed
coordinates and creates an inactive tab; it does not run the link's click
handlers. The test checks the returned page ID, preserved selection, and rejection
of a button without a hyperlink without opening another page. It then verifies
the new page's background screenshot and input. Read-only tab oracles use the extension worker
(or explicit CDP `userGesture:false`); DOM result checks run after all foreground
assertions. This avoids page-evaluation user gestures contaminating focus tests.
Initial attachment must finish before a one-second idle baseline; screenshots
are not prewarmed. Arbitrary JavaScript-created windows are outside this check.
`focus_mac_fixture.py` requires PyObjC AppKit/Quartz; the Python interpreter also
needs the Saygo dependencies. The Node environment needs Playwright or
`SAYGO_TEST_PLAYWRIGHT_MODULE` pointing to a compatible Playwright module.
The browser must support `Extensions.loadUnpacked` via its debugging pipe.
Ordinary Node discovery skips this test; a skip is not macOS acceptance.
`SAYGO_TEST_FOCUS_LEFT_CLICK=1` instead exercises the ordinary left-click
foregrounding reproduction. It is expected to fail on affected macOS Chrome and
never counts as a passing background-link acceptance run. Optional
`SAYGO_TEST_FOCUS_DIAGNOSTICS=1` separates CLI page listing, raw selection and
capture probes before the acceptance sequence.

```sh
SAYGO_TEST_HEADED=1 SAYGO_TEST_CHROME=/path/to/chrome \
  SAYGO_TEST_PYTHON=/path/to/python3 \
  SAYGO_TEST_FOCUS_SCREENSHOT=/tmp/saygo-focus-result.png \
  node --test tests/extension_demo/test_focus_mac_live.mjs
```

With `SAYGO_TEST_FOCUS_SCREENSHOT` set, the run retains the input-result PNG plus
`-popup.png` showing the connected extension and `-webpage-popup.png` showing the
background-opened page's input result. `SAYGO_TEST_FOCUS_POPUP_SCREENSHOT` can
override the extension-popup path. Inspect these images alongside the assertions;
an available screenshot path alone is not visual acceptance.

Validation on 2026-11-09 (unreleased source, macOS arm64, Chrome 157.0.8103.39):

- The real CLI/native-host/extension run passed logical selection/reselection,
  inactive tab creation, coordinate link-URL opening, and screenshot/input on both
  the original and newly opened pages. The owned foreground app retained its PID
  and window order throughout. A non-link button was rejected without creating a
  page. The connected extension popup and both input-result PNGs were inspected.
- Ordinary left-click and middle-click link experiments both foregrounded Chrome;
  neither gesture is used by `open_link_background`. URL opening does not execute
  the fixture's click handler. The old extension still changed the visible active
  tab under the corrected selection test; this is distinct from OS activation.
- Earlier page-level Playwright oracle calls carried a synthetic user gesture.
  The final test uses worker queries or explicit `userGesture:false`, checks the
  oracle itself, and samples an idle baseline before cold screenshot requests.
- Offline checks: 90 JavaScript tests passed (the opt-in macOS case is separately
  skipped in ordinary discovery), 20 bridge tests, 25 shared-service tests and
  10 desktop decision tests passed. Same-document detached-node rejection,
  navigation/timeout during lookup and uncertain creation have mock coverage.
- Windows/Linux and other browser versions were not run for this change. Mobile,
  Playwright and arbitrary JavaScript-created windows are outside this acceptance.
  `claude plugin validate` could not run because the Claude CLI was unavailable.
  No user-installed extension was updated/reloaded; no version bump or release.

`test_capture.mjs` uses mocked window states (including minimized) to ensure
requests never activate tabs or change focus. These are control-policy checks,
not proof of minimized-window support. It also covers per-page pending ownership, late results, no post-timeout capture
dispatch, diagnostic availability, recovery after the original call finishes,
and preservation of screenshot diagnostics across subsequent size reads.

## Manual background capture matrix

Serve `capture_fixture.html` on localhost and open it in a dedicated test window
in the browser profile containing the extension. Bind a separate Saygo extension
session to its explicit page ID. Do not navigate or send input to unrelated tabs.

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory tests/extension_demo
saygo device screenshot --session capture-test
saygo device diagnose --session capture-test
```

With WSL, the browser must be able to reach the fixture server; running the server
on Windows avoids host forwarding dependencies. Use the real extension/Native
Messaging route for acceptance. A direct CDP harness only checks Chrome's capture
behavior, not the extension or bridge.

Check foreground, background but visible, fully covered, and inactive tab states.
Confirm the timestamp changes, the image matches the fixture, and the target
does not become active/focused. Leave the target tab inactive in a normal window
with no Saygo requests for 35 seconds and capture again. Compare bridge identity
and debugger attachment before/after. Close only fixture tabs when done.

## Observed coverage (2026-10-03)

Windows Chrome 154.0.8037.93 with the extension and WSL MCP client:

| State | Observation result |
| --- | --- |
| Foreground | Fresh screenshot |
| Background, visible | Fresh screenshot, foreground stayed on the cover window |
| Fully covered | Fresh screenshot, foreground stayed on the cover window |
| Minimized | Fresh screenshot, target remained minimized |
| Minimized after about 84 seconds without requests | Fresh screenshot, connection retained |
| Inactive tab | Fresh screenshot, tab remained inactive |

Background MCP observations took approximately 1.4–1.6 seconds, including bridge
and observation processing. A separate disposable-profile CDP experiment returned
20 screenshots across five window/tab conditions with/without a viewport clip;
all completed, approximately 0.03–0.17 seconds per capture. These measurements
are local samples, not latency guarantees. No alternate image source, browser
throttling flags, heartbeat, or automatic reconnect was needed.

The previously reported intermittent capture timeout was not reproduced in this
matrix. This does not prove its underlying cause has been fixed. The timeout
tests use deliberately unresolved mock commands; they validate request handling,
not recovery from a real Chrome renderer hang. Lock-screen, OS suspend, long-term
idle, other Chrome versions, and other operating systems remain unverified.

## Automated regression gates

Cloud regression jobs were removed for 1.0.0 at the user's explicit request.
Release workflows now build and upload only; they do not execute these tests.
The scripts below remain local entry points. macOS CDP-loaded focus acceptance
and Linux native persistent-install/restart acceptance exercise different platform
paths; neither result stands in for the other. Record browser and dependency
versions with each actual run. Hardware-only skips are not passes.

```sh
python -m pip install '.[mcp,browser,desktop,qa,selenium,mobile]'
python scripts/check_core_tests.py
node --test tests/extension_demo/test_*.mjs
```

The local Linux entry point runs the real extension/native host in headed Chromium under
Xvfb and Openbox. It checks foreground, background, covered and inactive
tab captures with exact fixture colors; window/tab state must stay unchanged.
It also checks a 35-second idle interval with an inactive tab in a normal window,
12 consecutive captures, actual scroll
movement in independent panes, fractional fine adjustments, reverse direction,
and top/bottom boundaries. Record browser integration failures explicitly with the local acceptance evidence.

```sh
python -m playwright install --with-deps chromium
# Install xvfb, openbox, x11-utils and xdotool with the system package manager.
xvfb-run -a -s '-screen 0 1600x1000x24' python scripts/check_browser_tests.py
```

Use an isolated virtual display. The live runner requires a functioning window
manager and fails if it cannot start. Minimized windows are excluded from
acceptance by the requested scope; inactivity coverage remains on background
tabs in normal windows. Fixture JavaScript and scroll offsets are
only test setup/oracles, never production perception. Multi-hour endurance tests
are deliberately excluded. Native Windows/macOS background browser behavior and
lock-screen/suspend still require dedicated platform environments.

The deterministic capture tests also cover navigation (including same-URL reload),
closing a tab, manual release while a capture is pending, simultaneous clients,
viewport changes, and cleanup of transient tabs. Simulated time advances the
extension's real deadline values; tests do not rely on 30–50 ms wall-clock races.
Navigation, closure and release must discard the outstanding image rather than
returning an observation from an obsolete page/control state.

Adaptive scroll tests validate model input images, capabilities, and dispatched
amounts using a scripted model. They do not establish that every real model will
choose an appropriate amplitude; that remains a separate model evaluation.

### Current regression finding

The expanded Linux headed run (Chrome for Testing 153.0.8010.12, Xvfb/Openbox)
reproduces `Page.captureScreenshot` timeouts when the extension target is minimized,
including after the short idle interval. The bridge remains connected. The same
run passes the other window/tab states, scroll assertions and capture burst.
Disabling Playwright viewport emulation did not resolve the failure. Removing the
clip in a disposable extension copy also did not resolve it; production capture
parameters have not been changed on that basis.

Minimized-window support was subsequently excluded from the requested scope.
The release gate no longer tests that state, and the 35-second idle check now
uses an inactive tab in a normal window. The historical failure above is not
resolved and the earlier successful Windows sample is not a support guarantee. The capture invalidation bugs exposed by deterministic
navigation/reload/closure/release tests have been corrected in this checkout.

An additional isolated Linux probe disables Playwright's automatic focus
emulation and switches to a different tab before each bridge operation.
Background screenshot and click succeed, but the first
`Input.synthesizeScrollGesture` times out after 20 seconds. Enabling focus
emulation in a disposable extension does not resolve that timeout. This does not
yet establish the cause of the Windows long-session screenshot incident.

`test_background_tab_input_after_manual_tab_switch` covers this missing case:
12 foreground/background transitions, screenshots, clicks, and alternating
scrolls in one pane. It checks tab/window state, exact fixture scroll offsets,
click counts and bridge identity. It stops sending input after a failed round.
The earlier scroll assertions only exercised the foreground tab. With wheel
input and temporary focus emulation, the new case passes all 12 rounds through
the real extension/native bridge on Linux. The launch also removes Playwright's
three background-throttling overrides. Before the scope change, the complete
headed run took about 146 seconds and failed the minimized and minimized-idle
capture checks; its other capture states and foreground scroll assertions passed.

A separate disposable Windows Chrome 154.0.8037.93 CDP probe reproduces a wheel
timeout without focus emulation. With focus emulation, two rounds pass before
an unlabelled state assertion fails; the follow-up diagnostic run was blocked
by approval timeouts. This is incomplete Windows evidence, not extension
acceptance or proof that the long-session screenshot incident is resolved.


### Background capture repair (2026-10-10)

A Windows inactive-tab observation succeeded once, then the action's preflight
capture timed out in `Page.captureScreenshot`. Layout requests and the native
bridge remained responsive; no wheel input was dispatched. This separates this
failure from a wheel command timeout.

Extension 0.4.13 scopes a `Page.startScreencast` / `Page.stopScreencast` pair around
screenshot capture so the hidden compositor continues producing frames. Stream
frames are acknowledged and discarded; observation images still use the original
viewport PNG capture and coordinate mapping. It does not activate tabs, focus
windows, or change viewport emulation. Timeout cleanup does not unlock an
unresolved screenshot or replay an action. Late stream preparation is cleaned
up without starting an expired screenshot.

Windows Chrome 154.0.8037.98 isolated extension checks passed 49 screenshots,
12 alternating wheel scrolls, and a screenshot after 35 seconds inactive. Each
round checked actual fixture scroll offsets, unchanged tab activity/window focus,
and stream cleanup; differing scroll positions also produced different image
hashes. The first check invoked the extension's
request handler through test-only hooks in a disposable copy, without native
messaging. A subsequent run through the real extension and a separate native host
passed the same 49 screenshots, 12 scrolls and 35-second idle check. The temporary
host registration was removed after the test. An earlier native-host attempt was
inconclusive because window focus changed during startup; the successful run
waited for startup to settle and retained the same strict state assertions.
This is not yet acceptance on the user's existing long-lived profile,
and does not establish minimized-window support.

The native-host integration regression now takes three consecutive inactive-tab
screenshots before each input. Deterministic capture tests also cover scoped
rendering, owned frame acknowledgement, cleanup on error/timeout/detach, and
late stream initialization. These mocked tests do not prove renderer liveness.

### Full network bodies (2026-10-13)

Linux Chrome for Testing 153.0.8010.12 passed
`test_large_network_body_through_extension_native_host_and_cli` in an isolated
headless profile against a local fixture. A 33 MiB JSON payload with a Unicode
tail exceeded Chrome's response cache; the extension recovered it from captured
stream bytes and returned it through the real native host and CLI. Decoded length,
SHA-256, the final JSON field, `source: stream`, and zero truncation/drops were
verified. The shared live setup also checked HTTP, WebSocket, SSE, visual input,
PNG capture, session reconnect, page selection and release. This was one live
test, not Windows/macOS, store-build, or existing-profile acceptance.

```sh
SAYGO_TEST_CHROME=/path/to/chrome python -m unittest tests.extension_demo.test_live.ExtensionLive.test_large_network_body_through_extension_native_host_and_cli -v
python -m unittest tests.extension_demo.test_bridge tests.extension_demo.test_shared_bridge tests.control_demo.test_network -v
for test_file in tests/extension_demo/test_*.mjs; do node "$test_file" || exit; done
```

The related Python suite passed 33 tests, including a real host process with a
simulated extension sending more than 32 MiB. JavaScript suites passed 51 tests,
including full long fields, multi-tab retention, cursor pagination, stream/cache
failures, delayed stream setup, burst body reads, capture clearing and Unicode
native-frame boundaries. Initial regressions reproduced truncation, the native
host's 32 MiB rejection and a split Unicode surrogate; these now pass. No user
installation, extension reload, hosted privacy-page deployment or release was
performed during that validation. The 0.4.18 release and its actual publication evidence are recorded in `docs/common/history/release-0.4.18.md`; its bundled extension is 0.4.17. Data already lost by an older capture cannot be restored by this fix.

The subsequent checkout reconciliation found an additional pending-counter fix:
`clear` now resets `pending_bodies`, and completion of an old capture cannot
decrement the new capture counter. Its regression failed against the published
0.4.17 extension and passes on the working branch. This follow-up is not in the
0.4.18 release assets and does not change their response-body retention behavior.
