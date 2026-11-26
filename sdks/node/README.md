# b4n1-notary — JavaScript SDK

Authorship integrity and sealing: one Merkle root over a project, a portable
proof file, optional Bitcoin-anchored receipts.

The package bundles precompiled engines per platform — no compiler needed.

```bash
npm install b4n1-notary
```

```js
const { NotaryClient } = require("b4n1-notary");

const client = new NotaryClient();
const sealed = client.stamp("/path/to/project", "team");
console.log(sealed.ok, sealed.stdout);
console.log(client.history("/path/to/project").stdout);
```

| Method | Engine verb |
|---|---|
| `stamp(path, identity)` | `stamp` |
| `verify(path, proof)` | `verify` |
| `verifyOts(path, proof, { checkCalendar, header })` | `verify-ots` |
| `history(path)` | `history` |
| `license(action, key, json)` | `license` |

Resolution order: `B4N1NOTARY_BIN_PATH`, bundled `bin/`, then `PATH`.

## Test

```bash
node test/index.test.js
```

## License

Business Source License 1.1 (BUSL-1.1). See `LICENSE`. Binaries ship with
`EULA.txt`.
