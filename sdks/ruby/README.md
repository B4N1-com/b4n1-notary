# b4n1-notary — Ruby SDK

Authorship integrity and sealing: one Merkle root over a project, a portable
proof file, optional Bitcoin-anchored receipts.

```bash
gem install b4n1-notary
```

```ruby
require "b4n1notary"

client = B4N1Notary::Client.new
sealed = client.stamp("/path/to/project", identity: "team")
puts sealed.ok?
puts client.history("/path/to/project").stdout
```

| Method | Engine verb |
|---|---|
| `stamp(path, identity:)` | `stamp` |
| `verify(path, proof)` | `verify` |
| `verify_ots(path, proof, check_calendar:, header:)` | `verify-ots` |
| `history(path)` | `history` |
| `license(action, key:, json:)` | `license` |

Resolution order: `B4N1NOTARY_BIN_PATH`, bundled `bin/`, then `PATH`.

## Test

```bash
ruby test/test_sdk.rb
```

## License

Business Source License 1.1 (BUSL-1.1). See `LICENSE`. Binaries ship with
`EULA.txt`.
