# b4n1-notary — Go SDK

Authorship integrity and sealing: one Merkle root over a project, a portable
proof file, optional Bitcoin-anchored receipts.

```bash
go get github.com/B4N1-com/b4n1-notary/sdks/go
```

```go
import b4n1notary "github.com/B4N1-com/b4n1-notary/sdks/go"

client := b4n1notary.NewClient()
sealed := client.Stamp("/path/to/project", "team")
fmt.Println(sealed.OK(), sealed.Stdout)
```

| Method | Engine verb |
|---|---|
| `Stamp(path, identity)` | `stamp` |
| `Verify(path, proof)` | `verify` |
| `VerifyOts(path, proof, checkCalendar, header)` | `verify-ots` |
| `History(path)` | `history` |
| `License(action, key, jsonOut)` | `license` |

Resolution order: `B4N1NOTARY_BIN_PATH`, bundled `bin/`, then `PATH`.

## Test

```bash
go test ./...
```

## License

Business Source License 1.1 (BUSL-1.1). See `LICENSE`. Binaries ship with
`EULA.txt`.
