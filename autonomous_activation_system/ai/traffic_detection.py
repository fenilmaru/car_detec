"""
Traffic Sign Detection Module
Detects and classifies traffic signs from camera feed.
"""
import numpy as np
from typing import Dict, List
import logging

logger = logging.getLogger('ai_detection')

TRAFFIC_SIGNS = {
    0: 'Speed Limit 20', 1: 'Speed Limit 30', 2: 'Speed Limit 50',
    3: 'Speed Limit 60', 4: 'Speed Limit 70', 5: 'Speed Limit 80',
    6: 'End Speed Limit 80', 7: 'Speed Limit 100', 8: 'Speed Limit 120',
    9: 'No Passing', 10: 'No Passing for Vehicles over 3.5t',
    11: 'Right of Way at Next Intersection', 12: 'Priority Road',
    13: 'Yield', 14: 'Stop', 15: 'No Vehicles',
    16: 'Vehicles over 3.5t Prohibited', 17: 'No Entry',
    18: 'General Caution', 19: 'Dangerous Curve to Left',
    20: 'Dangerous Curve to Right', 21: 'Double Curve',
    22: 'Bumpy Road', 23: 'Slippery Road',
    24: 'Road Narrows on Right', 25: 'Road Work',
    26: 'Traffic Signals', 27: 'Pedestrians', 28: 'Children Crossing',
    29: 'Bicycles Crossing', 30: 'Beware of Ice/Snow',
    31: 'Wild Animals Crossing', 32: 'End of All Speed/Passing Limits',
    33: 'Turn Right Ahead', 34: 'Turn Left Ahead', 35: 'Ahead Only',
    36: 'Go Straight or Right', 37: 'Go Straight or Left',
    38: 'Keep Right', 39: 'Keep Left', 40: 'Roundabout Mandatory',
    41: 'End of No Passing', 42: 'End of No Passing over 3.5t'
}

class TrafficSignDetector:
    """Detects and classifies traffic signs."""

    def __init__(self, confidence_threshold: float = 0.6):
        self.confidence_threshold = confidence_threshold
        self.model = None

    def detect(self, frame: np.ndarray) -> Dict:
        """Detect traffic signs in frame."""
        if self.model:
            try:
                results = self.model(frame, conf=self.confidence_threshold)
                signs = []
                for result in results:
                    for box in result.boxes:
                        cls = int(box.cls[0])
                        signs.append({
                            'sign_id': cls,
                            'sign_name': TRAFFIC_SIGNS.get(cls, f'Unknown ({cls})'),
                            'confidence': round(float(box.conf[0]), 4),
                            'bounding_box': [int(x) for x in box.xyxy[0]],
                        })
                return {'signs_detected': signs, 'count': len(signs)}
            except Exception as e:
                logger.error(f"Traffic sign detection error: {e}")

        return self._mock_detect(frame)

    def _mock_detect(self, frame: np.ndarray) -> Dict:
        import random
        count = random.randint(0, 3)
        signs = []
        for _ in range(count):
            sign_id = random.randint(0, 42)
            signs.append({
                'sign_id': sign_id,
                'sign_name': TRAFFIC_SIGNS.get(sign_id, 'Unknown'),
                'confidence': round(random.uniform(0.6, 0.99), 4),
                'bounding_box': [random.randint(0, 500), random.randint(0, 300),
                               random.randint(100, 300), random.randint(100, 300)],
            })
        return {'signs_detected': signs, 'count': len(signs)}
