# OpenTimestamps anchoring

The Merkle root can be submitted to public OpenTimestamps calendars, which
aggregate it into a Bitcoin transaction. That receipt is what makes the seal
independent of us: verifying it does not require this tool's author.

```bash
# ask the calendars and inspect the receipt
b4n1-notary verify-ots --path . --proof <proof> --check-calendar

# verify against an externally trusted Bitcoin block header (airtight)
b4n1-notary verify-ots --path . --proof <proof> --header header.bin
```

Exit codes are typed: the command distinguishes a receipt that is present but
still pending from one that is anchored, and from a proof with no receipt at
all. A network failure during `stamp` never blocks the local seal — it is
reported as `HashReady` with no receipt.
