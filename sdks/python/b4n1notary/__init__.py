"""b4n1-notary SDK — authorship integrity and sealing.

Thin Python wrapper around the b4n1-notary binary. The wheel bundles the engine
for the supported platforms and resolves the matching one at import time.

Quick start:

    from b4n1notary import NotaryClient

    client = NotaryClient()
    sealed = client.stamp("/path/to/project", identity="team")
    print(sealed.stdout)
    proofs = client.history("/path/to/project")

CLI usage:

    python -m b4n1notary stamp --path .
"""

from .binary import get_b4n1notary_binary, run

SDK_VERSION = "0.2.1"

__version__ = SDK_VERSION
__author__ = "Bani Montoya"
__email__ = "banimontoya@gmail.com"

__all__ = [
    "get_b4n1notary_binary",
    "run",
    "NotaryClient",
    "NotaryResult",
]


class NotaryResult:
    """Outcome of one notary command: exit code plus the two streams."""

    def __init__(self, exit_code: int, stdout: str, stderr: str):
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr

    @property
    def ok(self) -> bool:
        return self.exit_code == 0

    def __repr__(self) -> str:
        return f"NotaryResult(exit_code={self.exit_code})"


class NotaryClient:
    """High-level client wrapping the b4n1-notary binary."""

    def __init__(self, binary_path: str = None):
        self._binary = binary_path or get_b4n1notary_binary()
        if not self._binary:
            raise RuntimeError(
                "b4n1-notary binary not found. Set B4N1NOTARY_BIN_PATH or "
                "install the binary."
            )

    def _call(self, *args, timeout=120) -> NotaryResult:
        import subprocess

        result = subprocess.run(
            [self._binary] + list(args),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return NotaryResult(result.returncode, result.stdout, result.stderr)

    def stamp(self, path: str = ".", identity: str = None) -> NotaryResult:
        """Seal a project: Merkle root + a .b4n1-proof file under .b4n1/."""
        args = ["stamp", "--path", path]
        if identity:
            args += ["--identity", identity]
        return self._call(*args)

    def verify(self, path: str, proof: str) -> NotaryResult:
        """Check a project against an existing .b4n1-proof file."""
        return self._call("verify", "--path", path, "--proof", proof)

    def verify_ots(
        self,
        path: str,
        proof: str,
        check_calendar: bool = False,
        header: str = None,
    ) -> NotaryResult:
        """Verify the OpenTimestamps receipt attached to a proof."""
        args = ["verify-ots", "--path", path, "--proof", proof]
        if check_calendar:
            args.append("--check-calendar")
        if header:
            args += ["--header", header]
        return self._call(*args)

    def history(self, path: str = ".") -> NotaryResult:
        """List the proofs already sealed for a project."""
        return self._call("history", "--path", path)

    def license(self, action: str = None, key: str = None, json: bool = False) -> NotaryResult:
        """Licence surface: status (default), check, machine or install."""
        args = ["license"]
        if action:
            args.append(action)
        if key:
            args.append(key)
        if json:
            args.append("--json")
        return self._call(*args)
