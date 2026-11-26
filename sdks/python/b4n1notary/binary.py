"""Binary resolution for the b4n1-notary SDK.

The wheel bundles the engine for every supported platform and resolves the
matching one at import time. Overrides:

    B4N1NOTARY_BIN_PATH=/path/to/b4n1-notary   exact binary, wins over the bundle
    B4N1NOTARY_BINARY=/path/to/b4n1-notary     same, kept for older callers
"""

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Optional

_PLATFORM_BINARIES = {
    ("linux", "x86_64"): "b4n1notary-linux-amd64",
    ("linux", "aarch64"): "b4n1notary-linux-arm64",
    ("linux", "i686"): "b4n1notary-linux-ia32",
    ("darwin", "x86_64"): "b4n1notary-macos-x64",
    ("darwin", "arm64"): "b4n1notary-macos-arm64",
    ("win32", "AMD64"): "b4n1notary-windows-amd64.exe",
    ("win32", "x86"): "b4n1notary-windows-ia32.exe",
}


def _platform_binary_name() -> Optional[str]:
    return _PLATFORM_BINARIES.get((sys.platform, platform.machine()))


def get_b4n1notary_binary() -> Optional[str]:
    """Resolve the b4n1-notary binary path.

    Order: exact env override, bundled binary for this platform, legacy env
    override, common install locations, then PATH.
    """
    exact = os.environ.get("B4N1NOTARY_BIN_PATH")
    if exact and os.path.isfile(exact) and os.access(exact, os.X_OK):
        return exact

    bin_name = _platform_binary_name()
    if bin_name:
        bundled = Path(__file__).parent / "bin" / bin_name
        if bundled.exists() and os.access(bundled, os.X_OK):
            return str(bundled)

    legacy = os.getenv("B4N1NOTARY_BINARY")
    if legacy and os.path.isfile(legacy) and os.access(legacy, os.X_OK):
        return legacy

    possible = [
        str(Path.home() / ".local/bin/b4n1-notary"),
        "/usr/local/bin/b4n1-notary",
        "/usr/bin/b4n1-notary",
    ]
    for d in os.environ.get("PATH", "").split(":"):
        if d:
            possible.append(os.path.join(d, "b4n1-notary"))

    for loc in possible:
        if os.path.isfile(loc) and os.access(loc, os.X_OK):
            return loc
    return None


def run(*args, **kwargs):
    """Run the b4n1-notary binary. Raises RuntimeError when unresolvable."""
    binary = get_b4n1notary_binary()
    if not binary:
        raise RuntimeError(
            "b4n1-notary binary not found. Set B4N1NOTARY_BIN_PATH or install "
            "the binary (see the manual in `b4n1-notary docs`)."
        )
    kwargs.setdefault("capture_output", True)
    kwargs.setdefault("text", True)
    return subprocess.run([binary] + list(args), **kwargs)
