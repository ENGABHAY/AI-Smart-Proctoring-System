"""
Rule-based suspicion scoring.

Same three conditions as the original script:
  1. No person in frame           -> suspicious, not evidence
  2. Multiple persons in frame    -> suspicious, evidence
  3. Suspicious object detected   -> suspicious, evidence
"""


def evaluate_suspicion(obj, highest_suspicious_confidence):
    """
    Returns:
        suspicious (bool)
        suspicion_score (float)
        evidence_eligible (bool)
    """

    person_count = obj["person"]

    suspicious = False
    suspicion_score = 0
    evidence_eligible = False

    # Condition 1: No person
    if person_count == 0:
        suspicious = True
        suspicion_score = 0.90
        evidence_eligible = False

    # Condition 2: Multiple persons
    if person_count > 1:
        suspicious = True
        suspicion_score = max(suspicion_score, 0.95)
        evidence_eligible = True

    # Condition 3: Suspicious object
    if highest_suspicious_confidence > 0:
        suspicious = True
        suspicion_score = max(suspicion_score, highest_suspicious_confidence)
        evidence_eligible = True

    return suspicious, suspicion_score, evidence_eligible
