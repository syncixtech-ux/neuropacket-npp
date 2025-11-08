#!/usr/bin/env python3
import json, uuid
from datetime import datetime, timezone
pkt = {
  "version":"1.0.0",
  "packet_id": str(uuid.uuid4()),
  "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]+"Z",
  "subject_id":"anon:demo",
  "source":{"device_id":"edge-1","sensor_profile":"PPG"},
  "metrics":{"hr_bpm":72,"hrv_rmssd_ms":32,"eda_uS":4.1,"skin_temp_c":33.0,"resp_bpm":12,"spo2_pct":98},
  "state":{"valence":0.5,"arousal":0.4,"stress":0.3,"cognitive_load":0.5,"resilience":0.7,"confidence":0.9},
  "quality":{"artifact_score":0.08,"calibrated":True,"missing":[]},
  "calibration_id":"cal-demo",
  "privacy":{"consent_token":"jwt:demo","retention":"P7D","scopes":["local_only"]},
  "integrity":{"hash":"blake3:demo","signature":"ed25519:demo","key_id":"k1"}
}
open("tests/vectors/_smoke_ok.json","w").write(json.dumps(pkt,indent=2))
print("Wrote tests/vectors/_smoke_ok.json")
import subprocess, sys
sys.exit(subprocess.call(["python3","tools/npp_validator.py","tests/vectors/_smoke_ok.json"]))
