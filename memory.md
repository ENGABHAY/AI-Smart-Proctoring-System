# Memory — AI Smart Proctoring System

Running context for anyone (or any AI assistant) picking this project up
later. Decisions and why, not just what.

## What this is

A portfolio project: YOLOv8-based exam proctoring that flags suspicious
objects/behavior from a webcam or recorded video, logs it to CSV, and
saves evidence frames. Built as a notebook first, then refactored into a
small modular app (`APP/`).

## Key decisions

- **6 → 4 classes.** Original Roboflow dataset had book, cell phone,
  headphone, laptop, person, tv. Dropped `laptop` and `tv` — not
  reliably attributable as "suspicious" in an exam context, and not
  worth the training signal. See `design.md` for the full reasoning.
- **Rule-based scoring, not learned.** Suspicion is three explicit
  rules (no person / multiple people / prohibited object), not a
  trained classifier on top of detections. Chosen for explainability —
  a reviewer can see exactly why a frame was flagged.
- **Top-N evidence only.** Saving every suspicious frame would flood the
  evidence folder; only the top 5 by score are kept per session.
- **YOLOv8n, not a larger variant.** Chosen for CPU-viability — this is
  meant to run on a normal laptop, not a GPU server.

## Known issues (don't lose these)

- `APP/config.py` → `MODEL_PATH` references `model/yolo_v1.pt`, but the
  committed weights file is `model/yolo_v12.pt`. This has been flagged
  multiple times across sessions and **is still unfixed** as of the last
  update to this file. Fix it before claiming the app "just works" from
  a fresh clone.
- No automated tests exist anywhere in the repo.
- The Roboflow API key that was originally hardcoded in the notebook has
  been moved to `os.environ["ROBOFLOW_API_KEY"]` — if you see a literal
  key string reappear in any notebook cell, that's a regression, pull it
  back out.

## Validated results (don't re-derive, these are from the actual
training run in `Notebook/object_detection.ipynb`)

| Class | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| book | 0.879 | 0.956 | 0.959 | 0.663 |
| cell phone | 0.902 | 0.946 | 0.933 | 0.525 |
| headphone | 0.825 | 0.856 | 0.850 | 0.377 |
| person | 0.955 | 0.970 | 0.980 | 0.717 |
| **All (mean)** | **0.890** | **0.932** | **0.931** | **0.570** |

`headphone` is consistently the weakest class — if this project gets
revisited, that's the first thing worth improving (more data/
augmentation), not a different architecture.

## Document map

- `prd.md` — what this is for and who it's for.
- `architecture.md` — how the pieces fit together.
- `design.md` — why specific behavior/UX decisions were made.
- `rules.md` — conventions to follow when touching the code.
- `tasks.md` — done vs. open work.
- `WORKFLOW.md` / `WORKFLOW.txt` — the actual frame-by-frame pipeline,
  diagrammed.
- `README.md` — public-facing summary (what a recruiter/visitor sees
  first).
