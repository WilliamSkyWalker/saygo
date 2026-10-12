# Desktop regression checks

This guide collects in-progress desktop work from the shared workspace. The launch/connection tests described below are not included in the 0.4.14 update-notification release; their source changes remain separate.

Run from the repository root with the desktop dependencies installed:

```sh
python -m unittest discover -s tests/desktop_demo -v
```

The desktop build workflow discovers this directory on Windows, macOS and Linux.
These tests do not call a model provider or operate real user applications.

`test_launch_runtime.py` uses the real InteractiveRuntime, SQLite persistence,
VisualResource adapter, action validation and dispatch journal. Only model
responses, native OS calls, captures and settling waits are fixtures.

| Scenario | Required result |
|---|---|
| Computer and browser connected; browser asleep; desktop pixels and focus change during model response | Launch catalog application exactly once, without capturing the unused browser; durable intent exists before native launch; completion uses a fresh post-launch image |
| Desktop pixels change before a click | Reject before sending input |
| Foreground focus changes before typing | Reject before sending input |
| Application disappears from the launch catalog | Reject before launching |
| Native launch response is lost | Keep `needs_review`; repeated request and restarted runtime never launch again |
| Pause or stop arrives during the model call | No launch and no submitted request |
| Model explicitly requests the browser | Capture it; preserve enabled-resource selection across a runtime restart |
| Requested browser cannot provide a screenshot | Reject model completion and request human intervention |
| Session contains non-ASCII app names and handoff notes on a non-UTF-8 system | Session reload and connection list preserve the text instead of dropping the session |

`test_launch.py` covers individual launch preconditions and routing.
`test_connections.py` covers connection discovery, bridge installation ordering,
application discovery and desktop coordinate/focus checks.

Passing these deterministic checks does not prove live model behavior, a real
application opening successfully, Chrome installation, or native macOS control.
Those require separate platform acceptance checks with recorded scope.
