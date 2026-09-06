# RetractionStatusGate

RetractionStatusGate is a narrow GenLayer Intelligent Contract that records the current official publication status of one DOI. It has no frontend, token, escrow, or payout system.

Possible verdicts:

- `ACTIVE`
- `RETRACTED`
- `EXPRESSION_OF_CONCERN`
- `IDENTITY_CONFLICT`
- `UNAVAILABLE`

## Why GenLayer

Publisher records mix structured identity fields with natural-language notices. A correction is not a retraction, and an expression of concern is not a final withdrawal. Validators must retrieve the publisher-controlled record, bind it to the requested DOI, interpret its notice, and reach consensus.

## Verification model

The owner registers a unique DOI prefix with an approved HTTPS authority and record-path prefix. A requester supplies only a normalized DOI; it cannot supply a URL, JSON document, digest, publisher, or verdict.

For every check, validators:

1. derive the publisher from the DOI prefix;
2. build the canonical HTTPS record URL from owner-controlled configuration;
3. fetch the record themselves;
4. calculate SHA-256 over the response bytes;
5. require exact DOI and publisher identity markers;
6. classify the notice;
7. reach strict equality over the digest, identity, reason code, and verdict;
8. store the agreed digest and verdict as a new historical check.

There is deliberately no submitted digest. A new request creates a new record rather than overwriting an older observation.

## Methods

Writes:

- `register_publisher(publisher_key, doi_prefix, authority_host, record_path_prefix)` — owner only.
- `deactivate_publisher(publisher_id)` — owner only.
- `request_status_check(doi)` — creates a pending observation.
- `assess_status(check_id)` — performs validator retrieval and assessment.

Views:

- `get_counts()`
- `get_publisher(publisher_id)`
- `get_check(check_id)`

## Local test

```bash
python -m pip install -r requirements.txt
pytest -q
```

See [deployment instructions](docs/DEPLOYMENT.md), [threat model](docs/THREAT_MODEL.md), and [local verification](verification/local-verification.md).

The included raw-GitHub records are deterministic demo fixtures. A real publisher registration must use that publisher's official authority or authenticated API; a repository controlled by the submitter is not authoritative production evidence.

