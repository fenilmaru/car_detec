"""
Lane Detection Module - OpenCV
Detects lane markings and calculates lane departure.
"""
import numpy as np
import cv2
from typing import Tuple, Dict, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger('ai_detection')

@dataclass
class LaneInfo:
    left_detected: bool
    right_detected: bool
    left_curve: Optional[float]
    right_curve: Optional[float]
    departure_score: float
    lane_center_x: Optional[float]
    vehicle_position: float

class LaneDetector:
    """OpenCV-based lane detection using edge detection and Hough transforms."""

    def __init__(self, roi_vertices: Optional[np.ndarray] = None):
        self.roi_vertices = roi_vertices
        self.low_threshold = 50
        self.high_threshold = 150
        self.canny_aperture = 3
        self.hough_threshold = 50
        self.min_line_length = 100
        self.max_line_gap = 10

    def detect(self, frame: np.ndarray) -> Dict:
        """Detect lanes in a frame."""
        h, w = frame.shape[:2]

        # Define ROI if not set
        if self.roi_vertices is None:
            self.roi_vertices = np.array([[(0, h), (w * 0.45, h * 0.6),
                                           (w * 0.55, h * 0.6), (w, h)]], dtype=np.int32)

        # Preprocess
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # ROI mask
        mask = np.zeros_like(gray)
        cv2.fillPoly(mask, self.roi_vertices, 255)
        masked = cv2.bitwise_and(blurred, mask)

        # Canny edge detection
        edges = cv2.Canny(masked, self.low_threshold, self.high_threshold, apertureSize=self.canny_aperture)

        # Hough lines
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, self.hough_threshold,
                                minLineLength=self.min_line_length, maxLineGap=self.max_line_gap)

        if lines is None:
            return {'lane_detected': False, 'departure': 0.0, 'confidence': 0.0}

        # Separate left and right lanes
        left_lines, right_lines = [], []
        center_x = w // 2

        for line in lines:
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1 + 1e-6)
            if slope < -0.3:
                left_lines.append((x1, y1, x2, y2, slope))
            elif slope > 0.3:
                right_lines.append((x1, y1, x2, y2, slope))

        left_detected = len(left_lines) > 0
        right_detected = len(right_lines) > 0

        # Calculate departure
        departure = 0.0
        if left_detected and right_detected:
            left_avg_x = np.mean([l[0] for l in left_lines])
            right_avg_x = np.mean([l[0] for l in right_lines])
            lane_center = (left_avg_x + right_avg_x) / 2
            departure = abs(lane_center - center_x) / center_x
        elif left_detected:
            left_avg_x = np.mean([l[0] for l in left_lines])
            departure = abs(left_avg_x * 2 - center_x) / center_x
        elif right_detected:
            right_avg_x = np.mean([l[0] for l in right_lines])
            departure = abs(right_avg_x * 2 - center_x) / center_x

        confidence = min(1.0, (len(left_lines) + len(right_lines)) / 10.0)

        return {
            'lane_detected': left_detected or right_detected,
            'left_detected': left_detected,
            'right_detected': right_detected,
            'departure': round(float(departure), 4),
            'confidence': round(float(confidence), 4),
            'line_count': len(lines),
        }

    def draw_lanes(self, frame: np.ndarray, result: Dict) -> np.ndarray:
        """Draw detected lanes on frame."""
        overlay = frame.copy()
        if result.get('lane_detected'):
            cv2.putText(overlay, f"Departure: {result.get('departure', 0):.2%}",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        return overlay
