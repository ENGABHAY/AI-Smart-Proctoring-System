"""
Video/webcam source handling.

Keeps the exact timing logic from the original script:
- Webcam uses real clock time (time.time())
- Video uses the video's own elapsed time (CAP_PROP_POS_MSEC)
"""

import cv2
import time

from config import FRAME_INTERVAL


def open_source(source):
    """
    Opens a webcam (source=0) or a video file (source=path).
    Returns the VideoCapture object, or None if it couldn't be opened.
    """

    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("Could not open source")
        return None

    return cap


def is_webcam_source(source):
    return source == 0


def get_frame_timing(is_webcam, cap, last_process_time):
    """
    Decides whether the current frame should be processed, based on
    PROCESS_FPS, and returns the frame's timestamp string.

    Returns:
        should_process (bool)
        updated_last_process_time (float)
        frame_time (str or None)  - None when should_process is False
    """

    if is_webcam:

        current_time = time.time()

        if current_time - last_process_time < FRAME_INTERVAL:
            return False, last_process_time, None

        last_process_time = current_time
        frame_time = time.strftime("%H:%M:%S")

        return True, last_process_time, frame_time

    else:

        video_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

        if video_time - last_process_time < FRAME_INTERVAL:
            return False, last_process_time, None

        last_process_time = video_time

        total_seconds = int(video_time)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        frame_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        return True, last_process_time, frame_time
