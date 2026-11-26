# SDKs

Seven thin wrappers expose the same verbs. None of them reimplements the
engine: each one resolves the binary and runs it, so behaviour cannot drift
between languages.

| Language | Entry point | Test |
|---|---|---|
| Python | `b4n1notary.NotaryClient` | `tests/test_sdk.py` |
| JavaScript | `NotaryClient` in `index.js` | `test/index.test.js` |
| Java | `com.b4n1.notary.NotaryClient` | `NotaryTest` |
| C# | `B4n1.Notary.NotaryClient` | `tests/Program.cs` |
| Ruby | `B4N1Notary::Client` | `test/test_sdk.rb` |
| PHP | `B4N1\Notary\Client` | `test/run.php` |
| Go | `b4n1notary.Client` | `b4n1notary_test.go` |

## What each suite proves

1. `stamp` writes exactly one proof for a fresh tree.
2. `verify` accepts that proof.
3. `verify` rejects the same proof after one byte changes.
4. `history` lists the proof.
5. `license status --json` reports the community entitlement.

All five run offline against the real binary.
