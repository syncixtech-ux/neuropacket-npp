#!/usr/bin/env python3
"""
Generate N synthetic Neuropackets in tests/vectors/sample_*.json
Usage: python3 examples/python/generate_packets.py 20
"""
import json, os, sys, uuid, random
from datetime import datetime, timezone
import subprocess

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
out_dir = "tests/vectors"
os.makedirs(out_dir, exist_ok=True)

def ts_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

for i in range(N):
    pkt = {
      "version":"1.0.0",
      "packet_id": str(uuid.uuid4()),
      "ts": ts_now(),
      "subject_id": f"anon:user-{random.randint(1,3)}",
      "source": {"device_id": f"edge-{random.randint(1,2)}", "sensor_profile":"PPG"},
      "metrics": {
        "hr_bpm": random.uniform(55, 110),
        "hrv_rmssd_ms": random.uniform(15, 60),
        "eda_uS": random.uniform(0.5, 8.0),
        "skin_temp_c": random.uniform(30.0, 36.0),
        "resp_bpm": random.uniform(8, 22),
        "spo2_pct": random.uniform(94, 100)
      },
      "state": {
        "valence": round(random.uniform(0.2, 0.8), 2),
        "arousal": round(random.uniform(0.2, 0.8), 2),
        "stress": round(random.uniform(0.1, 0.7), 2),
        "cognitive_load": round(random.uniform(0.2, 0.8), 2),
        "resilience": round(random.uniform(0.3, 0.9), 2),
        "confidence": round(random.uniform(0.5, 0.95), 2)
      },
      "quality": {"artifact_score": round(random.uniform(0.0, 0.25), 2), "calibrated": True, "missing": []},
      "calibration_id":"cal-demo",
      "privacy":{"consent_token":"jwt:demo","retention":"P7D","scopes":["local_only"]},
      "integrity":{"hash":"blake3:demo","signature":"ed25519:demo","key_id":"k1"}
    }
    path = os.path.join(out_dir, f"sample_{i+1:03d}.json")
    with open(path,"w") as f: json.dump(pkt, f, indent=2)

print(f"Wrote {N} packets to {out_dir}")

# Optional: quick validation of one file to show PASS
subprocess.call(["python3","tools/npp_validator.py", os.path.join(out_dir, "sample_001.json")])
