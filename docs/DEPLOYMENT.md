# Deployment procedure

## Before deployment

1. Run `pytest -q` and retain the complete result.
2. The demo evidence files are published at immutable commit `910d9ac3efa766593b7f824996c10ff7f0ba551b`.
3. Re-run tests and verify every raw record returns HTTP 200.
4. Calculate each fixture digest independently for evidence documentation.

## Deploy

Deploy `contracts/RetractionStatusGate.py` as a new GenLayer Studio instance. Record the address and compare the deployed source SHA-256 with the local file.

## Register demo publisher

Using the deployer wallet, call:

```text
publisher_key: DEMO-PUBLISHER
doi_prefix: 10.5555
authority_host: raw.githubusercontent.com
record_path_prefix: /Azaria723/RetractionStatusGate/910d9ac3efa766593b7f824996c10ff7f0ba551b/evidence/
```

Expected publisher ID: `0`.

This registration is only a reproducible fixture demonstration. It must not be represented as an actual publisher authority.

## On-chain lifecycle

Run and retain these cases:

1. `10.5555/active-001` → `ACTIVE`
2. `10.5555/retracted-002` → `RETRACTED`
3. `10.5555/concern-003` → `EXPRESSION_OF_CONCERN`

For every case, retain both the request and assessment transactions, then call `get_check`. Confirm:

- `status` is `1`;
- the stored verdict is expected;
- `identity` in diagnostics is `MATCH`;
- `record_sha256` equals an independently calculated digest of the served raw bytes.

Do not claim success from transaction finalization alone. A finalized method can return a fail-closed error value without producing the intended state.
