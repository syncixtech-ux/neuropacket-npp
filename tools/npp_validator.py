#!/usr/bin/env python3
import sys, json, re

RFC3339Z_MS = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$')
UUIDv4 = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$', re.I)

def check(pkt):
    problems = []
    req = ["version","packet_id","ts","subject_id","source","metrics","state","quality","calibration_id","privacy","integrity"]
    for k in req:
        if k not in pkt: problems.append(f"missing_required_field:{k}")
    if "packet_id" in pkt and not UUIDv4.match(str(pkt["packet_id"])):
        problems.append("invalid_uuid_v4:packet_id")
    if "ts" in pkt and not RFC3339Z_MS.match(str(pkt["ts"])):
        problems.append("invalid_timestamp_format:ts")
    metrics = pkt.get("metrics",{})
    def rng(key, lo, hi):
        v = metrics.get(key); 
        if v is not None:
            try:
                fv = float(v)
                if not (lo <= fv <= hi):
                    problems.append(f"out_of_range:metrics.{key}={v} not in [{lo},{hi}]")
            except Exception:
                problems.append(f"type_error:metrics.{key} must be number")
    rng("hr_bpm",0,300); rng("hrv_rmssd_ms",0,500); rng("eda_uS",0,100); rng("skin_temp_c",20,45); rng("resp_bpm",0,60); rng("spo2_pct",0,100)
    state = pkt.get("state",{})
    for k in ["valence","arousal","stress","cognitive_load","resilience","confidence"]:
        v = state.get(k)
        if v is None: problems.append(f"missing_state:{k}")
        else:
            try:
                fv = float(v)
                if not (0.0 <= fv <= 1.0): problems.append(f"out_of_range:state.{k}={v} not in [0,1]")
            except Exception:
                problems.append(f"type_error:state.{k} must be number")
    privacy = pkt.get("privacy",{})
    if not privacy.get("consent_token"): problems.append("privacy:missing_consent_token")
    if not privacy.get("retention"): problems.append("privacy:missing_retention")
    if not isinstance(privacy.get("scopes"), list): problems.append("privacy:scopes_must_be_array")
    integ = pkt.get("integrity",{})
    if not integ.get("hash"): problems.append("integrity:missing_hash")
    if not integ.get("signature"): problems.append("integrity:missing_signature")
    if not integ.get("key_id"): problems.append("integrity:missing_key_id")
    q = pkt.get("quality",{})
    a = q.get("artifact_score")
    try:
        if a is None or not (0.0 <= float(a) <= 1.0): problems.append("quality:artifact_score_out_of_range_or_missing")
    except Exception:
        problems.append("type_error:quality.artifact_score must be number")
    return problems

def main():
    if len(sys.argv) < 2:
        print("Usage: npp_validator.py <packet.json>"); sys.exit(2)
    with open(sys.argv[1],"r") as f:
        pkt = json.load(f)
    probs = check(pkt)
    if probs:
        print("FAIL"); [print(" -",p) for p in probs]; sys.exit(1)
    print("PASS")

if __name__ == "__main__":
    main()
