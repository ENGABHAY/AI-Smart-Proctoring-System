# Design — AI Smart Proctoring System

## Interaction model

A CLI prompt at startup (webcam vs. video path), then a single OpenCV
window that shows the live annotated feed until the source ends or the
user presses `Q`. No GUI beyond that — this is a processing tool, not a
monitoring dashboard.

## On-screen overlay

- Bounding boxes drawn per detection (standard YOLO annotation via
  Ultralytics' plotting).
- A `"CHEATING DETECTED"` banner is overlaid once the session crosses
  `SUSPICIOUS_THRESHOLD` — once shown, remaining frames in that session
  skip further detection/scoring (no point re-flagging what's already
  flagged) and just keep displaying the banner.

## Suspicion scoring design

Three independent rules, each can trigger a flag on its own — deliberately
simple and explainable rather than a learned classifier, so a human
reviewing evidence can see exactly why a frame was flagged:

| Condition | Score | Saved as evidence? |
|---|---|---|
| No person visible | 0.90 | No — an empty frame isn't useful evidence |
| More than one person visible | 0.95 | Yes |
| Prohibited object detected | = detection confidence | Yes |

The "no person" case is logged (so a gap in attendance shows up in the
CSV) but doesn't produce an evidence image, since there's nothing visual
to show. The other two do, because the frame itself is the proof.

## Evidence selection

Rather than saving every suspicious frame (which would flood
`reports/cheating_evidence/` on a long exam), only the top `TOP_N` (5)
highest-scoring eligible frames are kept, chosen after the session ends.
This keeps the evidence folder reviewable — five best shots, not
hundreds of near-duplicates.

## Why 4 classes, not 6

The source dataset had 6 classes (book, cell phone, headphone, laptop,
person, tv). `laptop` and `tv` were dropped — in a typical exam setup
either is either expected equipment (not suspicious) or not something
the model can reliably attribute to the candidate vs. the room. Keeping
only exam-relevant classes also meant less training signal spent on
classes that don't map to a scoring rule.

## Frame-rate throttling

Running YOLO on every single frame is wasteful for this use case —
nothing meaningfully changes frame-to-frame at 30fps for exam
monitoring. `PROCESS_FPS` (10) caps how often detection actually runs;
`get_frame_timing()` uses wall-clock time for a live webcam and the
video's own internal timestamp for a file, so playback speed doesn't
affect scoring consistency.

## Explicitly not designed yet

- A review UI for the saved evidence (currently: open the CSV and the
  JPGs directly).
- Any live/real-time alert to an invigilator.
- Per-candidate session separation if multiple exams are processed.
