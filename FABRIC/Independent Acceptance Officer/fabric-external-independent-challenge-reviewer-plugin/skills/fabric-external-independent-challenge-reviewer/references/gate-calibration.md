# Gate Calibration Failure Defense

For each release-significant or high-risk gate, check:

1. **Objective alignment** — does the gate test the product outcome/risk it claims to protect?
2. **Risk-proportionate strictness** — is the gate neither cosmetic nor unnecessarily impossible?
3. **Positive case** — does a known-good fixture pass?
4. **Negative/adversarial case** — does a known-bad or adversarial fixture fail?
5. **Regression baseline** — is the current result comparable to a frozen prior baseline?
6. **Anti-overfitting** — can the candidate pass by targeting the evaluator rather than the real behavior?
7. **Judge calibration** — if an LLM judgment is used, is it counterbalanced/grounded and subordinate to deterministic checks where possible?
8. **HITL** — is human/domain calibration present where the frozen risk model requires it?
9. **Evaluator integrity** — did the candidate change the gate/evaluator/fixture it is being judged by? If yes, route as a separate governed evaluator change.

A gate that cannot demonstrate basic calibration must not be treated as strong evidence merely because it is strict.
