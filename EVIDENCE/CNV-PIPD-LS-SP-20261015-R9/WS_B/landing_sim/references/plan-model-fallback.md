# PLAN-lane model fallback (operator standing instruction, 2026-10-08)

## Rule

The Planning intelligence lane of a governed HGK/FAR round runs on
`gpt-6.1-sol` / `openai-codex` (OpenAI OAuth). **If that model's usage/quota is exhausted, the
PLAN lane MUST switch to its declared fallback: `mimo-v2.6-pro` / `opencode-go`**
(operator instruction 2026-10-08, superseding the earlier `glm-5.3` declaration).

Do not silently substitute a different model, and never let a quota exhaustion turn into a
skipped PLAN lane: a blocked PLAN lane means no adjudication, which is worse than a recorded
fallback.

## Use the provider-qualified id

- Correct id form: **`opencode-go/mimo-v2.6-pro`**. Measured: qualified id -> HTTP 200 with a real
  completion; the bare `mimo-v2.6-pro` did not answer, and `opencode-go/mimo-v2.6` returned HTTP 400
  `Model is unavailable`.
- The relay's `GET /v1/models` is **not authoritative** (it listed only `opencode-go/deepseek-v4.1-flash`
  while the fallback was in fact served - consistent with the known finding that de-listing does not
  stop the direct completion path). Verify a model by a minimal completion probe through
  `http://127.0.0.1:10101/v1/chat/completions` with the `x-opencode-session` header (without it the
  relay answers 400 MissingSessionID), `max_tokens: 1`, then read the served `model` field back.
- A probe **timeout is inconclusive, not proof of unavailability** - a model can be cold/slow over the
  relay while still resolving correctly through Hermes' own provider client. Record timeouts as
  NOT_TESTED rather than unavailable.

## How to record it

Treat the fallback as a **model-SoD deviation**, not as a detail:

1. State it in the round receipt (`model_sod` block): requested model, served model, why.
2. Bind it to evidence: the quota/error text you actually saw (verbatim), not a paraphrase, plus
   the probe receipt if you tested availability.
3. Put the same statement in the round report's model-SoD section before any verdict is read.

## Independence

`mimo-v2.6-pro` is distinct from the VERIFY/SECURITY checker model (`glm-5.3-flash`), so falling
back here **preserves model-level maker/checker separation** - unlike the earlier `glm-5.3`
declaration, which would have collapsed it. If a future instruction ever points the fallback at the
checker's own model, that round must say so explicitly and must not claim model diversity as part of
its acceptance argument; process-level separation (fresh one-shot process, different session, own
write scope) must stay intact regardless.

## Fail-closed shape

- PLAN on primary exhausted -> ONE fallback attempt on `opencode-go/mimo-v2.6-pro` -> if that also
  fails, mark the PLAN lane BLOCKED with the verbatim errors and stop; do not shop for a third model.
- A fallback PLAN ruling carries the same claim ceiling (`CANDIDATE_ONLY`) and the same requirement
  to cite evidence; it does not gain authority from having been run on a fallback.
