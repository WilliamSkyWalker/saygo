# Android input handoff fixture

This single-page Android app has two editable fields that accept Chinese and
English. It requests no permissions, uses no network, and has no account flow.
Use sample text only. Its package is `com.example.saygo.imefixture`.

Build with an already installed JDK and Android SDK. The script downloads nothing
and uses a temporary signing key, so uninstall an earlier fixture before replacing
it with an independently built APK. Build artifacts belong outside this checkout.

```sh
python tests/mobile_demo/ime_fixture/build.py \
  --sdk /path/to/android-sdk --java-home /path/to/jdk \
  --output /path/to/temp/input-handoff.apk
```

The defaults are SDK platform 35 and build-tools 35.0.0; override `--api` and
`--build-tools` for existing installations. On Windows, run with Windows Python
and Windows paths. Console tools use Saygo's background process options.

Use a dedicated emulator and Saygo session. Verify this sequence through the
normal CLI or MCP: connect, observe, focus the automatic field, type sample text,
handoff, let a person focus and type into the human field, resume, observe again,
and type into the automatic field. Repeat handoff and reconnect. Check both the
on-screen keyboard and a computer keyboard. Agent-injected text does not count
as human input verification. Keep the test emulator separate from business apps.
