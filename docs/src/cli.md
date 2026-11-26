# Command reference

```
b4n1-notary <command> [options]

stamp      --path <dir> [--identity <name>]
verify     --path <dir> --proof <file>
verify-ots --path <dir> --proof <file> [--check-calendar] [--header <bin>]
history    --path <dir>
license    [status|check|machine|install] [<key>] [--json]
```

## Exit codes

| Code | Meaning |
|---|---|
| 0 | the command succeeded |
| 1 | the operation failed (mismatch, unreadable proof, bad input) |
| 2 | usage error (unknown verb or option) |

## Environment

| Variable | Effect |
|---|---|
| `B4N1_LICENSE_PUBKEY` | overrides the compiled-in licence public key |
| `B4N1NOTARY_BIN_PATH` | SDK only: exact engine path |

## Licence surface

`license status --json` prints the current entitlement as JSON. The product
runs in `community` mode when no key is present; the field is explicit rather
than an empty success.
