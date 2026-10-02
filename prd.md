# PRD — AI Smart Proctoring System

## Problem

Online/remote exams have no automated way to flag suspicious behavior —
someone leaving the frame, a second person stepping in, or a prohibited
item (phone, book, headphone) in view. A human invigilator watching every
feed live doesn't scale.

## Goal

Watch a webcam or recorded exam video, detect prohibited objects and
people in each frame, apply simple rule-based suspicion scoring, and
produce an evidence trail (CSV log + saved frames) an invigilator can
review after the fact — without needing live human monitoring of every
candidate.

## Users

Instructors / exam invigilators reviewing flagged sessions after an exam,
not during it (no live alerting is built).

## Functional Requirements

- Choose input source: webcam or a video file.
- Run object detection on sampled frames (book, cell phone, headphone,
  person).
- Flag a frame as suspicious when:
  - no person is visible,
  - more than one person is visible, or
  - a prohibited object is detected.
- Overlay detection boxes and a "CHEATING DETECTED" banner once a session
  crosses the suspicion threshold.
- Log every suspicious frame (timestamp + object counts) to
  `reports/suspicious_records.csv`.
- Save the top-N highest-confidence evidence frames as JPGs to
  `reports/cheating_evidence/`.

## Non-Functional Requirements

- Must run on a single consumer machine (no GPU required — YOLOv8n is
  CPU-viable, just slower).
- Config-driven: thresholds, paths, FPS, and class list live in
  `APP/config.py`, not hardcoded in logic.
- No external services at runtime (model is local; Roboflow is only used
  once, at dataset-build time in the notebook).

## Out of Scope (current version)

- Identity verification / face recognition.
- Audio analysis.
- Live alerting to an invigilator during the exam.
- Multi-camera support.
- A review dashboard — evidence is just files on disk today.
- LMS/exam-platform integration.

## Success Metrics

Model quality on the held-out validation set (`best.pt`, YOLOv8n, 4
classes):

| Class | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| book | 0.879 | 0.956 | 0.959 | 0.663 |
| cell phone | 0.902 | 0.946 | 0.933 | 0.525 |
| headphone | 0.825 | 0.856 | 0.850 | 0.377 |
| person | 0.955 | 0.970 | 0.980 | 0.717 |
| **All (mean)** | **0.890** | **0.932** | **0.931** | **0.570** |

`headphone` is the weakest class (mAP50-95 0.377) — worth more training
data or augmentation if this moves past a portfolio project.

## Known Gaps

- `config.py` currently points `MODEL_PATH` at `model/yolo_v1.pt`, but the
  committed weights file is `model/yolo_v12.pt` — breaks on a fresh
  checkout until fixed.
- No automated tests.
- Suspicion scoring is fixed rules, not learned/tunable per deployment.
