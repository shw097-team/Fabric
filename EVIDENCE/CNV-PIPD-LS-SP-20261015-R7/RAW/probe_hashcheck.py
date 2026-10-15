import json, sys, hashlib
sys.path.insert(0, "C:/Projects/Agent_Workspace/PIPD/src")
from pipd_ls_sp import pipeline, validate
from pipd_ls_sp.util import canonical_json, sha256_text
SRC="C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015/R6_DELIVERY/RAW/pipd_scratch_source.md"
import pathlib
def _bh(rec):
    body={k:v for k,v in rec.items() if k not in ("subject_id","version","content_hash","schema_version","trace","_profile_meta")}
    return hashlib.sha256(json.dumps(body,sort_keys=True,ensure_ascii=False,separators=(",",":")).encode()).hexdigest()
card=pipeline.intake("bind the R6 scratch requirements", sources=[SRC])
pi=pipeline.compile_pi(card,"LITE")
atom=pipeline.atoms_of(pi)[0]
tl=pi["trace"][0]
pb=pi["stable_semantic_contract"]["profile_binding"]
for name,rec in (("PI",pipeline.strip_sidecar(pi)),("ATOM",atom),("TL",tl),("PB",pb)):
    recorded=rec.get("content_hash")
    print(name, "len_fields=",len(rec), "sid=",rec.get("subject_id"), "recorded=",recorded[:12] if recorded else None,
          "bodyhash=",_bh(rec)[:12], "match=", recorded==_bh(rec))
print("profile_binding assurance=",pb.get("assurance"),"artifact_depth=",pb.get("artifact_depth"))
print("oracle=", json.dumps(atom["risk_guard"]["oracle"]))
print("tl keys=", sorted(tl.keys()))
print("pi acceptance=", json.dumps(pi["acceptance"]))
print("pi stable contract keys=", sorted(pi["stable_semantic_contract"].keys()))
