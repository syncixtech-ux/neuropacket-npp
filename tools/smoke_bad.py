#!/usr/bin/env python3
# Intentionally missing consent + bad ranges
import json, uuid
from datetime import datetime, timezone
pkt = {
  "version":"1.0.0",
  "packet_id": str(uuid.uuid4()),
  "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")+"Z",
  "subject_id":"anon:demo",
  "source":{"device_id":"edge-1","sensor_profile":"PPG"},
  "metrics":{"hr_bpm":400,"hrv_rmssd_ms":-1,"eda_uS":4.1,"skin_temp_c":55.0,"resp_bpm":80,"spo2_pct":140},
  "state":{"valence":1.2,"arousal":-0.1,"stress":0.3,"cognitive_load":0.5,"resilience":0.7,"confidence":0.9},
  "quality":{"artifact_score":1.5,"calibrated":True,"missing":[]},
  "calibration_id":"cal-demo",
  "privacy":{"retention":"P7D","scopes":["local_only"]},  # missing consent_token
  "integrity":{"hash":"","signature":"","key_id":""}
}
open("tests/vectors/_smoke_bad.json","w").write(json.dumps(pkt,indent=2))
print("Wrote tests/vectors/_smoke_bad.json")
import subprocess, sys
sys.exit(subprocess.call(["python3","tools/npp_validator.py","tests/vectors/_smoke_bad.json"]))
