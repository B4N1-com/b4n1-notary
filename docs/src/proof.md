# The proof file

`stamp` writes `.b4n1/proofs/<timestamp>.b4n1-proof`, a JSON document with:

| Field | Meaning |
|---|---|
| `project_hash` | Merkle root over the sealed tree |
| `file_count` | Number of files in the tree |
| `timestamp_utc` | When the seal was produced |
| `identity` | Optional author identity, exactly as given |
| `status` | `HashReady`, `CalendarPending` or `OtsComplete` |
| `receipt` | Base64 OpenTimestamps receipt, when one was obtained |

The status is the honest part: `HashReady` means the root exists locally and
no calendar was reached. It never claims an anchor that was not obtained.
