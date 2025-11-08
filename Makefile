SHELL := /bin/bash
.PHONY: smoke ok bad

ok:
	python3 tools/npp_validator.py tests/vectors/ok_min.json

bad:
	python3 tools/npp_validator.py tests/vectors/bad_signature.json || true

smoke:
	python3 tools/smoke_ok.py
	python3 tools/smoke_bad.py || true

