"""Make a notebook run the same way in Colab, on the school JupyterHub, and locally.

Every notebook starts with the same short cell::

    import pathlib, subprocess, sys
    REPO = "https://github.com/arubrno/atrium-school-ml-lessons.git"
    HUB_REPO = pathlib.Path.home() / "_atrium-school-ml-lessons"
    here = pathlib.Path.cwd()
    root = next((p for p in [here, *here.parents, HUB_REPO]
                 if (p / "atrium_bootstrap.py").exists()), None)
    if root is None:                                   # Colab, or a bare kernel
        root = pathlib.Path("atrium-school-ml-lessons").resolve()
        if not (root / "atrium_bootstrap.py").exists():
            subprocess.run(["git", "clone", "--depth", "1", REPO, str(root)], check=True)
    sys.path.insert(0, str(root))
    from atrium_bootstrap import setup
    setup("torch", "transformers");

That cell is deliberately self-contained: on Colab nothing of this repository
exists yet when it runs, so it cannot import anything from here until it has
cloned. Everything after the clone lives in this module, so a fix reaches every
notebook at once.

On the school JupyterHub every participant's server mounts the same
``/home/jovyan``. The organisers keep one clone in ``~/_atrium-school-ml-lessons``
and participants copy notebooks out of it into ``~/<their name>/``; ``HUB_REPO``
is how a copied notebook finds its way back. Packages (``~/.local``), model
weights (``~/.cache/huggingface``) and datasets (``~/_atrium-data``) are shared
the same way, so whatever the organisers' first run fetched, everyone has.

``setup()`` does three things:

* installs only the packages that are actually missing, with the flags that
  suit the platform (``--user`` on the hub, the CPU wheel index for PyTorch off
  Colab);
* points the model cache and the dataset cache somewhere that survives as long
  as the platform allows;
* puts the repository root on ``sys.path`` so ``from atrium_data import
  get_dataset`` works from any day's folder.
"""

from __future__ import annotations

import contextlib
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

__all__ = ["setup", "ensure", "where_am_i", "REPO_ROOT", "HUB_DATA"]

_HERE = Path(__file__).resolve().parent
REPO_ROOT = _HERE

#: Where datasets live on the school JupyterHub. The home directory is shared by
#: every participant's server, so one copy serves the whole room.
HUB_DATA = Path.home() / "_atrium-data"

#: pip name -> import name, only where the two differ.
_MODULE = {
    "pillow": "PIL",
    "pyyaml": "yaml",
    "opencv-python": "cv2",
    "opencv-python-headless": "cv2",
    "scikit-learn": "sklearn",
    "scikit-image": "skimage",
    "huggingface-hub": "huggingface_hub",
    "pillow-simd": "PIL",
}

#: Version limits applied when a package has to be installed. Anything already
#: installed is left alone.
_PINS = {
    # transformers 5 switches PyTorch off entirely below torch 2.5, and the
    # school JupyterHub image ships torch 2.4.1. The 4.x line needs only 2.1.
    "transformers": "transformers>=4.40,<5",
}

#: Installed from the CPU index unless we are on Colab, which ships its own build.
_TORCH_FAMILY = {"torch", "torchvision", "torchaudio"}

_CPU_INDEX = [
    "--index-url", "https://download.pytorch.org/whl/cpu",
    "--extra-index-url", "https://pypi.org/simple",
]

#: Needed by essentially every notebook, so `setup()` always ensures them.
_CORE = ("pillow", "matplotlib", "requests", "pyyaml")


def where_am_i() -> str:
    """Return ``"colab"``, ``"hub"`` or ``"local"``."""
    if "google.colab" in sys.modules:
        return "colab"
    try:
        if importlib.util.find_spec("google.colab") is not None:
            return "colab"
    except (ImportError, ValueError):
        pass
    if os.environ.get("JUPYTERHUB_USER") or Path("/home/jovyan").is_dir():
        return "hub"
    return "local"


def _in_venv() -> bool:
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix)


def _pip(packages: list[str], *, user: bool, extra_args: list[str] | None = None) -> None:
    cmd = [sys.executable, "-m", "pip", "install", "-q"]
    if user:
        # ~/.local/bin is not on the hub's PATH. Notebooks only import the
        # packages, so the command-line scripts some of them ship don't matter.
        cmd += ["--user", "--no-warn-script-location"]
    cmd += (extra_args or []) + packages
    subprocess.run(cmd, check=True)


def _missing(packages) -> list[str]:
    out = []
    for pkg in packages:
        module = _MODULE.get(pkg, pkg.replace("-", "_"))
        try:
            found = importlib.util.find_spec(module) is not None
        except (ImportError, ValueError):
            found = False
        if not found and pkg not in out:
            out.append(pkg)
    return out


def _add_user_site() -> None:
    """Make ``pip install --user`` packages importable without a kernel restart.

    Python only puts ``~/.local`` on the path if it existed when the interpreter
    started, and on the hub another participant's server may have installed into
    it since.
    """
    import site
    user_site = site.getusersitepackages()
    for path in ([user_site] if isinstance(user_site, str) else list(user_site)):
        if path not in sys.path:
            sys.path.append(path)
    importlib.invalidate_caches()


@contextlib.contextmanager
def _install_lock(quiet: bool):
    """Take turns installing into the ``~/.local`` that every hub server shares.

    Two pips writing the same site-packages at once can leave it half-installed
    for everyone. ``lockf`` rather than ``flock`` because it also holds across
    machines on an NFS-mounted home.
    """
    import fcntl
    path = Path.home() / ".cache" / "atrium-install.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as fh:
        try:
            fcntl.lockf(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            if not quiet:
                print("someone else is installing packages on the shared home; waiting ...")
            fcntl.lockf(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.lockf(fh, fcntl.LOCK_UN)


def ensure(*packages: str, quiet: bool = False) -> list[str]:
    """Install whichever of ``packages`` are not importable. Returns what it installed."""
    env = where_am_i()
    # --user is what makes an install survive a hub respawn; it is also invalid
    # inside a virtual environment, where a plain install is already persistent.
    user = env == "hub" and not _in_venv()
    if user:
        _add_user_site()

    if not _missing(packages):
        if not quiet:
            print("packages: all present")
        return []

    if env != "hub":
        return _install(_missing(packages), env=env, user=user, quiet=quiet)
    with _install_lock(quiet):
        # Whoever held the lock before us may have just installed all of it.
        _add_user_site()
        return _install(_missing(packages), env=env, user=user, quiet=quiet)


def _install(missing: list[str], *, env: str, user: bool, quiet: bool) -> list[str]:
    if not missing:
        if not quiet:
            print("packages: all present")
        return []

    torch_pkgs = [_PINS.get(p, p) for p in missing if p in _TORCH_FAMILY]
    other = [_PINS.get(p, p) for p in missing if p not in _TORCH_FAMILY]

    if torch_pkgs:
        # Off Colab, the default PyPI wheel drags in ~2.5 GB of CUDA runtime even
        # on a machine with no NVIDIA card. The CPU index is the whole difference
        # between a one-minute install and a coffee break.
        if not quiet:
            print(f"installing {', '.join(torch_pkgs)} (CPU build) ...")
        _pip(torch_pkgs, user=user, extra_args=None if env == "colab" else _CPU_INDEX)
    if other:
        if not quiet:
            print(f"installing {', '.join(other)} ...")
        _pip(other, user=user)

    # A --user install lands in a directory this interpreter may not have on its
    # path yet.
    if user:
        _add_user_site()
    importlib.invalidate_caches()

    return missing


def _mount_drive() -> Path | None:
    try:
        from google.colab import drive  # type: ignore
    except ImportError:
        return None
    drive.mount("/content/drive")
    return Path("/content/drive/MyDrive/atrium-school")


def _cache_root(env: str, drive: bool) -> Path:
    if env == "colab":
        if drive:
            mounted = _mount_drive()
            if mounted is not None:
                return mounted
        # Colab's disk is wiped when the runtime is recycled; caching here still
        # saves every re-run within one session.
        return Path("/content/atrium-cache")
    # Hub and local machines both have a home directory that persists.
    return Path.home() / ".cache"


#: Environment variables that setup() itself chose, so a second call may change
#: them (to switch Colab over to Drive) without trampling ones the user set.
_OURS: dict[str, str] = {}


def _set_env(name: str, value: str) -> bool:
    """Set ``name`` unless the user set it themselves. Returns whether it changed."""
    current = os.environ.get(name)
    if current is not None and _OURS.get(name) != current:
        return False
    os.environ[name] = _OURS[name] = value
    return current is not None and current != value


def setup(*packages: str, drive: bool = False, quiet: bool = False) -> Path:
    """Prepare the current runtime and return the repository root.

    ``packages`` are the extras this notebook needs on top of the core four
    (pillow, matplotlib, requests, pyyaml) — e.g. ``setup("torch", "transformers")``.

    ``drive=True`` mounts Google Drive on Colab so model weights and datasets are
    downloaded once instead of once per session. It prompts for authorisation, so
    it is off by default.
    """
    env = where_am_i()

    root = _find_root() or REPO_ROOT
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    cache = _cache_root(env, drive)
    data = HUB_DATA if env == "hub" else cache / "atrium-school"
    hf_moved = _set_env("HF_HOME", str(cache / "huggingface"))
    _set_env("ATRIUM_CACHE", str(data))
    os.environ.setdefault("ATRIUM_ENV", env)
    (cache / "huggingface").mkdir(parents=True, exist_ok=True)

    ensure(*_CORE, *packages, quiet=quiet)

    if not quiet:
        where = {"colab": "Google Colab", "hub": "JupyterHub", "local": "this machine"}[env]
        print(f"\nrunning on : {where}")
        print(f"repository : {root}")
        print(f"models in  : {os.environ['HF_HOME']}")
        print(f"datasets in: {os.environ['ATRIUM_CACHE']}")
        if env == "colab" and not drive:
            print("note       : Colab forgets these when the runtime is recycled.\n"
                  "             setup(..., drive=True) keeps them in your Google Drive.")
    if hf_moved and "huggingface_hub" in sys.modules:
        # huggingface_hub reads HF_HOME once, when it is first imported.
        print("\nThe model cache moved, but a model was already loaded from the old one.\n"
              "Restart the kernel (Colab: Runtime → Restart session) and run again.")
    return root


def _find_root() -> Path | None:
    """The repository root, whether we were started from it or cloned into it."""
    for candidate in [Path.cwd(), *Path.cwd().parents, REPO_ROOT]:
        if (candidate / "atrium_data.py").exists():
            return candidate
    return None
