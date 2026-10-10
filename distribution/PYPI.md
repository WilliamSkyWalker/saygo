# Python package release

Package: `saygo-agent-control`. CLI: `saygo`. Version: `0.4.13` (beta software).
The release workflow publishes after installation and plugin preparation checks
on Linux, Windows and macOS. Verify the workflow and PyPI for publication status.

## Build and verify

```sh
python -m pip install build twine
python -m build --outdir dist/python
python -m twine check --strict dist/python/*
python scripts/check_python_package.py dist/python/saygo_agent_control-0.4.13-py3-none-any.whl
```

The default build produces an sdist and builds the wheel from that sdist, checking
that source releases contain all required build inputs. The wheel includes a
small allowlisted source ZIP for `saygo setup`. It contains the installer, plugin
manifests, Skill and extension files, with no local configuration or session data.
The setup command invokes the existing managed installer against that exact source
version. Python dependencies are downloaded as needed; this is not an offline bundle.

The smoke test installs into a disposable environment outside the checkout,
prepares both client bundles without registering them, imports MCP from the managed
runtime, and repeats setup to verify runtime reuse. It does not operate devices or
prove live client ingestion. CI runs the same check on Linux, Windows and macOS.

## Publisher configuration

The production PyPI Trusted Publisher is configured. Use these settings when configuring or restoring a publisher (TestPyPI is separate):

| Field | Value |
| --- | --- |
| Project | `saygo-agent-control` |
| Owner | `WilliamSkyWalker` |
| Repository | `saygo` |
| Workflow | `python-package.yml` |
| Environment | `pypi` (or `testpypi`) |

Create the matching GitHub environments. For unattended tag releases, leave
required reviewers disabled in the `pypi` environment. Adding a reviewer makes
each production upload wait for approval. Trusted Publishing uses GitHub OIDC
rather than committed credentials or a long-lived API token.

Push a version tag matching `distribution/release.json` (for example `v0.4.13`)
to publish automatically. The **Build release** workflow publishes the GitHub
release after its checks; **Python package** uploads to PyPI only after its build
and Linux, Windows and macOS installation checks pass. Ordinary branch pushes
do not publish packages.

For manual validation, run **Python package** with `publish: none`. Manual
`testpypi` and `pypi` publishing remain available; production publishing must
select the matching version tag. Pull requests only build and test.

If only validation scripts need correction, keep the existing version and tag.
Run the workflow from the corrected branch with `release_tag: v0.4.13` and
`publish: pypi`. Regression checks and package builds use that tag; installation
smoke tests use the workflow branch's validation script on all three platforms.
This does not replace an existing PyPI upload or move the release tag.

After publication, verify from outside the checkout:

```sh
pipx install 'saygo-agent-control[mcp]'
saygo setup --help
saygo setup --client codex
```

Install [Saygo Browser from the Chrome Web Store](https://chromewebstore.google.com/detail/ehomcchjfomfkcmbeinlcmpbaamdhfbo), then click
**Connect local bridge** in its popup. Store registration is the default; ordinary users do not supply an extension ID.

PyPI setup uses the installed package interpreter directly, so `pipx upgrade saygo-agent-control`
and an Agent client restart update MCP too. No repeated setup or copied runtime is needed.
Installations created before this change need one `saygo setup --client codex` migration
(or their selected client), using a package release containing this fix.
Native host files are staged on the next MCP startup after a package update. A connected host
keeps running until the user reconnects; Saygo never forces a browser disconnect.
Standalone GitHub installers retain their managed update channel.

References: [PyPA publishing guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/).
