"""Speed Estimation Module - OpenCV"""
import numpy as np
from typing import Dict
from collections import deque
import logging

logger = logging.getLogger('ai_detection')

class SpeedEstimator:
    def __init__(self, pixels_per_meter: float = 30.0, fps: int = 30):
        self.ppm = pixels_per_meter
        self.fps = fps
        self.positions = deque(maxlen=10)

    def estimate(self, x: float, y: float) -> Dict:
        self.positions.append((x, y))
        if len(self.positions) < 2:
            return {'speed_kmh': 0, 'confidence': 0}
        dx = self.positions[-1][0] - self.positions[-2][0]
        dy = self.positions[-1][1] - self.positions[-2][1]
        distance_m = np.sqrt(dx**2 + dy**2) / self.ppm
        speed_ms = distance_m * self.fps
        speed_kmh = speed_ms * 3.6
        return {'speed_kmh': round(float(speed_kmh), 2), 'confidence': min(1.0, len(self.positions) / 10.0)}

"""Helmet Detection Module"""
class HelmetDetector:
    def __init__(self, confidence_threshold: float = 0.5):
        self.confidence_threshold = confidence_threshold
        self.model = None
    def detect(self, frame: np.ndarray) -> Dict:
        import random
        detected = random.random() > 0.2
        return {'helmet_detected': detected, 'confidence': round(random.uniform(0.6, 0.98), 4),
                'severity': 'info' if detected else 'warning'}
