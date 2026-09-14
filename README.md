# AI Smart Proctoring System

AI-powered exam proctoring using YOLOv8 and OpenCV for suspicious activity
detection, prohibited-object detection, evidence logging, and integrity
reporting.

## Overview

The system watches a webcam feed or a recorded exam video, runs each frame
through a YOLOv8 object-detection model, and applies rule-based suspicion
scoring to flag potential cheating — no face/person in frame, multiple
people in frame, or a prohibited object (book, cell phone, headphone). Once
enough suspicious frames accumulate, it saves a CSV of all suspicious
records plus the top-5 highest-scoring evidence frames as images.

For the full step-by-step breakdown of how a frame moves from capture to
saved evidence, see [`WORKFLOW.txt`](WORKFLOW.txt).

## Sample Detections

<p align="center">
  <img src="Sample%20images/random_10.png" width="480" alt="Random sample of annotated detections"><br>
  <em>Random sample of annotated detections from the validation set</em>
</p>

<p align="center">
  <img src="Sample%20images/image1.png" width="480" alt="Model inference example"><br>
  <em>Model inference on a single frame</em>
</p>

## Model Performance (`best.pt`, validated on held-out data)

| Class | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| book | 0.879 | 0.956 | 0.959 | 0.663 |
| cell phone | 0.902 | 0.946 | 0.933 | 0.525 |
| headphone | 0.825 | 0.856 | 0.850 | 0.377 |
| person | 0.955 | 0.970 | 0.980 | 0.717 |
| **All (mean)** | **0.890** | **0.932** | **0.931** | **0.570** |

Trained: YOLOv8n, 100 epochs, image size 640, batch size 16, on a 4-class
dataset (book, cell phone, headphone, person). Full training log and
validation output are in [`Notebook/object_detection.ipynb`](Notebook/object_detection.ipynb).

## Project Structure

```
AI-Smart-Proctoring-System/
├── APP/
│   ├── config.py            # paths, thresholds, class list
│   ├── video_source.py      # webcam/video capture + frame timing
│   ├── detector.py          # YOLO model loading + per-frame detection
│   ├── suspicion.py         # rule-based suspicion scoring
│   ├── evidence_manager.py  # CSV + evidence frame saving
│   └── main.py               # entry point
├── model/
│   └── yolo_v12.pt           # trained YOLOv8n weights
├── Notebook/
│   └── object_detection.ipynb  # dataset prep, training, evaluation
├── Sample images/             # example annotated/detection images
├── reports/
│   ├── cheating_evidence/     # saved evidence frames (generated)
│   └── suspicious_records.csv # suspicious-frame log (generated)
├── testing_vid/                # sample test video (ignored in git)
├── WORKFLOW.txt                # full pipeline walkthrough
└── README.md
```

## How It Works

1. Choose a source — webcam or a video file.
2. Frames are sampled at a fixed processing rate (`PROCESS_FPS`).
3. Each sampled frame is run through the YOLOv8 model.
4. Suspicion rules check for: no person, multiple people, or a
   suspicious object (book / cell phone / headphone).
5. Suspicious frames are logged; evidence-eligible frames are buffered.
6. Once the suspicious-frame count crosses a threshold, cheating is
   flagged, and the CSV + top evidence frames are written to `reports/`.

See [`WORKFLOW.txt`](WORKFLOW.txt) for the complete diagram and explanation.

## Getting Started

```bash
git clone https://github.com/ENGABHAY/AI-Smart-Proctoring-System.git
cd AI-Smart-Proctoring-System
pip install -r requirements.txt
python APP/main.py
```

You'll be prompted to choose a webcam or a video file. Press `Q` to stop
processing at any time.

## Tech Stack

- Python
- OpenCV
- Ultralytics YOLOv8
- Pandas

## License

See [`LICENSE`](LICENSE).
