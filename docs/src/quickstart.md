# Quick start

`b4n1-notary` seals a project: it hashes every file into one Merkle root and
writes a proof that can be checked later.

```bash
b4n1-notary stamp --path . --identity "team"
b4n1-notary history --path .
b4n1-notary verify --path . --proof .b4n1/proofs/<id>.b4n1-proof
```

- `stamp` prints the file count, the Merkle root and the proof path.
- `history` lists the proofs already sealed for the project.
- `verify` recomputes the root and compares it with the proof.

A second `stamp` on an unchanged tree is a no-op: the engine reports
`Skip: Project has not changed` instead of writing a duplicate proof.
