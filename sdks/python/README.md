# b4n1-notary — Python SDK

Authorship integrity and sealing: seal a project into one Merkle root, then
verify it later with a portable proof file.

The wheel bundles the engine for every supported platform — nothing to compile.

```bash
pip install b4n1-notary
```

```python
from b4n1notary import NotaryClient

client = NotaryClient()
client.stamp("/path/to/project", identity="team")
proof = client.history("/path/to/project").stdout
print(proof)
print(client.verify("/path/to/project", "/path/to/project/.b4n1/proofs/<id>.b4n1-proof").ok)
```

| Method | Engine verb |
|---|---|
| `stamp(path, identity=None)` | `stamp` |
| `verify(path, proof)` | `verify` |
| `verify_ots(path, proof, check_calendar=False, header=None)` | `verify-ots` |
| `history(path)` | `history` |
| `license(action=None, key=None, json=False)` | `license` |

Resolution order: `B4N1NOTARY_BIN_PATH`, the bundled binary, then
`b4n1-notary` on `PATH`.

CLI: `python -m b4n1notary stamp --path .`

## Test

```bash
PYTHONPATH=. python3 -m unittest discover -s tests
```

Offline; five checks against the real binary.

## License

Business Source License 1.1 (BUSL-1.1). See `LICENSE`. Binaries ship with
`EULA.txt`.
