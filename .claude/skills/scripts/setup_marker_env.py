#!/usr/bin/env python3
"""Initialize / resolve a local marker-pdf Python environment for preprocess-pdf.

Creates a machine-local config at .claude/marker-env.local.json so agents do not
re-discover Python interpreters on every PDF conversion.

Default setup order (avoids re-downloading the large marker/torch stack):
  1. Reuse .venv-marker if it already has marker
  2. Bind any discovered system/conda Python that already has marker (GPU > CPU)
  3. Only then create .venv-marker and pip install marker-pdf

Usage (from repo root):
  python .claude/skills/scripts/setup_marker_env.py setup
  python .claude/skills/scripts/setup_marker_env.py setup --use-existing PATH
  python .claude/skills/scripts/setup_marker_env.py setup --force-venv
  python .claude/skills/scripts/setup_marker_env.py setup --cuda cu124
  python .claude/skills/scripts/setup_marker_env.py resolve
  python .claude/skills/scripts/setup_marker_env.py doctor
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import venv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
CONFIG_PATH = REPO_ROOT / ".claude" / "marker-env.local.json"
VENV_DIR = REPO_ROOT / ".venv-marker"
PREFERRED_MAJOR_MINOR = {(3, 11), (3, 12), (3, 13)}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def venv_python(venv_dir: Path) -> Path:
    if platform.system() == "Windows":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=check, text=True, capture_output=True)


def probe_interpreter(python: Path) -> dict[str, Any]:
    """Return capability probe for a Python executable."""
    code = r"""
import json, sys
out = {
    "python": sys.executable,
    "python_version": sys.version.split()[0],
    "marker_ok": False,
    "torch_ok": False,
    "cuda_available": False,
    "cuda_device": None,
    "torch_version": None,
    "marker_version": None,
    "error": None,
}
try:
    import torch
    out["torch_ok"] = True
    out["torch_version"] = getattr(torch, "__version__", None)
    out["cuda_available"] = bool(torch.cuda.is_available())
    if out["cuda_available"]:
        out["cuda_device"] = torch.cuda.get_device_name(0)
except Exception as e:
    out["error"] = f"torch: {e}"
try:
    from marker.converters.pdf import PdfConverter  # noqa: F401
    import importlib.metadata as md
    out["marker_ok"] = True
    try:
        out["marker_version"] = md.version("marker-pdf")
    except Exception:
        try:
            out["marker_version"] = md.version("marker")
        except Exception:
            out["marker_version"] = None
except Exception as e:
    err = f"marker: {e}"
    out["error"] = err if not out["error"] else f"{out['error']}; {err}"
print(json.dumps(out))
"""
    try:
        proc = run([str(python), "-c", code], check=False)
    except OSError as e:
        return {
            "python": str(python),
            "python_version": None,
            "marker_ok": False,
            "torch_ok": False,
            "cuda_available": False,
            "cuda_device": None,
            "torch_version": None,
            "marker_version": None,
            "error": str(e),
        }
    if proc.returncode != 0:
        return {
            "python": str(python),
            "python_version": None,
            "marker_ok": False,
            "torch_ok": False,
            "cuda_available": False,
            "cuda_device": None,
            "torch_version": None,
            "marker_version": None,
            "error": (proc.stderr or proc.stdout or "probe failed").strip(),
        }
    try:
        return json.loads(proc.stdout.strip())
    except json.JSONDecodeError:
        return {
            "python": str(python),
            "python_version": None,
            "marker_ok": False,
            "torch_ok": False,
            "cuda_available": False,
            "cuda_device": None,
            "torch_version": None,
            "marker_version": None,
            "error": f"invalid probe output: {proc.stdout[:200]!r}",
        }


def discover_base_pythons() -> list[Path]:
    found: list[Path] = []
    seen: set[str] = set()

    def add(p: Path | None) -> None:
        if p is None:
            return
        try:
            resolved = p.resolve()
        except OSError:
            return
        if not resolved.is_file():
            return
        key = str(resolved).lower()
        if key in seen:
            return
        seen.add(key)
        found.append(resolved)

    # PATH entries
    which = shutil.which("python")
    if which:
        add(Path(which))
    which3 = shutil.which("python3")
    if which3:
        add(Path(which3))

    if platform.system() == "Windows":
        # `where python`
        where = shutil.which("where")
        if where:
            proc = run([where, "python"], check=False)
            if proc.returncode == 0:
                for line in proc.stdout.splitlines():
                    line = line.strip()
                    if line:
                        add(Path(line))
        local = Path.home() / "AppData" / "Local" / "Programs" / "Python"
        if local.is_dir():
            for py in sorted(local.glob("Python*/python.exe")):
                add(py)
        for conda_root in (
            Path.home() / "Miniconda3",
            Path.home() / "anaconda3",
            Path.home() / "mambaforge",
            Path.home() / "miniforge3",
        ):
            add(conda_root / "python.exe")
            envs = conda_root / "envs"
            if envs.is_dir():
                for py in sorted(envs.glob("*/python.exe")):
                    add(py)
    else:
        for pattern in (
            Path("/usr/bin"),
            Path("/usr/local/bin"),
            Path.home() / ".local" / "bin",
            Path.home() / "miniconda3" / "bin",
            Path.home() / "anaconda3" / "bin",
            Path.home() / "mambaforge" / "bin",
            Path.home() / "miniforge3" / "bin",
        ):
            add(pattern / "python3")
            add(pattern / "python")
        conda_envs = Path.home() / "miniconda3" / "envs"
        if conda_envs.is_dir():
            for py in sorted(conda_envs.glob("*/bin/python")):
                add(py)

    return found


def python_version_tuple(python: Path) -> tuple[int, int] | None:
    proc = run(
        [str(python), "-c", "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')"],
        check=False,
    )
    if proc.returncode != 0:
        return None
    try:
        major_s, minor_s = proc.stdout.strip().split(".", 1)
        return int(major_s), int(minor_s)
    except ValueError:
        return None


def pick_base_python(explicit: Path | None) -> Path:
    if explicit is not None:
        if not explicit.is_file():
            raise SystemExit(f"Base Python not found: {explicit}")
        ver = python_version_tuple(explicit)
        if ver is None:
            raise SystemExit(f"Cannot query version for: {explicit}")
        if ver not in PREFERRED_MAJOR_MINOR:
            print(
                f"WARNING: {explicit} is Python {ver[0]}.{ver[1]}; "
                "marker works best on 3.11–3.13 (3.14+ often fails on Pillow).",
                file=sys.stderr,
            )
        return explicit.resolve()

    candidates = discover_base_pythons()
    preferred: list[Path] = []
    others: list[Path] = []
    for py in candidates:
        ver = python_version_tuple(py)
        if ver in PREFERRED_MAJOR_MINOR:
            preferred.append(py)
        elif ver is not None:
            others.append(py)

    if preferred:
        # Prefer higher minor within 3.11–3.13
        preferred.sort(key=lambda p: python_version_tuple(p) or (0, 0), reverse=True)
        return preferred[0]
    if others:
        others.sort(key=lambda p: python_version_tuple(p) or (0, 0), reverse=True)
        print(
            f"WARNING: No Python 3.11–3.13 found; falling back to {others[0]}",
            file=sys.stderr,
        )
        return others[0]
    raise SystemExit(
        "No suitable Python found. Install Python 3.11–3.13, or pass --python PATH."
    )


def write_config(probe: dict[str, Any], *, source: str, venv_path: str | None) -> dict[str, Any]:
    if not probe.get("marker_ok"):
        raise SystemExit(
            "marker is not importable in the selected interpreter.\n"
            f"Probe error: {probe.get('error')}"
        )
    config = {
        "schema_version": 1,
        "python": probe["python"],
        "python_version": probe.get("python_version"),
        "marker_ok": True,
        "marker_version": probe.get("marker_version"),
        "torch_ok": bool(probe.get("torch_ok")),
        "torch_version": probe.get("torch_version"),
        "cuda_available": bool(probe.get("cuda_available")),
        "cuda_device": probe.get("cuda_device"),
        "venv_path": venv_path,
        "source": source,  # "venv" | "existing"
        "created_at": utc_now()
        if not CONFIG_PATH.is_file()
        else json.loads(CONFIG_PATH.read_text(encoding="utf-8")).get("created_at", utc_now()),
        "validated_at": utc_now(),
        "platform": platform.platform(),
        "hostname": platform.node(),
    }
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return config


def print_config_summary(config: dict[str, Any]) -> None:
    gpu = (
        f"yes ({config.get('cuda_device')})"
        if config.get("cuda_available")
        else "no (CPU)"
    )
    print("Marker environment ready:")
    print(f"  config : {CONFIG_PATH}")
    print(f"  python : {config['python']}")
    print(f"  version: {config.get('python_version')}")
    print(f"  marker : {config.get('marker_version')}")
    print(f"  torch  : {config.get('torch_version')}")
    print(f"  GPU    : {gpu}")
    print(f"  source : {config.get('source')}")


def install_packages(python: Path, *, cuda: str | None) -> None:
    run([str(python), "-m", "pip", "install", "--upgrade", "pip"], check=True)
    if cuda:
        # Install GPU torch first from the official index, then marker.
        index = f"https://download.pytorch.org/whl/{cuda}"
        print(f"Installing torch with CUDA ({cuda}) from {index} ...")
        proc = run(
            [
                str(python),
                "-m",
                "pip",
                "install",
                "torch",
                "torchvision",
                "--index-url",
                index,
            ],
            check=False,
        )
        if proc.returncode != 0:
            print(proc.stdout)
            print(proc.stderr, file=sys.stderr)
            raise SystemExit(
                "Failed to install CUDA torch. Try another --cuda tag "
                "(e.g. cu121, cu124, cu126) matching your driver, or omit --cuda."
            )
    print("Installing marker-pdf ...")
    proc = run([str(python), "-m", "pip", "install", "marker-pdf"], check=False)
    if proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr, file=sys.stderr)
        raise SystemExit("Failed to install marker-pdf")


def probe_rank(probe: dict[str, Any]) -> tuple:
    """Higher is better: CUDA first, then preferred Python versions, then newer."""
    ver = probe.get("python_version") or "0.0.0"
    try:
        nums = [int(x) for x in ver.split(".")[:3]]
    except ValueError:
        nums = [0, 0, 0]
    while len(nums) < 3:
        nums.append(0)
    parts = tuple(nums)
    major_minor = (parts[0], parts[1])
    preferred = 1 if major_minor in PREFERRED_MAJOR_MINOR else 0
    return (
        1 if probe.get("cuda_available") else 0,
        preferred,
        parts,
    )


def find_marker_ready_probes(*, require_cuda: bool = False) -> list[dict[str, Any]]:
    """Probe known interpreters; return those with marker importable."""
    candidates: list[Path] = []
    venv_py = venv_python(VENV_DIR)
    if venv_py.is_file():
        candidates.append(venv_py.resolve())
    candidates.extend(discover_base_pythons())

    seen: set[str] = set()
    ready: list[dict[str, Any]] = []
    for py in candidates:
        key = str(py).lower()
        if key in seen:
            continue
        seen.add(key)
        print(f"Probing: {py}")
        probe = probe_interpreter(py)
        if not probe.get("marker_ok"):
            continue
        if require_cuda and not probe.get("cuda_available"):
            continue
        ready.append(probe)
    ready.sort(key=probe_rank, reverse=True)
    return ready


def create_venv_and_install(*, base: Path, cuda: str | None, recreate: bool) -> dict[str, Any]:
    print(f"Base Python: {base} ({python_version_tuple(base)})")
    print(f"Creating venv: {VENV_DIR}")
    print("NOTE: marker-pdf + torch is large; first install may take several minutes.")
    VENV_DIR.mkdir(parents=True, exist_ok=True)
    venv.EnvBuilder(with_pip=True, clear=bool(recreate)).create(str(VENV_DIR))
    py = venv_python(VENV_DIR)
    if not py.is_file():
        raise SystemExit(f"venv python missing after create: {py}")
    install_packages(py, cuda=cuda)
    probe = probe_interpreter(py)
    return write_config(
        probe,
        source="venv",
        venv_path=str(VENV_DIR.relative_to(REPO_ROOT)).replace("\\", "/"),
    )


def cmd_setup(args: argparse.Namespace) -> int:
    # Explicit bind — never auto-scan
    if args.use_existing:
        python = Path(args.use_existing).expanduser().resolve()
        if not python.is_file():
            raise SystemExit(f"Interpreter not found: {python}")
        print(f"Using existing interpreter: {python}")
        probe = probe_interpreter(python)
        if not probe.get("marker_ok"):
            if args.install_into_existing:
                print("marker missing; installing into existing interpreter ...")
                install_packages(python, cuda=args.cuda)
                probe = probe_interpreter(python)
            else:
                raise SystemExit(
                    "Selected interpreter cannot import marker.\n"
                    f"Error: {probe.get('error')}\n"
                    "Re-run with --install-into-existing, or: setup --force-venv"
                )
        config = write_config(probe, source="existing", venv_path=None)
        print_config_summary(config)
        return 0

    # Force a fresh project venv (skip reuse)
    if args.force_venv or args.recreate:
        base = pick_base_python(Path(args.python).expanduser() if args.python else None)
        config = create_venv_and_install(base=base, cuda=args.cuda, recreate=True)
        print_config_summary(config)
        return 0

    # Default: reuse existing marker install to avoid huge re-download
    require_cuda = bool(args.cuda)
    if require_cuda:
        print(
            f"--cuda {args.cuda} requested: looking for an existing marker env with CUDA ..."
        )
    else:
        print("Looking for an existing Python that already has marker ...")

    ready = find_marker_ready_probes(require_cuda=require_cuda)
    if ready:
        best = ready[0]
        try:
            is_project_venv = Path(best["python"]).resolve() == venv_python(VENV_DIR).resolve()
        except OSError:
            is_project_venv = False
        source = "venv" if is_project_venv else "existing"
        venv_path = (
            str(VENV_DIR.relative_to(REPO_ROOT)).replace("\\", "/")
            if is_project_venv
            else None
        )
        print(f"Reusing existing marker environment (no reinstall): {best['python']}")
        config = write_config(best, source=source, venv_path=venv_path)
        print_config_summary(config)
        return 0

    if require_cuda:
        print(
            "No existing marker+CUDA environment found; "
            "creating .venv-marker and installing GPU torch + marker ..."
        )
    else:
        print(
            "No existing marker environment found; "
            "creating .venv-marker and installing marker-pdf ..."
        )
    base = pick_base_python(Path(args.python).expanduser() if args.python else None)
    config = create_venv_and_install(base=base, cuda=args.cuda, recreate=False)
    print_config_summary(config)
    return 0


def load_config() -> dict[str, Any] | None:
    if not CONFIG_PATH.is_file():
        return None
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"Corrupt config {CONFIG_PATH}: {e}") from e


def ensure_python_exists(config: dict[str, Any]) -> Path:
    python = Path(config.get("python", ""))
    if not python.is_file():
        raise SystemExit(
            f"Configured python missing: {python}\n"
            "Run: python .claude/skills/scripts/setup_marker_env.py setup"
        )
    return python


def refresh_config_from_probe(config: dict[str, Any]) -> dict[str, Any]:
    python = ensure_python_exists(config)
    probe = probe_interpreter(python)
    if not probe.get("marker_ok"):
        raise SystemExit(
            f"Configured python no longer has marker: {python}\n"
            f"Error: {probe.get('error')}\n"
            "Run setup again (or setup --recreate)."
        )
    return write_config(
        probe,
        source=config.get("source", "existing"),
        venv_path=config.get("venv_path"),
    )


def cmd_resolve(args: argparse.Namespace) -> int:
    config = load_config()
    if config is None:
        raise SystemExit(
            "No marker env config found.\n"
            "First-time / new machine:\n"
            "  python .claude/skills/scripts/setup_marker_env.py setup\n"
            "Or bind an existing interpreter:\n"
            "  python .claude/skills/scripts/setup_marker_env.py setup "
            "--use-existing PATH/to/python"
        )
    ensure_python_exists(config)
    if args.verify:
        # Full torch/marker import — slow; use when conversion fails mysteriously
        config = refresh_config_from_probe(config)
    if args.json:
        print(json.dumps(config, indent=2))
    else:
        # Agent-friendly single line: absolute python path
        print(config["python"])
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    config = load_config()
    if config is None:
        raise SystemExit(
            "No config yet. Run setup first:\n"
            "  python .claude/skills/scripts/setup_marker_env.py setup"
        )
    config = refresh_config_from_probe(config)
    print_config_summary(config)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Setup / resolve local marker-pdf environment")
    sub = p.add_subparsers(dest="command", required=True)

    setup = sub.add_parser(
        "setup",
        help="Prefer reuse of existing marker env; only create .venv-marker if none found",
    )
    setup.add_argument(
        "--python",
        help="Base interpreter used when creating .venv-marker (ignored with --use-existing)",
    )
    setup.add_argument(
        "--use-existing",
        metavar="PATH",
        help="Bind this interpreter only (skip auto-discovery)",
    )
    setup.add_argument(
        "--install-into-existing",
        action="store_true",
        help="With --use-existing, pip install marker-pdf if missing",
    )
    setup.add_argument(
        "--force-venv",
        action="store_true",
        help="Skip reuse; create/reinstall .venv-marker even if marker already exists elsewhere",
    )
    setup.add_argument(
        "--cuda",
        metavar="TAG",
        help="Prefer/reuse a CUDA env if present; otherwise install GPU torch into new venv "
        "(tag e.g. cu121 / cu124 / cu126)",
    )
    setup.add_argument(
        "--recreate",
        action="store_true",
        help="Same as --force-venv: recreate .venv-marker and reinstall packages",
    )
    setup.set_defaults(func=cmd_setup)

    resolve = sub.add_parser("resolve", help="Print configured python path (or JSON)")
    resolve.add_argument("--json", action="store_true", help="Print full config JSON")
    resolve.add_argument(
        "--verify",
        action="store_true",
        help="Re-import marker/torch and refresh cache (slow); default only checks path exists",
    )
    resolve.set_defaults(func=cmd_resolve)

    doctor = sub.add_parser("doctor", help="Re-probe configured env and refresh config")
    doctor.set_defaults(func=cmd_doctor)
    return p


def main() -> int:
    # Avoid accidentally running from a different cwd for relative paths in messages
    os.chdir(REPO_ROOT)
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
