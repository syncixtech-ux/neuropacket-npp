# Neuropacket v1-min Field Layout

This document describes the **required** fields, units, and ranges for the Neuropacket v1-min specification.

---

## Required Fields

### Top-Level

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `version` | string | SemVer format version | `"1.0.0"` |
| `packet_id` | string | UUIDv4 unique identifier | `"7e4b9f42-4c48-4e31-8c77-7f7bb4a9c9f5"` |
| `ts` | string | RFC3339 UTC timestamp with `Z` | `"2025-11-08T00:00:00.000Z"` |
| `subject_id` | string | Pseudonymous subject identifier | `"anon:abc"` |
| `source` | object | Device and sensor information | See below |
| `metrics` | object | Physiological measurements | See below |
| `state` | object | Computed affective/cognitive state | See below |
| `quality` | object | Data quality indicators | See below |
| `calibration_id` | string | Calibration reference ID | `"cal-1"` |
| `privacy` | object | Consent and retention metadata | See below |
| `integrity` | object | Cryptographic verification fields | See below |

---

### `source` Object

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `device_id` | string | Unique device identifier | `"edge-1"` |
| `sensor_profile` | string | Sensor type/configuration | `"PPG"`, `"EEG"`, `"MultiModal"` |

---

### `metrics` Object

Physiological measurements with specified units and valid ranges:

| Field | Type | Unit | Range | Description |
|-------|------|------|-------|-------------|
| `hr_bpm` | number | beats/min | 0–300 | Heart rate |
| `hrv_rmssd_ms` | number | milliseconds | 0–500 | HRV (RMSSD) |
| `eda_uS` | number | microsiemens | 0–100 | Electrodermal activity |
| `skin_temp_c` | number | °Celsius | 20–45 | Skin temperature |
| `resp_bpm` | number | breaths/min | 0–60 | Respiration rate |
| `spo2_pct` | number | percent | 0–100 | Blood oxygen saturation |

**Note:** All metrics fields are optional, but when present must be within specified ranges.

---

### `state` Object

Computed affective and cognitive state values (all **required**, range 0.0–1.0):

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `valence` | number | 0.0–1.0 | Emotional valence (negative to positive) |
| `arousal` | number | 0.0–1.0 | Physiological arousal level |
| `stress` | number | 0.0–1.0 | Stress indicator |
| `cognitive_load` | number | 0.0–1.0 | Mental workload |
| `resilience` | number | 0.0–1.0 | Adaptive capacity |
| `confidence` | number | 0.0–1.0 | Model confidence score |

---

### `quality` Object

| Field | Type | Range/Type | Description |
|-------|------|------------|-------------|
| `artifact_score` | number | 0.0–1.0 | Signal quality (0=clean, 1=noisy) |
| `calibrated` | boolean | true/false | Whether device is calibrated |
| `missing` | array | string[] | List of missing metric field names |

---

### `privacy` Object

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `consent_token` | string | JWT or consent identifier | `"jwt:eyJ..."` |
| `retention` | string | ISO 8601 duration | `"P7D"` (7 days) |
| `scopes` | array | Allowed usage scopes | `["local_only"]`, `["research", "analytics"]` |

---

### `integrity` Object

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `hash` | string | Packet hash (algorithm:value) | `"blake3:c0ffee..."` |
| `signature` | string | Cryptographic signature | `"ed25519:abcd..."` |
| `key_id` | string | Signing key identifier | `"k1"` |

**Note:** The free validator checks for presence only; it does not perform cryptographic verification.

---

## Example Minimal Packet

```json
{
  "version": "1.0.0",
  "packet_id": "7e4b9f42-4c48-4e31-8c77-7f7bb4a9c9f5",
  "ts": "2025-11-08T00:00:00Z",
  "subject_id": "anon:abc",
  "source": {
    "device_id": "edge-1",
    "sensor_profile": "PPG"
  },
  "metrics": {
    "hr_bpm": 65,
    "hrv_rmssd_ms": 25,
    "eda_uS": 2.1,
    "skin_temp_c": 32.0,
    "resp_bpm": 10,
    "spo2_pct": 97
  },
  "state": {
    "valence": 0.5,
    "arousal": 0.5,
    "stress": 0.5,
    "cognitive_load": 0.5,
    "resilience": 0.5,
    "confidence": 0.9
  },
  "quality": {
    "artifact_score": 0.1,
    "calibrated": true,
    "missing": []
  },
  "calibration_id": "cal-1",
  "privacy": {
    "consent_token": "jwt:ok",
    "retention": "P7D",
    "scopes": ["local_only"]
  },
  "integrity": {
    "hash": "blake3:c0ffee",
    "signature": "",
    "key_id": ""
  }
}
```

---

## Validation

Use `tools/npp_validator.py` to check packet structure:

```bash
python3 tools/npp_validator.py tests/vectors/ok_min.json
```

The validator checks:
- Required field presence
- UUIDv4 format for `packet_id`
- RFC3339 timestamp format
- Metric ranges
- State value ranges (0.0–1.0)
- Privacy field presence
- Integrity field presence

---

*For more information, see schema/neuropacket.schema.json or visit https://sync-ix.com*

    "metadata": {
      "subject_id": "P001",
      "task": "resting_state",
      "electrode_locations": ["Fp1", "Fp2", "C3", "C4", "P3", "P4", "O1", "O2"]
    }
  }
}
```

---

## Units and Ranges

### Common Units

| Measurement | Recommended Unit | Range |
|-------------|------------------|-------|
| Voltage (EEG/ECoG) | microvolts (µV) | -100 to +100 |
| Voltage (single-unit) | millivolts (mV) | -70 to +30 |
| Sample rate | Hertz (Hz) | 1 to 30,000+ |
| Time | seconds (s) | 0+ |
| Frequency | Hertz (Hz) | 0+ |
| Power | decibels (dB) or µV² | varies |

### Timestamps

- **Absolute:** Use ISO 8601 (top-level `timestamp` field)
- **Relative:** Use seconds from session start (in `data.events[].time` or similar)

---

## Best Practices

1. **Document your schema** – Include a `README.md` or schema file in your repository
2. **Use consistent units** – Specify units in the `data` object or documentation
3. **Validate locally** – Use `tools/npp_validator.py` to check structure before transmission
4. **Sign packets** – Always include valid `signature` and `public_key` fields
5. **Keep metadata separate** – Put experiment/subject info in `data.metadata`, not top-level

---

## Examples

See `tests/vectors/ok_min.json` for a minimal valid packet.

For more examples, check the SYNC-IX documentation at [https://syncix.tech](https://syncix.tech).

---

*This guide is a living document. Feedback and contributions are welcome.*
