"""
AI Exam Proctoring System — entry point.

Run this file directly:
    python main.py

It will prompt you to choose a webcam or video source, then run the
same detection/suspicion/evidence logic as the original notebook,
just split across config.py, video_source.py, detector.py,
suspicion.py and evidence_manager.py.
"""

import os
import cv2

from config import SUSPICIOUS_THRESHOLD, CSV_PATH, PROJECT_ROOT
from video_source import open_source, is_webcam_source, get_frame_timing
from detector import load_model, detect_objects
from suspicion import evaluate_suspicion
from evidence_manager import (
    ensure_evidence_dir,
    save_suspicious_csv,
    save_evidence_frames,
)


def process_source(source, model):

    ensure_evidence_dir()

    cap = open_source(source)

    if cap is None:
        return

    is_webcam = is_webcam_source(source)

    last_process_time = 0
    suspicious_count = 0
    cheating_detected = False

    evidence_frames = []
    data = []

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        # ================================================
        # If cheating already detected
        # ================================================

        if cheating_detected:

            cv2.putText(
                frame,
                "CHEATING DETECTED",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )

            cv2.imshow("Proctoring System", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            continue

        # ================================================
        # PROCESS FPS gate (webcam: real time, video: elapsed time)
        # ================================================

        should_process, last_process_time, frame_time = get_frame_timing(
            is_webcam, cap, last_process_time
        )

        if not should_process:

            if is_webcam:
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            continue

        # ================================================
        # YOLO PREDICTION
        # ================================================

        result, obj, highest_suspicious_confidence = detect_objects(model, frame)

        # ================================================
        # SUSPICION LOGIC
        # ================================================

        suspicious, suspicion_score, evidence_eligible = evaluate_suspicion(
            obj, highest_suspicious_confidence
        )

        # ================================================
        # IF SUSPICIOUS
        # ================================================

        if suspicious:

            suspicious_count += 1

            data.append({"frame_time": frame_time, **obj})

            if evidence_eligible:
                evidence_frames.append((suspicion_score, frame.copy(), frame_time))

            print(
                f"Suspicious time: {frame_time}"
                f" | Suspicious frame: {suspicious_count}/{SUSPICIOUS_THRESHOLD}"
                f" | Score: {suspicion_score:.2f}"
                f" | Objects: {obj}"
                f" | Evidence: {evidence_eligible}"
            )

        # ================================================
        # CHECK SUSPICIOUS RECORDS
        # ================================================

        if suspicious_count >= SUSPICIOUS_THRESHOLD:

            print()
            print("====================================")
            print("       CHEATING DETECTED")
            print("====================================")

            cheating_detected = True

            save_suspicious_csv(data, is_webcam)

            print()
            print("Suspicious records saved:")
            print(os.path.relpath(CSV_PATH, PROJECT_ROOT))

            top_frames = save_evidence_frames(evidence_frames)

            print()
            print(f"Saved top {len(top_frames)} evidence frames.")

        # ================================================
        # DISPLAY
        # ================================================

        annotated_frame = result.plot()

        cv2.imshow("Proctoring System", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # ====================================================
    # RELEASE
    # ====================================================

    cap.release()
    cv2.destroyAllWindows()

    # ====================================================
    # IF VIDEO ENDED BEFORE THRESHOLD
    # ====================================================

    if suspicious_count > 0:

        save_suspicious_csv(data, is_webcam)

        print()
        print("Processing finished.")
        print(f"Total suspicious records: {suspicious_count}")
        print("Suspicious records saved:")
        print(os.path.relpath(CSV_PATH, PROJECT_ROOT))

        save_evidence_frames(evidence_frames)

    else:

        print("No suspicious activity detected.")

    print()
    print("Program stopped.")


def main():

    print()
    print("====================================")
    print("      AI EXAM PROCTORING SYSTEM")
    print("====================================")
    print()

    print("1. Webcam")
    print("2. Video")
    print()

    choice = input("Enter your choice (1/2): ")

    model = load_model()

    if choice == "1":

        print()
        print("Starting webcam...")
        print("Press Q to stop.")
        print()

        process_source(0, model)

    elif choice == "2":

        video_path = input(
            "Enter video path (relative to project root, or full path): "
        )

        if not os.path.isabs(video_path):
            video_path = os.path.join(PROJECT_ROOT, video_path)

        print()
        print("Processing video...")
        print()

        process_source(video_path, model)

    else:

        print("Invalid choice.")


if __name__ == "__main__":
    main()