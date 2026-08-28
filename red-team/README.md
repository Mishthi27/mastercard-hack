# Mastercard Defense Lab - Red Team

This is the safe, synthetic-only red-team module for the Mastercard Innovation Challenge. It creates a machine-readable attack atlas, stateful legitimate payment traffic, signed mandate chains, 14 labelled behavioural fraud simulations, and a five-round evasion arena.

## Run

```powershell
cd outputs/mastercard-red-team
python run_red.py --events 5000 --seed 42
```

Generated artifacts are written to `data/` and `results/`:

- `atlas/*.yaml` and `results/atlas_matrix.json`
- `data/events.jsonl` - contract-compatible labelled events
- `results/fidelity.json` - transparent synthetic-data checks
- `results/arena_log.json`, `results/phylogeny.json`, `results/asr_curve.svg`

The module intentionally simulates only metadata and behavioural signals. It does not contact payment systems, generate phishing pages, clone voices, or use real personal data.

## Integration contract

`data/events.jsonl` follows `contracts/event.schema.json`. Blue team must not read `label.*` at inference. A future blue scorer can replace the included `HeuristicBlueScorer` by implementing `score(event) -> float` in `loop/arena.py`.
