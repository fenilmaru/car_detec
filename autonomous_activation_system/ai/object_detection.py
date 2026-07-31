"""
AI Object Detection Module - YOLOv11 + OpenCV
Detects vehicles, pedestrians, obstacles, traffic objects.
"""
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger('ai_detection')

@dataclass
class Detection:
    class_id: int
    class_name: str
    confidence: float
    bounding_box: Tuple[int, int, int, int]  # x, y, w, h
    metadata: Dict = None

    def to_dict(self):
        return asdict(self)

class ObjectDetector:
    """YOLOv11-based object detector for vehicles and road objects."""

    # COCO classes relevant for vehicle safety
    CLASSES = {
        0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane',
        5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic_light',
        10: 'fire_hydrant', 13: 'stop_sign', 14: 'parking_meter',
        15: 'bench', 16: 'bird', 17: 'cat', 18: 'dog', 19: 'horse',
        20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear', 24: 'zebra',
        25: 'giraffe', 27: 'backpack', 28: 'umbrella',
        31: 'handbag', 32: 'tie', 33: 'suitcase', 34: 'frisbee',
        35: 'skis', 36: 'snowboard', 37: 'sports_ball', 38: 'kite',
        39: 'baseball_bat', 40: 'baseball_glove', 41: 'skateboard',
        42: 'surfboard', 43: 'tennis_racket', 44: 'bottle',
        46: 'wine_glass', 47: 'cup', 48: 'fork', 49: 'knife',
        50: 'spoon', 51: 'bowl', 52: 'banana', 53: 'apple',
        54: 'sandwich', 55: 'orange', 56: 'broccoli', 57: 'carrot',
        58: 'hot_dog', 59: 'pizza', 60: 'donut', 61: 'cake',
        62: 'chair', 63: 'couch', 64: 'potted_plant', 65: 'bed',
        67: 'dining_table', 70: 'toilet', 72: 'tv', 73: 'laptop',
        74: 'mouse', 75: 'remote', 76: 'keyboard', 77: 'cell_phone',
        78: 'microwave', 79: 'oven', 80: 'toaster', 81: 'sink',
        82: 'refrigerator', 84: 'book', 85: 'clock', 86: 'vase',
        87: 'scissors', 88: 'teddy_bear', 89: 'hair_drier', 90: 'toothbrush'
    }

    def __init__(self, model_path: str = None, confidence_threshold: float = 0.5):
        self.confidence_threshold = confidence_threshold
        self.model = None
        self._load_model(model_path)

    def _load_model(self, model_path: Optional[str]):
        """Load YOLOv11 model."""
        try:
            import ultralytics
            if model_path:
                self.model = ultralytics.YOLO(model_path)
            else:
                self.model = ultralytics.YOLO('yolo11n.pt')
            logger.info(f"YOLOv11 model loaded: {model_path or 'yolo11n.pt'}")
        except ImportError:
            logger.warning("ultralytics not installed, using mock detector")
            self.model = None
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            self.model = None

    def detect(self, frame: np.ndarray) -> List[Dict]:
        """Run detection on a frame."""
        if self.model is None:
            return self._mock_detect(frame)

        try:
            results = self.model(frame, conf=self.confidence_threshold)
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        conf = float(box.conf[0])
                        cls_id = int(box.cls[0])
                        detections.append({
                            'class_id': cls_id,
                            'class_name': self.CLASSES.get(cls_id, 'unknown'),
                            'confidence': round(conf, 4),
                            'bounding_box': [x1, y1, x2 - x1, y2 - y1],
                            'metadata': {}
                        })
            return detections
        except Exception as e:
            logger.error(f"Detection error: {e}")
            return []

    def _mock_detect(self, frame: np.ndarray) -> List[Dict]:
        """Mock detection for testing."""
        import random
        h, w = frame.shape[:2]
        count = random.randint(0, 5)
        detections = []
        for _ in range(count):
            cls = random.choice([2, 3, 0, 1])
            detections.append({
                'class_id': cls,
                'class_name': self.CLASSES.get(cls, 'unknown'),
                'confidence': round(random.uniform(0.5, 0.99), 4),
                'bounding_box': [random.randint(0, w//2), random.randint(0, h//2),
                               random.randint(50, 200), random.randint(50, 200)],
                'metadata': {}
            })
        return detections

    def get_critical_detections(self, detections: List[Dict]) -> List[Dict]:
        """Filter for critical safety objects."""
        critical_classes = ['person', 'car', 'truck', 'bus', 'motorcycle', 'bicycle']
        return [d for d in detections if d['class_name'] in critical_classes]
