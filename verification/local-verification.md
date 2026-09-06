# Local verification

Run from the repository root:

```text
pytest -q
```

The suite covers all three principal semantic statuses, live validator digest calculation, DOI and publisher identity conflicts, source failure, invalid model output, owner-only configuration, duplicate mappings, DOI/URL/path injection, deactivation, state preservation, and append-only repeated checks.

Result on 2026-09-06: `17 passed`.

- Contract SHA-256: `3e143546d6c66ae6102aa2e47f1e7e24a0dc2dfeb6f674f1666a4a84a51c0bc0`
- `active-001.json`: `71ac69e7891c53195d0740aeade7cc086a499566b1f225343c631c8701737050`
- `retracted-002.json`: `42361f9b501742d1a360bfac540915c4c3eebcfc9c3d92bcf50bca9e8b30677f`
- `concern-003.json`: `6aff3b789e7d9573529b8b2559b7f730063d573779b4832ee5aa9bebe65a49be`

On-chain transaction evidence and deployed source parity must be added after a new instance is deployed.
