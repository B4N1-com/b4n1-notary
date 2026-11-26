# b4n1-notary — PHP SDK

Authorship integrity and sealing: one Merkle root over a project, a portable
proof file, optional Bitcoin-anchored receipts.

```bash
composer require b4n1/b4n1-notary
```

```php
use B4N1\Notary\Client;

$client = new Client();
$sealed = $client->stamp('/path/to/project', 'team');
echo $sealed['ok'] ? "sealed\n" : $sealed['stderr'];
echo $client->history('/path/to/project')['stdout'];
```

| Method | Engine verb |
|---|---|
| `stamp(path, identity)` | `stamp` |
| `verify(path, proof)` | `verify` |
| `verifyOts(path, proof, checkCalendar, header)` | `verify-ots` |
| `history(path)` | `history` |
| `license(action, key, json)` | `license` |

Resolution order: `B4N1NOTARY_BIN_PATH`, bundled `bin/`, then `PATH`.

## Test

```bash
php test/run.php
```

## License

Business Source License 1.1 (BUSL-1.1). See `LICENSE`. Binaries ship with
`EULA.txt`.
