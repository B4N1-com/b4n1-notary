"""b4n1-notary CLI entry point: python -m b4n1notary <verb> [args...]."""

import sys

from .binary import get_b4n1notary_binary


def main():
    binary = get_b4n1notary_binary()
    if not binary:
        print(
            "b4n1-notary binary not found. Set B4N1NOTARY_BIN_PATH or install "
            "the binary.",
            file=sys.stderr,
        )
        sys.exit(1)

    import subprocess

    result = subprocess.run([binary] + sys.argv[1:])
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
