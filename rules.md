# Rules — AI Smart Proctoring System

Conventions for working on this codebase (human or AI assistant).

## Module boundaries

Each file in `APP/` owns exactly one concern — don't blur them:
- `config.py` — constants only. No logic.
- `video_source.py` — capture/timing only. No detection or scoring.
- `detector.py` — model load + inference only. No suspicion logic.
- `suspicion.py` — pure scoring function, no I/O, no file writes.
- `evidence_manager.py` — all file/CSV writes live here. Other modules
  don't touch `reports/` directly.
- `main.py` — orchestration and the CLI loop only; no detection or
  scoring logic duplicated here.

## Config, not hardcoding

Any threshold, path, FPS value, or class name goes in `config.py` and is
imported — never hardcoded inline in a second place. If you need a new
tunable value, add it to `config.py` first.

## Paths

Always resolve paths through `PROJECT_ROOT` / the constants in
`config.py`. Don't assume the working directory — `main.py` can be run
from `APP/` or the repo root, and paths must still resolve.

## Model changes

If you retrain or swap the model weights, update `MODEL_PATH` in
`config.py` to match the actual committed filename in `model/`. (This
repo currently has a mismatch — `yolo_v1.pt` vs `yolo_v12.pt` — don't
repeat that.)

## Secrets

No API keys or credentials in code or notebooks. The Roboflow key used
for dataset download is read from `os.environ["ROBOFLOW_API_KEY"]`, not
hardcoded — follow the same pattern for anything added later.

## What's intentionally not tracked in git

See `.gitignore`: `.venv/`, `testing_vid/` (sample video),
`reports/cheating_evidence/` and `reports/*.csv` (generated output).
`Sample images/` is tracked on purpose — don't add it to `.gitignore`.

## Style

- PEP 8, standard library + `cv2`/`pandas`/`ultralytics` naming
  conventions.
- Functions over classes unless state genuinely needs to persist across
  calls (the codebase is currently all functions — keep it that way
  unless there's a real reason to change it).

## Testing

There are none yet. If you add logic to `suspicion.py` in particular
(it's pure and easy to unit test), add a test alongside it — it's the
one module in this codebase with no I/O to mock.

## Documentation

Keep `WORKFLOW.txt`/`WORKFLOW.md` in sync with `main.py`'s actual loop
order if the control flow changes. Keep the metrics table in `README.md`
/ `prd.md` pointing at the real validation output from
`Notebook/object_detection.ipynb`, not placeholder numbers.
