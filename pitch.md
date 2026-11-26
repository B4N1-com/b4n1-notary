# b4n1-notary — authorship you can prove

## What it is

A command-line engine and a seven-language SDK that seal a project into a
single **Merkle root** and record it in a portable proof file. An optional
OpenTimestamps receipt anchors the same root in Bitcoin, so the seal can be
checked later by anyone, without trusting us and without a network call.

## Who it is for

- Teams that hand code or data to a client and must prove **what** was
  delivered and **when**.
- Auditors and compliance workflows that need evidence of a snapshot.
- Developers who want a one-line integrity check in CI.

## What pain it removes

Version control answers "what changed", not "what exactly did I deliver on
the 12th". A Git tag can be moved, an archive can be re-zipped. A Merkle root
plus a timestamp is a single value that either matches the tree or does not.

## Three value bullets

1. **One root, every file.** `stamp` walks the project and produces the Merkle
   root; `verify` recomputes it and answers in one line.
2. **Portable proof.** The `.b4n1-proof` file is JSON: content hash, file
   count, timestamp and the optional OTS receipt.
3. **Seven languages, one engine.** Python, JavaScript, Java, C#, Ruby, PHP
   and Go wrappers — the binary decides, so a fix lands everywhere at once.

## One demonstrable metric

On a 1 000-file tree the seal is computed in a single pass and the proof file
stays a few hundred bytes; verification re-hashes the tree and prints
`✅ VERIFIED` or the first mismatch.

## Call to action

```bash
b4n1-notary stamp --path . --identity "team"
b4n1-notary verify --path . --proof .b4n1/proofs/<id>.b4n1-proof
```

The full manual ships with the SDK (`docs/`) and works offline.
