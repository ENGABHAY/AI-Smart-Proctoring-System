# Tasks — AI Smart Proctoring System

## Done

- [x] Pulled and annotated dataset via Roboflow (6 classes).
- [x] Reduced dataset to 4 exam-relevant classes (book, cell phone,
      headphone, person) with remapped labels + regenerated `data.yaml`.
- [x] Trained YOLOv8n (100 epochs, imgsz 640, batch 16); validated —
      mAP50 0.931 overall.
- [x] Refactored the notebook's inline logic into `APP/` modules
      (`config.py`, `video_source.py`, `detector.py`, `suspicion.py`,
      `evidence_manager.py`, `main.py`).
- [x] Rule-based suspicion scoring (no person / multiple people /
      prohibited object).
- [x] CSV logging + top-N evidence frame saving.
- [x] Notebook cleaned up with professional markdown documentation
      (outputs preserved).
- [x] `.gitignore` (ignores `.venv/`, `testing_vid/`,
      `reports/cheating_evidence/`, `reports/*.csv`; keeps
      `Sample images/` tracked).
- [x] `README.md` with sample detection images, metrics table, workflow
      link, project structure, quick-start.
- [x] `requirements.txt` (core app deps + notebook-only deps split out).
- [x] `WORKFLOW.md` / `WORKFLOW.txt` — full capture-to-evidence pipeline
      breakdown with diagram.

## Open

- [ ] **Fix `config.py` model path bug** — `MODEL_PATH` points to
      `yolo_v1.pt`, repo ships `yolo_v12.pt`. Breaks `load_model()` on a
      fresh checkout. Flagged repeatedly, not yet applied.
- [ ] Add automated tests, starting with `suspicion.py` (pure function,
      easiest to cover).
- [ ] Improve `headphone` class performance (weakest class, mAP50-95
      0.377) — more training images or augmentation.
- [ ] Decide whether evidence/CSV output needs a simple review UI, or
      stays file-based.
- [ ] Add inference-speed/hardware note to README (CPU vs GPU
      expectations) once benchmarked.

## Not planned (explicitly out of scope for now)

- Live alerting during an exam.
- Multi-camera / multi-session support.
- Face/identity verification.
- LMS integration.
