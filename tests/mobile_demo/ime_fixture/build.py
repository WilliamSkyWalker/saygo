"""Build the offline fixture using an existing SDK/JDK; never install tools."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from saygo.devices.toolchain import background_options


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sdk", type=Path, required=True)
    parser.add_argument("--java-home", type=Path, required=True)
    parser.add_argument("--build-tools", default="35.0.0")
    parser.add_argument("--api", default="35")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    build_tools = args.sdk / "build-tools" / args.build_tools
    android = args.sdk / "platforms" / ("android-" + args.api) / "android.jar"
    suffix = ".exe" if os.name == "nt" else ""

    def java_tool(name):
        return args.java_home / "bin" / (name + suffix)

    def run(*command):
        result = subprocess.run([str(part) for part in command], capture_output=True,
                                text=True, errors="replace", timeout=90,
                                **background_options())
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        result.check_returncode()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="saygo-ime-fixture-") as temporary:
        root = Path(temporary)
        classes, dex = root / "classes", root / "dex"
        classes.mkdir()
        dex.mkdir()
        run(java_tool("javac"), "-encoding", "UTF-8", "-source", "8", "-target", "8",
            "-bootclasspath", android, "-d", classes, source / "InputActivity.java")
        run(java_tool("java"), "-cp", build_tools / "lib" / "d8.jar",
            "com.android.tools.r8.D8", "--lib", android, "--min-api", "23",
            "--output", dex, *classes.rglob("*.class"))
        unsigned = root / "unsigned.apk"
        run(build_tools / ("aapt2" + suffix), "link", "--manifest",
            source / "AndroidManifest.xml", "-I", android, "-o", unsigned)
        with zipfile.ZipFile(unsigned, "a", zipfile.ZIP_DEFLATED) as archive:
            archive.write(dex / "classes.dex", "classes.dex")
        aligned = root / "aligned.apk"
        run(build_tools / ("zipalign" + suffix), "-f", "4", unsigned, aligned)
        key = root / "fixture.p12"
        run(java_tool("keytool"), "-genkeypair", "-keystore", key,
            "-storepass", "android", "-keypass", "android", "-alias", "fixture",
            "-keyalg", "RSA", "-keysize", "2048", "-validity", "30",
            "-dname", "CN=Offline Input Test", "-noprompt")
        signer = build_tools / "lib" / "apksigner.jar"
        run(java_tool("java"), "-jar", signer, "sign", "--ks", key,
            "--ks-pass", "pass:android", "--key-pass", "pass:android",
            "--out", args.output, aligned)
        run(java_tool("java"), "-jar", signer, "verify", "--verbose", args.output)
    print(args.output)


if __name__ == "__main__":
    main()
