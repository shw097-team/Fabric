# FAR run 015 - R10-0 session closure synthesis

## Decision

Close what is closable WITHOUT over-engineering and WITHOUT manufacturing anything; hand the rest over with a
locator and an owner. Concretely: (1) adjudicate the two stale change records rather than tick or rewrite them;
(2) repair the two defects in this session's OWN tooling, because they destroyed evidence this round depends on;
(3) ship a closure/handover package; (4) deliver the packet for external verification.

## What the measurements decided

- **The rebind the stale record asks for is ALREADY LIVE.** Registry epoch 21, `PLAN` = `openai-codex/gpt-6.1-sol`
  (medium, ADMITTED), `check_drift` `[]` - applied by an act **outside** this round at 12:36:30. So 20 of that
  record's 25 rows are `DONE_MEASURED` but **unticked**: the record is stale, not the work. This round does not
  edit another round's record (a peer round is publishing that packet right now).
- **The cap-remediation premise was already false.** The pre-slim main file measured **99,996 of 100,000**
  LF-normalized characters by the governing constant; it never exceeded the cap. The file now sits at **21,026
  bytes**. Splitting it would be the over-engineering the order explicitly forbids, so the remedy is
  `SUPERSEDED` and the honest remainder is a regrowth guard plus a **73-of-112 unlisted-reference index gap**.
- **This session's own tooling destroyed evidence.** One receipt path served five EXECUTE turns and three
  VERIFY_SECURITY turns; and the dispatcher's nonce gate reported a nonce absent while the nonce sat in the
  429,783-byte stdout that same receipt recorded. Both are repaired in a successor wrapper with **8 passing
  local tests**, including a regression against the earlier round's real receipt.
- **A new control-plane defect surfaced**: `check_sod(PLAN, VERIFY_SECURITY)` = **SOD_VIOLATION** - the registry
  itself now puts the maker and the checker on the same model.
- **One child probe was wrong** (a "0-byte SKILL.md"): the file is 35,739 bytes and loaded fine. Recorded as a
  probe defect; the product was never in question.

## What is NOT claimed

No acceptance, no Gate PASS, no AO verdict, no release, no product behaviour. The verification of this round is
performed by a checker bound to the SAME arm as the writer, so model-axis independence is **absent**; only
process/lane separation plus a re-derivation duty remains, and the checker's verdict is advisory evidence.
