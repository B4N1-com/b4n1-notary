# b4n1-notary — Java SDK

Authorship integrity and sealing: one Merkle root over a project, a portable
proof file, optional Bitcoin-anchored receipts.

```xml
<dependency>
  <groupId>com.b4n1</groupId>
  <artifactId>b4n1-notary</artifactId>
  <version>0.2.1</version>
</dependency>
```

```java
import com.b4n1.notary.NotaryClient;

NotaryClient client = new NotaryClient();
NotaryClient.Result sealed = client.stamp("/path/to/project", "team");
System.out.println(sealed.ok() + " " + sealed.stdout);
```

| Method | Engine verb |
|---|---|
| `stamp(path, identity)` | `stamp` |
| `verify(path, proof)` | `verify` |
| `verifyOts(path, proof, checkCalendar, header)` | `verify-ots` |
| `history(path)` | `history` |
| `license(action, key, json)` | `license` |

Resolution order: `B4N1NOTARY_BIN_PATH`, `native/` next to the jar, then
`PATH`.

## Test

```bash
javac -d out/main $(find src/main/java -name '*.java')
javac -d out/test -cp out/main $(find src/test/java -name '*.java')
java -cp out/main:out/test com.b4n1.notary.NotaryTest
```

## License

Business Source License 1.1 (BUSL-1.1). See `LICENSE`. Binaries ship with
`EULA.txt`.
