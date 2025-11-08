# Neuropacket & NPP (Free Minimal)

This is the simple, free edition of **Neuropacket** (the data object) and the **Neuropacket Protocol (NPP)** (rules).
It ships with a JSON Schema, a tiny validator, and *smoke* scripts + example packets.

**Website:** https://sync-ix.com  
**Contact:** syncix.tech@gmail.com

## What's here
- `schema/neuropacket.schema.json` — JSON Schema (free layout)
- `proto/neuropacket.proto` — optional Protobuf schema
- `tools/npp_validator.py` — dependency‑free validator (schema/units/consent/integrity presence)
- `tools/smoke_ok.py` — create a valid packet and validate it
- `tools/smoke_bad.py` — create an invalid packet and see errors
- `tests/vectors/*.json` — example packets

## Quick start
```bash
python3 tools/npp_validator.py tests/vectors/ok_min.json
python3 tools/npp_validator.py tests/vectors/bad_signature.json
```

### Smoke (generate + validate)
```bash
python3 tools/smoke_ok.py   # prints PASS
python3 tools/smoke_bad.py  # prints FAIL + reasons
```

## License
Starter code in this folder is under **Apache-2.0**.
Trademarks: "Neuropacket", "Neuropacket Protocol", "Neuropacket‑Compliant" belong to SYNC‑IX Technologies.
