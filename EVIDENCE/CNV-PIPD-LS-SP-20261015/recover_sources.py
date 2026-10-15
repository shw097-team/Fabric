import os, hashlib, json, shutil

ROOT = r"C:/Projects/Agent_Workspace/_handover/CNV-PIPD-LS-SP-20261015"
with open(ROOT + "/PHYSICAL_SOURCE_READBACK_MANIFEST.json", encoding="utf-8") as f:
    src_manifest = json.load(f)
missing = {m["filename"]: m for m in src_manifest["missing"]}
hash_to_name = {m["sha256"]: fn for fn, m in missing.items()}
need_sizes = set(m["bytes"] for m in missing.values())
TARGET6 = "Fabric_Hermes_HGK_Convergence_Global_Engineering_Blueprint_v1.1.0_PATCHED_2026-10-15.md"
target_bytes = missing[TARGET6]["bytes"]

# 1) search whole C:/Users + ProgramData for the 6th file by size (fast), then hash
found6 = []
scanned = 0
for d in ["C:/Users", "C:/ProgramData", "C:/Temp", "C:/tmp"]:
    if os.path.isdir(d):
        for base, dirs, files in os.walk(d, onerror=lambda e: None):
            dirs[:] = [x for x in dirs if x not in (".git", "node_modules", "__pycache__")]
            for fn in files:
                p = os.path.join(base, fn)
                scanned += 1
                try:
                    if os.path.getsize(p) == target_bytes:
                        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
                        if h == missing[TARGET6]["sha256"]:
                            found6.append(p)
                except OSError:
                    pass
print("SIX_SCAN_SCANNED", scanned, "FOUND6", found6)

# 2) recycle bin: list all $R files, try rename to $R->original name (recycle pairs)
pairs = {}
rb = r"C:\$Recycle.Bin\S-1-5-21-2687334950-3868438633-1592137926-1000"
if os.path.isdir(rb):
    rfiles = [f for f in os.listdir(rb) if f.startswith("$R")]
    ifiles = [f for f in os.listdir(rb) if f.startswith("$I")]
    print("RECYCLE_$R_files", len(rfiles), "$I_files", len(ifiles))
    # $I files contain original names + sizes; parse minimal
    import struct
    meta = {}
    for f in ifiles:
        p = os.path.join(rb, f)
        try:
            data = open(p, "rb").read()
        except OSError:
            continue
        if len(data) < 24:
            continue
        ver = struct.unpack("<q", data[:8])[0]
        size = struct.unpack("<q", data[8:16])[0]
        # v2: name at offset 24 wide-char
        try:
            raw = data[24:24 + 520]
            name = raw.decode("utf-16-le", errors="ignore").split("\x00")[0]
        except Exception:
            name = ""
        meta["$R" + f[2:]] = {"name": name, "size": size}
    # decode sizes for the missing six
    for rf, m in sorted(meta.items()):
        for fn, pin in missing.items():
            if pin["bytes"] == m["size"] and (rf in rfiles):
                print("MAPPED", fn, "->", rf, "recycle_size", m["size"], "name", m["name"])

# 3) if 5 files recoverable: copy bytes into evidence readback with byte verify
recovered = {}
rbm = {
    "Fabric_Hermes_HGK_Convergence_Global_Engineering_Blueprint_2026-10-14.md": "$R1QRQJ8.md",
    "Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG_Blueprint_v1.0.0_FULL_DESTRUCTIVE_AUDIT_2026-10-15(1).md": "$R33F37M.md",
    "AUDIT_Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG_v1.0.0_FULL_DESTRUCTIVE_2026-10-15(1).md": "$R9BSFJU.md",
    "Fabric_HG-KSEOS_Convergence_PIPD-LS-PKG_Blueprint_v1.0.0_2026-10-15.md": "$RCD676D.md",
    "Fabric_Hermes_HGK_Convergence_Blueprint_Full_Destructive_Audit_2026-10-14(1).md": "$RF2D68N.md",
}
READBACK = os.path.join(ROOT, "physical_source_readback")
for fn, rf in rbm.items():
    src = os.path.join(rb, rf)
    if not os.path.isfile(src):
        continue
    h = hashlib.sha256(open(src, "rb").read()).hexdigest()
    if h != missing[fn]["sha256"]:
        print("HASH_MISMATCH_SKIP", fn, h)
        continue
    dst = os.path.join(READBACK, fn)
    if not os.path.exists(dst):
        shutil.copyfile(src, dst)
    h2 = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    recovered[fn] = {"path": dst, "bytes": os.path.getsize(dst), "sha256": h2,
        "origin_kind": "RECYCLE_BIN_BYTE_RECOVERY", "origin": src}
print("RECOVERED_COUNT", len(recovered))
for k, v in recovered.items():
    print("RECOVERED", k, v["bytes"], v["sha256"])
