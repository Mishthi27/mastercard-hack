# Solution and red-team handoff

## One-sentence solution

**MandateGuard is a closed-loop payment-security lab that turns a broad, safe threat atlas into stateful synthetic payment attacks, detects their deviation from a signed user intent, and uses the survivors to harden the defense.**

## What is already strong

The team plan has an unusually clear differentiator: agentic payment fraud is evaluated not only from a transaction row, but from the gap between an earlier user-signed intent, the cart, the final payment and the agent's provenance trace. The judge-facing moments are excellent: a side-by-side legacy allow versus our block, an attack composer, arena lineage, and a vaccination replay. It maps directly to all five rubric items.

## Improvements to make without changing the core idea

1. **Do not make unverified performance claims.** The current fidelity and arena fallback files label themselves as demos. Replace them with held-out, blue-model evidence before quoting PR-AUC, recall or ASR in the walkthrough.
2. **Make the protocol wording defensible.** Present the chain as an AP2-inspired *synthetic mandate abstraction* unless each field has been checked against the current primary AP2 specification. Do not claim Mastercard or AP2 uses the exact demonstration fields.
3. **Show taxonomy breadth, simulate depth.** Keep all 50 Atlas entries, but say that 14 representative families are simulated. The 14 cover injection, mandate integrity, agent delegation, card testing, account/bust-out, UPI and APP fraud.
4. **Use a strict temporal split.** Blue should train on earlier generated events and evaluate on later events; never let `label.*`, `atlas_id`, injected flags or round number enter features.
5. **Treat calibration as a task, not a decoration.** Calibrate legitimate traffic with approved public datasets and report source/version, sampling and limits. A self-consistency score is not proof of realism.
6. **Keep the demo deterministic.** Commit a seed, the generated JSONL, metrics JSON, and graphics; do no live model training or LLM calls in front of judges.
7. **Add an honest residual-risk panel.** Examples: stealthy authorised push payments with no mandate chain, sparse-history accounts and unseen social-engineering language. State the mitigation: step-up, analyst review and drift monitoring.

## Red-team implementation

### Attack Atlas

`atlas/catalog.py` is the source of 50 machine-readable entries and `atlas/render.py` produces one YAML file per entry plus `results/atlas_matrix.json` for the UI. Each has an identifier, rail, channel, kill chain, observable signals, defensive hooks, severity and feasibility statement. It is intentionally a taxonomy, not a playbook for attacking real systems.

### Legitimate population and mandate twin

`sim/population.py` creates persistent customers, merchants and devices; normal traffic is not generated as independent random spreadsheet rows. `sim/mandate_twin.py` adds an agentic subset with a synthetic intent, cart and payment chain. It uses an HMAC demonstration signature to make the artefact reproducible without persistent keys; if the team needs ECDSA P-256 specifically, replace only the `sign` helper after agreeing the exact AP2 field names.

All amounts are integer minor units and timestamps are UTC ISO-8601 strings. Classic events intentionally set mandate and trace to `null`, so the Blue team can distinguish unavailable evidence from a clean chain.

### Fourteen behavioural injectors

`sim/attacks.py` changes only synthetic event metadata. The families are: prompt-injection provenance anomaly, price inflation, playback/constraint mismatch, near-expiry use, presence mismatch, fan-out, cart-hash mismatch, delegation hijack, unregistered merchant DID, later false dispute, card testing velocity, bust-out amount anomaly, deceptive UPI collect request and synthetic APP urgency marker.

Every injector is paired with a clear expected signal. That pairing is crucial: it lets Blue build a per-attack recall heatmap and shows the judge why a detection occurred.

### Fidelity

`sim/fidelity.py` writes basic distribution summaries, a 24-hour profile, observed fraud rate and legitimate-chain conformance. It deliberately marks this as **self-consistency only**. To complete fidelity evidence, Blue should add: KS tests and correlation deltas against allowed public references, a real-versus-synthetic discriminator AUC, TSTR, amount Benford checks and merchant frequency comparison.

### Genome and Arena

`sim/genome.py` represents attack parameters such as injection style, delegation hops, delay, fan-out and evasion. `loop/arena.py` mutates the strongest candidates, logs parent lineage for a phylogeny, and produces an SVG curve. It ships with a very small `HeuristicBlueScorer` so the entire red package runs alone. Its JSON result is explicitly marked as a **demo heuristic**, not a detection result. Replace it with B's frozen scorer and use a held-out evaluation set for any submitted ASR curve.

## Blue and Ship handoff

- Blue reads `data/events.jsonl`, creates features without touching `label.*`, writes `scores` and `decision`, and serializes a frozen scorer.
- Red passes that scorer into `run_arena`; rerun the arena and update only then the submitted ASR number.
- Ship reads `results/atlas_matrix.json`, `results/fidelity.json`, `results/arena_log.json`, `results/phylogeny.json`, and `data/events.jsonl`. The app should badge demo data and cached evidence clearly.

## Commands

```powershell
python run_red.py --events 5000 --seed 42
```

The command regenerates all red-team artefacts deterministically enough for a demo. It creates no network traffic and no real payment artefacts.
