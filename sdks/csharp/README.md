# b4n1-notary — .NET SDK

Authorship integrity and sealing: one Merkle root over a project, a portable
proof file, optional Bitcoin-anchored receipts.

```bash
dotnet add package B4n1.Notary
```

```csharp
using B4n1.Notary;

var client = new NotaryClient();
var sealed = client.Stamp("/path/to/project", "team");
Console.WriteLine($"{sealed.Ok} {sealed.Stdout}");
```

| Method | Engine verb |
|---|---|
| `Stamp(path, identity)` | `stamp` |
| `Verify(path, proof)` | `verify` |
| `VerifyOts(path, proof, checkCalendar, header)` | `verify-ots` |
| `History(path)` | `history` |
| `License(action, key, json)` | `license` |

Resolution order: `B4N1NOTARY_BIN_PATH`, `native/` next to the assembly, then
`PATH`.

## Test

```bash
dotnet run --project tests
```

## License

Business Source License 1.1 (BUSL-1.1). See `LICENSE`. Binaries ship with
`EULA.txt`.
