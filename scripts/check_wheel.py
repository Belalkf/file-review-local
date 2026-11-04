"""Check packaged browser assets and smoke-test an isolated installation."""

from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import tarfile
import venv
import zipfile


def check_installation(binary, root, environment):
    """Exercise every presentation path outside the source checkout."""
    command = str(binary / "file-review")
    result = subprocess.run([command, "--demo", "--json"], check=True, cwd=root,
                            env=environment, capture_output=True, text=True, timeout=15)
    assert json.loads(result.stdout)["demo"] is True
    plan = subprocess.run([command, "--demo", "--plan", "--task", "Test export"],
                          check=True, cwd=root, env=environment,
                          capture_output=True, text=True, timeout=15)
    assert 'User task: "Test export"' in plan.stdout
    assert "No language parsing" in plan.stdout
    output = root / "report.html"
    subprocess.run([command, "--demo", "--no-open", "--output", str(output)],
                   check=True, cwd=root, env=environment, timeout=15)
    assert "Find the files" in output.read_text()
    subprocess.run([str(binary / "python"), "-m", "file_review", "--version"],
                   check=True, cwd=root, env=environment, timeout=15)


def main():
    wheels = list(Path(sys.argv[1]).resolve().glob("*.whl"))
    if len(wheels) != 1:
        raise SystemExit("Expected exactly one wheel")
    sources = list(Path(sys.argv[1]).resolve().glob("*.tar.gz"))
    if len(sources) != 1:
        raise SystemExit("Expected exactly one source archive")
    with tarfile.open(sources[0]) as archive:
        names = {"/".join(item.name.split("/")[1:]) for item in archive.getmembers()}
        for required in ("scripts/check_public.py", "scripts/check_wheel.py",
                         "tests/report_harness.cjs", "file_review/report.js", "docs/behavior.md",
                         "skills/file-review/SKILL.md"):
            assert required in names, f"Source archive missing {required}"
    wheel = wheels[0]
    with zipfile.ZipFile(wheel) as archive:
        names = set(archive.namelist())
        for asset in ("report.html", "report.css", "report.js"):
            assert f"file_review/{asset}" in names, f"Missing {asset}"
        assert not any(name.startswith("tests/") for name in names)
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        environment = dict(os.environ)
        environment.pop("PYTHONPATH", None)
        environment["PIP_NO_INDEX"] = "1"
        environment["PIP_NO_CACHE_DIR"] = "1"
        rebuilt = root / "rebuilt"
        rebuilt.mkdir()
        subprocess.run([sys.executable, "-m", "pip", "wheel", "--no-deps", "--no-build-isolation",
                        "--wheel-dir", str(rebuilt), str(sources[0])],
                       check=True, cwd=root, env=environment, timeout=120)
        rebuilt_wheels = list(rebuilt.glob("*.whl"))
        assert len(rebuilt_wheels) == 1
        with zipfile.ZipFile(rebuilt_wheels[0]) as archive:
            for asset in ("report.html", "report.css", "report.js"):
                assert f"file_review/{asset}" in archive.namelist(), f"Source-built wheel missing {asset}"
        venv.create(root / "venv", with_pip=True)
        binary = root / "venv/bin"
        for index, artifact in enumerate((wheel, rebuilt_wheels[0])):
            subprocess.run([str(binary / "python"), "-m", "pip", "install", "--force-reinstall",
                            "--no-deps", str(artifact)],
                           check=True, cwd=root, env=environment, timeout=60)
            run_root = root / f"installed-{index}"
            run_root.mkdir()
            check_installation(binary, run_root, environment)
    print("Source archive, both wheels, isolated installation and installed entry points passed.")


if __name__ == "__main__":
    main()
