# Neuropacket — Compliance Checklist (Free v1)

✅ Required fields present:
- version · packet_id (UUIDv4) · ts (RFC3339Z) · subject_id
- source.device_id · source.sensor_profile
- metrics.hr_bpm/hrv_rmssd_ms/eda_uS/skin_temp_c/resp_bpm/spo2_pct (units fixed)
- state.valence/arousal/stress/cognitive_load/resilience/confidence ∈ [0,1]
- quality.artifact_score ∈ [0,1] · quality.calibrated · quality.missing[]
- calibration_id
- privacy.consent_token · privacy.retention (ISO-8601 duration) · privacy.scopes[]
- integrity.hash · integrity.signature · integrity.key_id

✅ Ranges & formats:
- HR 0–300 bpm · HRV RMSSD 0–500 ms · EDA 0–100 µS · Skin temp 20–45 °C
- Resp 0–60 bpm · SpO₂ 0–100% · State 0–1 floats
- `ts` like `2025-11-08T12:34:56.123Z`

✅ Interop rules:
- No extra top-level fields (schema forbids additionalProperties)
- Use exact units above (no unit switching)
- Keep `version` SemVer (`1.0.0`)

**How to check:**  
```bash
python3 tools/npp_validator.py tests/vectors/ok_min.json
python3 tools/smoke_ok.py
```
