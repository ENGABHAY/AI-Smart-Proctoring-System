# Architecture — AI Smart Proctoring System

## Shape

A single-process Python application. No server, no database, no network
calls at runtime — everything is local: a video source, a model file, and
the local filesystem for output.

```
                 ┌────────────────────┐
  webcam/video → │  video_source.py   │ → frames (FPS-throttled)
                 └────────────────────┘
                           │
                           v
                 ┌────────────────────┐
                 │   detector.py      │  YOLOv8n inference (ultralytics)
                 │   (model/yolo_v12.pt) │ → class counts + confidences
                 └────────────────────┘
                           │
                           v
                 ┌────────────────────┐
                 │   suspicion.py     │  rule-based scoring
                 └────────────────────┘
                           │
                           v
                 ┌────────────────────┐
                 │ evidence_manager.py│ → reports/suspicious_records.csv
                 │                    │ → reports/cheating_evidence/*.jpg
                 └────────────────────┘
```

`main.py` owns the loop and wires the above together; `config.py` is the
single source of truth for paths, thresholds, and the class list — no
module reads an env var or hardcodes a path directly.

## Components

- **`config.py`** — `PROJECT_ROOT`, `MODEL_PATH`, `CSV_PATH`,
  `EVIDENCE_DIR`, `SUSPICIOUS_CLASSES`, `SUSPICIOUS_THRESHOLD` (30),
  `TOP_N` (5), `PROCESS_FPS` (10).
- **`video_source.py`** — opens webcam (index `0`) or a video file with
  OpenCV; `is_webcam_source()` and `get_frame_timing()` decide whether
  frame pacing is driven by wall-clock time (webcam) or the video's own
  timestamp (`CAP_PROP_POS_MSEC`, for files).
- **`detector.py`** — loads the YOLO model once (`load_model()`), runs
  `detect_objects()` per frame, returns per-class counts plus the
  highest confidence among suspicious classes.
- **`suspicion.py`** — `evaluate_suspicion()`: pure function, no I/O.
  Takes detection counts, returns `(suspicious, score, evidence_eligible)`.
- **`evidence_manager.py`** — buffers suspicious records in memory during
  the run; `save_suspicious_csv()` and `save_evidence_frames()` flush to
  disk, the latter keeping only the top `TOP_N` frames by score.
- **`main.py`** — CLI prompt for source selection, the capture/process/
  display loop, and final cleanup/flush on exit.

## Model

YOLOv8n, fine-tuned from COCO-pretrained weights via Ultralytics, trained
in `Notebook/object_detection.ipynb` (100 epochs, imgsz 640, batch 16) on
a Roboflow-sourced dataset reduced from 6 classes to 4 (book, cell phone,
headphone, person — `laptop` and `tv` dropped as not exam-relevant).
Weights are committed at `model/yolo_v12.pt`.

## Storage

Flat files only:
- `reports/suspicious_records.csv` — append-only log of suspicious
  frames.
- `reports/cheating_evidence/` — JPGs of the top-N scoring frames.

No database. For a single-user / single-session tool this is fine; it
would need to change before supporting concurrent exam sessions.

## Known Limitations

- Single camera, single process — not designed for concurrent sessions.
- Model path bug: `config.py` references `yolo_v1.pt`, repo ships
  `yolo_v12.pt`.
- No retry/error handling around model load or camera open failures
  beyond what OpenCV/Ultralytics raise natively.
- No tests.
