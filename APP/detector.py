"""
YOLO model loading and per-frame object detection.
"""

from ultralytics import YOLO

from config import MODEL_PATH, SUSPICIOUS_CLASSES


def load_model():
    return YOLO(MODEL_PATH)


def detect_objects(model, frame):
    """
    Runs YOLO prediction on a single frame.

    Returns:
        result                          - raw YOLO result (used for result.plot())
        obj                              - dict of object counts per class
        highest_suspicious_confidence    - highest confidence among suspicious classes
    """

    results = model.predict(frame, verbose=False)
    result = results[0]

    obj = {
        "book": 0,
        "cell phone": 0,
        "headphone": 0,
        "person": 0
    }

    highest_suspicious_confidence = 0

    for box in result.boxes:

        class_id = int(box.cls[0])
        class_name = result.names[class_id]
        confidence = float(box.conf[0])

        if class_name in obj:
            obj[class_name] += 1

        if class_name in SUSPICIOUS_CLASSES:
            if confidence > highest_suspicious_confidence:
                highest_suspicious_confidence = confidence

    return result, obj, highest_suspicious_confidence
