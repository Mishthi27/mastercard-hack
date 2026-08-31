# Mastercard AI Defense Lab - Blue Team

## Overview
MandateGuard BLUE TEAM implements a multi-modal feature extraction and evaluation pipeline for agentic payment fraud detection.

## Architecture
```text
events.jsonl -> Feature Extractors -> Tabular Model (LightGBM) -> Fusion -> Policy Action
```
Features are broken down into:
- **Semantic**: text embeddings using `sentence-transformers`
- **Provenance**: agent trace fingerprints and topic shifts
- **Structural**: mandate chain consistency and signatures
- **Temporal**: event velocities
- **Economic**: amount anomalies and budget utilization

## Execution
Run the following commands from the workspace root:

1. `python blue-team/train.py`
2. `python blue-team/inference.py`
3. `python blue-team/evaluate.py`
4. `python blue-team/vaccination.py`

## Arena Compatibility
`blue-team/blue_api.py` exposes a `score(event)` function.
To use it in `loop/arena.py`, import it and call `blue_api.score(event)`.

## Limitations
This is a demonstration pipeline optimized for a hackathon. Some embeddings use caching/mock defaults if network requests to huggingface fail.
