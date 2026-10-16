# Gates that live only in CI are not gates

(Supporting reference for `adversarial-verification-rounds`. The main SKILL.md is at its size ceiling, so
this lesson lives here; read it before you add a gate or trust one you have not executed.)

A gate that never executes on a workstation cannot be falsified there, so its first honest execution is a
red hosted run, and the round pays for it in someone else's time. This is the same failure class as a CI
step that hides its command's exit code: green because nothing said otherwise.

## Rules

1. **Put every assertion in a file the local suite can call, not in a YAML heredoc.** Then CI calls the
   same file. A heredoc is executed by exactly one thing (CI), so its type errors, stale field names and
   wrong-shape expectations are undiscoverable until push.
2. **Run the new gate locally BEFORE pushing, with the real input it will see in CI** — the document the
   product actually emits, not a hand-written fixture. A fixture asserts what you believed; the real
   document asserts what is.
3. **Assert the TYPE as well as the value**, and derive the expected type from the producer's code. Measured:
   a gate asserted `isinstance(doc["families"], dict) and len(...) == 19` while the producer reports
   `families` as the family COUNT (an `int`). The value was right (19), the assertion was still false, and
   the job failed blaming the product for a gate bug. Watch booleans too: `True == 1` passes a value check.
4. **Local execution must be mechanical, not a re-typed copy.** Extract the step's `run` and `env` out of the
   workflow YAML and execute it in the subject directory, so the local check cannot drift from what CI runs.
   Two host traps when you do: a bare `bash` may be WSL bash (cannot read `C:/` paths, and it mangles
   backticks and quotes in arguments), so name Git bash explicitly; and pass the script as a FILE rather
   than `bash -c <script>`, because the run text contains quotes, backticks, `$` expansions and Windows
   paths, and one argument reparse is enough to change what bash executes. Strip `\r` as well: a stray CR
   turns `set -euo pipefail` into a failed command lookup.
5. **A gate must be falsifiable by construction, and you must show it.** Pair the positive assertion with
   mutated inputs that must be REFUSED (wrong type, wrong value, wrong mode, a path that resolves back into
   the checkout). A gate that accepts everything and a gate that refuses everything look identical from the
   outside; the negative controls are what make the green mean something.
6. **Strengthen while you repair.** The replacement for a wrong gate should check more than the original and
   say why: `mode == INSTALLED` did not prove the artifact's schemas were the ones resolved, so the repaired
   gate also requires the resolved path NOT to be inside the checkout. Otherwise the repair reads as a
   loosening.
7. **A gate whose scope base comes from the pull request's base branch measures the wrong range.** When one
   workstream is stacked on another, `main...HEAD` attributes the lower branch's writes to the upper branch
   and the gate fails on paths nobody was governing. Have the subject DECLARE which stage it is, resolve the
   declared base to a commit, require that base to be an ancestor of the subject, and print the pull request
   base as context that is explicitly not the governed set. Keep the frozen-path denial list intact and keep
   the classifier self-test, so the correction cannot be a loosening.
8. **Prefer a resolved ref over a hardcoded base sha** for a stacked subject, and verify the ref is present
   in the CI checkout before relying on it (`actions/checkout` fetches `+refs/heads/*:refs/remotes/origin/*`,
   so `origin/<branch>` is there — check the checkout step's log rather than assuming). State the
   consequence: if the lower branch advances, the upper one goes red until it is re-stacked. That is the
   invariant, not an accident — but it must be written down, or it reads as flakiness.

## Reporting

When a gate you added is caught by CI, record it in the round's own evidence and name the class ("a red
produced by a gate that was never executed locally") instead of folding the fix into the product's
changelog. A reviewer who finds the self-inflicted red later cannot tell it apart from a concealment.
