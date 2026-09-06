# Studionet verification

Verified on 2026-09-06.

## Deployment

- Contract: `0x8A7eb525354F80b3dF867BEb5b632f50Fd0aAfef`
- Explorer: https://explorer-studio.genlayer.com/address/0x8A7eb525354F80b3dF867BEb5b632f50Fd0aAfef
- Chain ID: `61999`
- Local source SHA-256: `3e143546d6c66ae6102aa2e47f1e7e24a0dc2dfeb6f674f1666a4a84a51c0bc0`
- Deployed source SHA-256: `3e143546d6c66ae6102aa2e47f1e7e24a0dc2dfeb6f674f1666a4a84a51c0bc0`
- Source parity: `true`

## Publisher registration

- Owner registration: `0xd09b400a38ac7b5786b08818de2aaeb47cbb2349d1437c5b936ca50067714d50`
- Publisher key: `DEMO-PUBLISHER`
- DOI prefix: `10.5555`
- Authority: `raw.githubusercontent.com`
- Immutable record prefix: `/Azaria723/RetractionStatusGate/910d9ac3efa766593b7f824996c10ff7f0ba551b/evidence/`

## Happy path A — active article

- DOI: `10.5555/active-001`
- Request: `0x387f2368c23af95d72bfd70c5d660ef66eb9b357cd78fe35d0268851ad30c87f`
- Assessment: `0x9d27bcdf6e44dfd255bec399ad55238c90f3d0a8fef18004db25538911f006c7`
- Verdict: `ACTIVE`
- Identity: `MATCH`
- Validator digest: `71ac69e7891c53195d0740aeade7cc086a499566b1f225343c631c8701737050`
- Independently calculated raw digest: exact match

## Happy path B — retracted article

- DOI: `10.5555/retracted-002`
- Request: `0xfaee156ef4ba5b6b25a1c8eea6acbcd1f3ed37bcf0c116a357cd497776602f3e`
- Assessment: `0x1250ba13b42c98a2f6d97e198b4294d145aea57cea7d0d1d8d8763f24da9d978`
- Verdict: `RETRACTED`
- Identity: `MATCH`
- Validator digest: `42361f9b501742d1a360bfac540915c4c3eebcfc9c3d92bcf50bca9e8b30677f`
- Independently calculated raw digest: exact match

## Happy path C — expression of concern

- DOI: `10.5555/concern-003`
- Request: `0x4fdd90163f30ce7ca6dfd7edf7b7e6638b64ec28c486cff2976a51c8053ab630`
- Assessment: `0x211aa44e1dd1d11118876c58548186357db41ed8ea9493f3213c9eb05fe34826`
- Verdict: `EXPRESSION_OF_CONCERN`
- Identity: `MATCH`
- Validator digest: `6aff3b789e7d9573529b8b2559b7f730063d573779b4832ee5aa9bebe65a49be`
- Independently calculated raw digest: exact match

## Failure path A — unavailable canonical source

- DOI: `10.5555/missing-004`
- Request: `0xb1bf418e58d9b16b3ae1d6ce86fb3750f7b34cedacc54687bdb3968d33fac7fc`
- Assessment: `0xc5ae2485de0d1cc251ccf07ca2e1d741f18f70c8a0bd3b9e9eea1b259b4e8c0b`
- Verdict: `UNAVAILABLE`
- Reason: `SOURCE_UNAVAILABLE`
- Identity: `NOT_CHECKED`
- Stored digest: empty

The missing source did not become `ACTIVE`; it failed closed.

## Failure path B — rejected inputs preserve state

- Unknown prefix `10.9999/unknown`: `0x9c05f4abc0397ba01f693c3930906dad2b1868ad33493aa44384b8d80ca6ba9c`
- Repeated unknown-prefix regression: `0xc9020028d1d3fb6e7a3dabd74f51736871a2bf0a2861b66dda36889a021b2753`
- Path traversal `10.5555/../../secret`: `0x9531c884631ce50794d47805f36d7953ae3faf82bb158e3fbc25503aabc84f6b`
- Repeated traversal regression: `0x21b83e0aba5d3d088e6d2480f5dc5525a54507e6648af194c96778fcc5987101`

All four transactions finalized, and direct state reads confirmed that none created a check.

## Final state

```json
{"check_count": 4, "publisher_count": 1}
```

The four stored checks are the three semantic happy paths and the explicit unavailable-source failure path. Success was verified using `get_check` records, not inferred from finalized transaction status. Local Direct Mode remains `17 passed`.

This is reproducible Studionet evidence, not an independent security audit or a claim that the demo repository is a real scientific publisher.
