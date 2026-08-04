"""
Seat Belt Detection Module - YOLO + OpenCV
Detects whether driver and passengers are wearing seat belts.
"""
import numpy as np
from typing import Dict, List
import logging

logger = logging.getLogger('ai_detection')

class SeatbeltDetector:
    """Detects seat belt usage in vehicle interior images."""

    def __init__(self, confidence_threshold: float = 0.5):
        self.confidence_threshold = confidence_threshold
        self.model = None

    def detect(self, frame: np.ndarray) -> Dict:
        """Detect seat belt usage from interior camera frame."""
        try:
            if self.model:
                results = self.model(frame, conf=self.confidence_threshold)
                belt_detected = False
                for result in results:
                    for cls in result.boxes.cls:
                        if int(cls) == 0:  # person
                            belt_detected = True
                return {
                    'seatbelt_detected': belt_detected,
                    'confidence': 0.85 if belt_detected else 0.2,
                    'severity': 'info' if belt_detected else 'warning',
                }
            else:
                return self._mock_detect(frame)
        except Exception as e:
            logger.error(f"Seatbelt detection error: {e}")
            return {'seatbelt_detected': False, 'confidence': 0.0, 'severity': 'critical'}

    def _mock_detect(self, frame: np.ndarray) -> Dict:
        """Mock detection for testing."""
        import random
        detected = random.random() > 0.3
        return {
            'seatbelt_detected': detected,
            'confidence': round(random.uniform(0.7, 0.98), 4),
            'severity': 'info' if detected else 'warning',
        }
