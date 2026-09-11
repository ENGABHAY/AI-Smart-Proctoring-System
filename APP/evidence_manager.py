"""
Handles persisting outputs: the suspicious-records CSV and the
top-N evidence frame images.
"""

import os
import cv2
import pandas as pd

from config import EVIDENCE_DIR, CSV_PATH, TOP_N, PROJECT_ROOT


def ensure_evidence_dir():
    os.makedirs(EVIDENCE_DIR, exist_ok=True)


def save_suspicious_csv(data, is_webcam):
    """
    Builds the suspicious-records DataFrame and writes it to CSV_PATH.

    `data` is a list of dicts, one per suspicious frame, each containing
    "frame_time" plus the object counts. Using a list (instead of a dict
    keyed by frame_time) means two suspicious frames landing in the same
    second no longer overwrite each other - every suspicious frame gets
    its own row.

    Returns the DataFrame.
    """

    df = pd.DataFrame(data)

    df = df.set_index("frame_time")

    df.index.name = "webcam_time" if is_webcam else "video_time"

    df = df[["book", "cell phone", "headphone", "person"]]

    df.to_csv(CSV_PATH)

    return df


def save_evidence_frames(evidence_frames):
    """
    Sorts evidence frames by suspicion score (highest first), saves the
    top TOP_N as JPEGs in EVIDENCE_DIR, and returns the saved subset.
    """

    evidence_frames.sort(key=lambda x: x[0], reverse=True)

    top_frames = evidence_frames[:TOP_N]

    for i, (score, evidence_frame, evidence_time) in enumerate(top_frames, start=1):

        filename = os.path.join(
            EVIDENCE_DIR,
            f"evidence_{i}_"
            f"time_{evidence_time.replace(':', '-')}_"
            f"score_{score:.2f}.jpg"
        )

        cv2.imwrite(filename, evidence_frame)

        display_path = os.path.relpath(filename, PROJECT_ROOT)

        print(f"Saved evidence: {display_path}")

    return top_frames