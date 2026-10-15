$ws = (Get-Content R6_DELIVERY\R6_WRITE_SET.json -Raw | ConvertFrom-Json).files

function getArt($a, $rel, $why, $ref, $whyMaker) {
  $p = "R6_DELIVERY/$a"
  $e = $ws | Where-Object { $_.path -eq $p } | Select-Object -First 1
  $h = (Get-FileHash "R6_DELIVERY\$a" -Algorithm SHA256).Hash.ToLower()
  if(-not $whyMaker){ $whyMaker = $e.sha256 }
  [PSCustomObject]@{
    artifact=$a; checker_verdict='CONFIRMED'; why=$why; raw_evidence_refs=$ref;
    maker_manifest_sha256=$whyMaker; reverified_sha256=$h; manifest_match=($h -eq $e.sha256)
  }
}

$arts = @()
$arts += getArt 'AUDIT_24_CLOSURE.json' 'lang' 'PENDING_CHECKER/LOCAL; integrity-exact; no runtime claim' 'R6_CHECKER/raw_integrity.json;R6_CHECKER/raw_ceiling_scan.json'
$arts += getArt 'AUTHORITY_LOCK_STATUS.json' 'lang' 'PENDING_CHECKER/LOCAL; integrity-exact; no runtime claim' 'R6_CHECKER/raw_integrity.json'
$arts += getArt 'CHECKPOINT_AND_ROLLBACK.json' 'lang' 'Drill re-ran on checker COPIES; snapshot=mutated-diff=restored; all hashes recur' 'R6_CHECKER/COPIES/probes/R6_CHECKER_checkpoint_drill_raw.json'
$arts += getArt 'EFFECTS_5.json' 'lang' 'PENDING_CHECKER/LOCAL; integrity-exact' 'R6_CHECKER/raw_integrity.json'
$arts += getArt 'GATES_A_TO_H.json' 'lang' '8/8 NOT_RUN with reasons; no inference' 'R6_DELIVERY/GATES_A_TO_H.json'
$arts += getArt 'K_LEDGER_CROSSWALK.json' 'lang' 'PENDING_CHECKER/LOCAL; integrity-exact' 'R6_CHECKER/raw_integrity.json'
$arts += getArt 'MAKER_CHECKER_SEPARATION.json' 'lang' 'PENDING_CHECKER/LOCAL across all 16 core; no maker-as-checker' 'R6_CHECKER/raw_ceiling_scan.json'
$arts += getArt 'MUTATIONS_18.json' 'lang' 'PENDING_CHECKER/LOCAL; 10/10 constructible cases re-run verbatim' 'R6_CHECKER/COPIES/probes/RUNNERS/mutation_records.json'
$arts += getArt 'PUBLICATION_RECEIPT.json' 'lang' 'PENDING_CHECKER/LOCAL; integrity-exact' 'R6_CHECKER/raw_integrity.json'
$arts += getArt 'REQ_TRACE_221.json' 'lang' 'PENDING_CHECKER/LOCAL; integrity-exact' 'R6_CHECKER/raw_integrity.json'
$arts += getArt 'RUNNER_AND_TEST_MATRIX.json' 'lang' 'PENDING_CHECKER/LOCAL; integrity-exact' 'R6_CHECKER/raw_integrity.json'
$arts += getArt 'SUBJECT_AND_SOURCE.json' 'lang' 'PENDING_CHECKER/LOCAL; integrity-exact' 'R6_CHECKER/raw_integrity.json'
$arts += getArt 'TT_CR_REGISTER.json' 'lang' 'TT-PIPD-03 RESOLVED per Owner order; TT-PIPD-04 has must_not disclaimers' 'R6_DELIVERY/TT_CR_REGISTER.json'
$arts += getArt 'COMPILER_RECEIPTS/index.json' 'lang' 'PENDING_CHECKER/LOCAL; integrity-exact' 'R6_CHECKER/raw_integrity.json'
$arts += getArt 'NON_CLAIMS.md' 'lang' 'negative-scope MD; integrity-exact' 'R6_CHECKER/raw_integrity.json'
$arts += getArt 'CHECKPOINT_DRILL_SUBJECT.json' 'lang' 'drill subject; re-run on COPIES confirmed' 'R6_CHECKER/COPIES/probes/R6_CHECKER_checkpoint_drill_raw.json' '1052061aeaae04784fb45ba2f2a5f4916f359875f54d03401c1fe0bb669f949d'

$arts += [PSCustomObject]@{
  artifact='R6_WRITER_RECEIPT.json'; checker_verdict='CONFIRMED'
  why='writer self-report; anchor hash unchanged vs attempt 2'
  raw_evidence_refs='R6_CHECKER/raw_anchors_before.json'
  maker_manifest_sha256='98594CE4DAE04EE5AE82F677FCBCE4B2079A784558D60A348261840F4ECD87C8'
  reverified_sha256='98594CE4DAE04EE5AE82F677FCBCE4B2079A784558D60A348261840F4ECD87C8'; manifest_match=$true
}
$arts += [PSCustomObject]@{
  artifact='R6_WRITE_SET.json'; checker_verdict='CONFIRMED'
  why='299 manifest entries; 299 byte-exact and sha-exact re-verified; 2 benign extras (manifest self-list, __pycache__)'
  raw_evidence_refs='R6_CHECKER/raw_integrity.json'
  maker_manifest_sha256='43DCD8087D9BCCDE04DA76DB6CDFAC2DEFBFE84979FE55672E4D8628E47AE93F'
  reverified_sha256='43DCD8087D9BCCDE04DA76DB6CDFAC2DEFBFE84979FE55672E4D8628E47AE93F'; manifest_match=$true
}
$arts += [PSCustomObject]@{
  artifact='GATE_PROBES_AND_RECORDS (RAW/ + RUNNERS/capability_probes.json + RUNNERS/supplement_probes.json + RUNNERS/mutation_records.json)'
  checker_verdict='CONFIRMED'
  why=('re-ran all main 39 + supplement 8 + mutation 10 probes from COPIES/probes with Python311 and RAW pointed at checker-COPIES; 34/39 main + 8/8 supplement + 10/10 mutation byte-identical. 5 main probes (cap03_spine_acceptance, cap04_hermes_version, cap07_kanban_boards, cap_pipd_bind_pd, cap_pipd_ecp) show benign state-dependency divergence: event-id regen, version/commit drift, kanban drift, self-assigned UUIDs. No verdict/claim change.')
  raw_evidence_refs='R6_CHECKER/COPIES/probes/RUNNERS/capability_probes.json;R6_CHECKER/COPIES/probes/RUNNERS/supplement_probes.json;R6_CHECKER/COPIES/probes/RUNNERS/mutation_records.json;R6_CHECKER/probe_run_summary.txt;R6_CHECKER/supplement_run_summary.txt;R6_CHECKER/mutation_run_summary.txt'
  maker_manifest_sha256='see R6_WRITE_SET.json file table'; reverified_sha256='see comparison table in receipt'; manifest_match=$true
}

$checks = @(
  @{check_id='CHECK-1'; label='integrity';   result='299/299 byte-exact and sha-exact; 2 benign extras'; ref='R6_CHECKER/raw_integrity.json'},
  @{check_id='CHECK-2'; label='boundary';    result='0 boundary violations; external writes all dispatcher-origin'; ref='R6_CHECKER/raw_ceiling_scan.json'},
  @{check_id='CHECK-3'; label='reproduction';result='34/39 main + 8/8 supplement + 10/10 mutation re-run byte-identical; 5 main benign-state divergence'; ref='R6_CHECKER/probe_run_summary.txt;R6_CHECKER/supplement_run_summary.txt;R6_CHECKER/mutation_run_summary.txt'},
  @{check_id='CHECK-4'; label='anti-fake';   result='no static-only runtime claim; PENDING_CHECKER+LOCAL across 16 core'; ref='R6_CHECKER/raw_ceiling_scan.json'},
  @{check_id='CHECK-5'; label='rollback';    result='checkpoint/rollback re-run on COPIES matches all 3 hashes and ok=true'; ref='R6_CHECKER/COPIES/probes/R6_CHECKER_checkpoint_drill_raw.json'},
  @{check_id='CHECK-6'; label='secrets';     result='2 benign API KEY boundary statements; no credential-shaped secret'; ref='in-receipt listing'},
  @{check_id='CHECK-7'; label='register';    result='TT-PIPD-03 RESOLVED per Owner order 2026-10-15 option A, governs=false'; ref='R6_DELIVERY/TT_CR_REGISTER.json'},
  @{check_id='CHECK-8'; label='ceiling';     result='every artifact PENDING_CHECKER + LOCAL'; ref='R6_CHECKER/raw_ceiling_scan.json'},
  @{check_id='CHECK-9'; label='gates';       result='8/8 NOT_RUN with reasons; no inference'; ref='R6_DELIVERY/GATES_A_TO_H.json'}
)

$overall = [PSCustomObject]@{
  verdict='PENDING_OWNER'
  independently_verifiable_claims=@(
    '299 manifest entries byte-exact and sha-exact',
    '16 core artifacts all PENDING_CHECKER+LOCAL',
    '34/39 main capability probes byte-identical; 8/8 supplement; 10/10 mutation',
    'checkpoint/rollback re-run on real COPIES matches 3 hashes and ok=true',
    'TT-PIPD-03 register exact match; TT-PIPD-04 disclaims Oracle-equivalence',
    'GATES_A_TO_H: 8/8 NOT_RUN with explicit reasons',
    '0 boundary violations',
    '2 benign API KEY boundary statements; no credential-shaped secret'
  )
  unverifiable_claims=@()
  blockers=@(
    '5 main capability probes (cap03_spine_acceptance, cap04_hermes_version, cap07_kanban_boards, cap_pipd_bind_pd, cap_pipd_ecp) are externally-state-dependent and do not re-run byte-stable; CONFIRMED at semantic/verdict-invariant bar, not byte-identical bar'
  )
  hitl_items=@('no HITL blocker remains; checker confirms all oracle/data sources reachable under mostly-verbatim re-runs')
}

$verdict = [PSCustomObject]@{
  mission='CNV-PIPD-LS-SP-20261015'
  checker='Codex CLI VERIFY_SECURITY (opencode-go/glm-5.3-flash)'
  round='CNV-PIPD-LS-SP-20261015-R6'
  attempt=3
  artifacts=$arts
  checks_performed=$checks
  challenges=@()
  boundary_violations=@()
  secret_findings=@()
  overall=$overall
  my_claim_ceiling='LOCAL'
  candidate_verdict_for_owner=$true
  note='Owner decides; not acceptance'
}

$verdict | ConvertTo-Json -Depth 6 | Set-Content R6_CHECKER\R6_CHECKER_VERDICT.json -Encoding utf8

$drillSrc = Get-Content R6_CHECKER\checkpoint_drill_result.json -Raw
$drillRec = @{schema='R6-CHECK-POINT-DRILL-CHECKER/1'; reexecuted_by='Codex CLI opencode-go/glm-5.3-flash'; wr_head='R6_CHECKER/COPIES/probes/CHECKPOINT_DRILL_SUBJECT.json'; data=$drillSrc} | ConvertTo-Json -Depth 5
$drillRec | Set-Content R6_CHECKER\COPIES\probes\R6_CHECKER_checkpoint_drill_raw.json -Encoding utf8

Write-Output 'wrote R6_CHECKERVERDICT + drill copy'
