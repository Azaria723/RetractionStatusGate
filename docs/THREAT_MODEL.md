# Threat model

## Protected properties

- A requester cannot choose the publisher, evidence URL, response body, or digest.
- DOI prefix determines one owner-approved authority mapping.
- Every validator fetches the record and hashes the response bytes.
- Strict equality covers digest, identity, reason code, and verdict.
- DOI and publisher markers must match before semantic interpretation.
- Source, parsing, model, or enum failure becomes `UNAVAILABLE`.
- Each check is append-only history; a later observation does not overwrite an earlier one.

## Addressed attacks

- Contributor-authored JSON supplied as decisive evidence.
- DOI path traversal, extra slashes, schemes, uppercase aliases, query strings, and URL injection.
- Unregistered DOI prefixes and duplicate authority mappings.
- A valid record copied from a different DOI or publisher.
- Prompt injection text embedded in publisher metadata.
- Treating corrections or criticism as retraction.
- Treating an expression of concern as a completed retraction.
- Unknown model output and unavailable sources.
- Non-owner publisher registration or deactivation.

## Explicit limitations

- The owner-curated publisher registry is a trust boundary.
- Transport redirect destination is not exposed by the current GenLayer response API; use direct canonical authority endpoints and verify redirect behavior operationally.
- Live sources can change between separate checks. This is intentional: each consensus digest records the bytes observed for that check.
- A publisher-controlled record can itself be incorrect or compromised.
- The demo raw-GitHub fixture is reproducible test evidence, not an authoritative scientific publisher.
- The contract does not provide medical, legal, or research-integrity advice.

