"""
Central configuration for the exam proctoring pipeline.
All tunable constants live here so nothing is hard-coded inside the
processing modules.
"""

import os

# ============================================================
# PROJECT LAYOUT
# ============================================================

# This file lives in App/, and model/ + reports/ are sibling folders
# to App/ (project_root/App, project_root/model, project_root/reports).
# Resolving from this file's own location means it works no matter
# what directory you run "python main.py" from.

APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_DIR)

MODEL_DIR = os.path.join(PROJECT_ROOT, "model")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")


# ============================================================
# MODEL
# ============================================================

MODEL_PATH = os.path.join(MODEL_DIR, "yolo_v1.pt")


# ============================================================
# PROCESSING SETTINGS
# ============================================================

PROCESS_FPS = 10
FRAME_INTERVAL = 1 / PROCESS_FPS

SUSPICIOUS_THRESHOLD = 30
TOP_N = 5


# ============================================================
# SUSPICIOUS CLASSES
# ============================================================

SUSPICIOUS_CLASSES = {
    "cell phone",
    "book",
    "headphone"
}


# ============================================================
# MODEL CLASSES
# ============================================================

# New 4 classes:
# 0: book
# 1: cell phone
# 2: headphone
# 3: person

CLASS_NAMES = [
    "book",
    "cell phone",
    "headphone",
    "person"
]


# ============================================================
# OUTPUT PATHS
# ============================================================

EVIDENCE_DIR = os.path.join(REPORTS_DIR, "cheating_evidence")
CSV_PATH = os.path.join(REPORTS_DIR, "suspicious_records.csv")
