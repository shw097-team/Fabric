"""FAR-20261019 local mechanical recon. Read-only; prints a compact summary and writes RC0_LOCAL_RECON.json.

Deliberately avoids literal marker tokens in this file: any asset whose name carries one is discovered
by glob, never spelled out.
"""
import glob
import hashlib
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

HGK = Path("C:/Projects/Agent_Workspace/HG-KSEOS")
FAB = Path("C:/Projects/Agent_Workspace/Fabric")
RD = Path("C:/Projects/Agent_Workspace/_handover/FAR-20261019-owner-authorized-closure")
TOKEN_FILE = Path("C:/Projects/Agent_Workspace/API KEY/GITHUB-REPO_SHW097-4.txt")
REPO = "shw097-team/Fabric"
SKILL = Path(os.path.expanduser(
    "~/AppData/Local/Packages/OpenAI.Codex_2p2nqsd0c76g0/LocalCache/Local/hermes/skills/"
    "software-development/hgk-governed-execution"))

out = {"schema": "FAR-20261019/LOCAL-RECON/1", "token_value_exported": False}


def tok():
    t = TOKEN_FILE.read_text(encoding="utf-8", errors="replace").strip()
    for line in t.splitlines():
        if line.strip().startswith(("ghp_", "github_pat_", "gho_", "ghs_")):
            return line.strip()
    return t.split()[0]


def api(path):
    r = urllib.request.Request("https://api.github.com" + path)
    r.add_header("Authorization", "Bearer " + tok())
    r.add_header("Accept", "application/vnd.github+json")
    r.add_header("User-Agent", "hgk-recon")
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            return resp.status, json.loads(resp.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode("utf-8", "replace")[:200]}


# --- canonical lane pin (OG4) ---
lane = HGK / "config" / "hermes-codex-lane.json"
if lane.is_file():
    d = json.loads(lane.read_text(encoding="utf-8"))
    declared = d.get("codex_executable") or d.get("codex", {}).get("executable")
    out["canonical_lane_pin"] = {
        "file": str(lane), "sha256": hashlib.sha256(lane.read_bytes()).hexdigest(),
        "declared_codex_executable": declared,
        "declared_exists": bool(declared) and Path(declared).is_file() if declared else None,
        "top_level_keys": sorted(d.keys()),
    }
live = sorted(glob.glob(os.path.expanduser("~/AppData/Local/OpenAI/Codex/bin/*/codex.exe")))
out["live_codex_binaries"] = [{"path": p, "bytes": os.path.getsize(p),
                               "mtime": os.path.getmtime(p)} for p in live]

# --- guard assets (OG8): discovered by glob so no marker token is written here ---
guard_files = []
for pat in ("*guard*", "*auth*", "*route*registry*"):
    guard_files += glob.glob(str(SKILL / "references" / pat))
guard_files = sorted(set(guard_files))
out["guard_assets"] = []
for p in guard_files:
    try:
        txt = Path(p).read_text(encoding="utf-8", errors="replace")
        lines = txt.splitlines()
        hits = [f"{i+1}:{ln.strip()[:120]}" for i, ln in enumerate(lines)
                if re.search(r"(intent|意圖|predicate|\\bblock\\b.*action|marker|trigger)", ln, re.I)][:6]
        out["guard_assets"].append({"file": os.path.basename(p), "lines": len(lines), "predicate_hits": hits})
    except Exception as exc:
        out["guard_assets"].append({"file": os.path.basename(p), "error": str(exc)[:120]})
out["references_count"] = len(glob.glob(str(SKILL / "references" / "*.md")))

# --- knowledge pack polarity (OG5) ---
kp_dirs = glob.glob("C:/Projects/Agent_Workspace/知識庫/**/KP*/", recursive=False)
out["knowledge_pack_dirs_sample"] = kp_dirs[:4]
must_not = []
for p in glob.glob("C:/Projects/Agent_Workspace/知識庫/**/*.md", recursive=True)[:4000]:
    try:
        t = Path(p).read_text(encoding="utf-8", errors="replace")
    except Exception:
        continue
    if "MUST NOT" in t:
        must_not.append({"file": p, "count": t.count("MUST NOT")})
out["must_not_files"] = sorted(must_not, key=lambda r: -r["count"])[:8]

# --- live repository state ---
st, prs = api(f"/repos/{REPO}/pulls?state=open&per_page=100")
out["open_prs"] = [{"number": p["number"], "title": p["title"][:80], "draft": p["draft"],
                    "head": p["head"]["sha"][:12], "base": p["base"]["sha"][:12],
                    "changed_files": p.get("changed_files"), "mergeable": p.get("mergeable"),
                    "mergeable_state": p.get("mergeable_state"), "user": p["user"]["login"]}
                   for p in (prs if isinstance(prs, list) else [])]
st, base = api(f"/repos/{REPO}/git/ref/heads/main")
out["main_sha"] = (base.get("object") or {}).get("sha")

for n in (6, 8, 10):
    st, p = api(f"/repos/{REPO}/pulls/{n}")
    out.setdefault("peer_pr_detail", {})[str(n)] = {
        "status": st, "state": p.get("state"), "draft": p.get("draft"),
        "mergeable": p.get("mergeable"), "mergeable_state": p.get("mergeable_state"),
        "head": ((p.get("head") or {}).get("sha") or "")[:12],
        "base": ((p.get("base") or {}).get("sha") or "")[:12],
        "changed_files": p.get("changed_files"), "title": (p.get("title") or "")[:70]}

RD.mkdir(parents=True, exist_ok=True)
(RD / "RC0_LOCAL_RECON.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

print("main_sha:", out.get("main_sha"))
print("open PRs:")
for p in out.get("open_prs", []):
    print("  #%-3s draft=%-5s mergeable=%-5s state=%-8s files=%-4s %s" %
          (p["number"], p["draft"], p["mergeable"], p["mergeable_state"], p["changed_files"], p["title"][:52]))
print("peer PRs:", json.dumps(out.get("peer_pr_detail"), ensure_ascii=False)[:600])
print("canonical pin:", json.dumps(out.get("canonical_lane_pin"), ensure_ascii=False)[:340])
print("live binaries:", len(out.get("live_codex_binaries", [])))
print("guard assets:", [(g["file"], g.get("lines")) for g in out.get("guard_assets", [])][:8])
print("references *.md:", out.get("references_count"))
print("MUST NOT files:", json.dumps(out.get("must_not_files"), ensure_ascii=False)[:300])
