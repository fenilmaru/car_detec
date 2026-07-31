"""Drowsiness Detection Module - MediaPipe + OpenCV
Detects driver drowsiness using eye aspect ratio (EAR) and head pose.
"""
import numpy as np
import cv2
from typing import Dict, Optional
from dataclasses import dataclass
from collections import deque
import logging

logger = logging.getLogger('ai_detection')

@dataclass
class DrowsinessResult:
    is_drowsy: bool
    eye_aspect_ratio: float
    blink_count: int
    consecutive_blinks: int
    yawn_detected: bool
    head_tilt: float
    confidence: float

class DrowsinessDetector:
    """Detects drowsiness using eye aspect ratio and blink frequency."""

    EYE_AR_THRESH = 0.25
    EYE_AR_CONSEC_FRAMES = 3
    YAWN_THRESH = 0.6
    BLINK_WINDOW = 30  # frames

    def __init__(self):
        self.blink_counter = 0
        self.total_blinks = 0
        self.frame_counter = 0
        self.blink_history = deque(maxlen=self.BLINK_WINDOW)
        self.consecutive_drowsy = 0

        # Try loading MediaPipe
        self.mp_face = None
        try:
            import mediapipe as mp
            self.mp_face = mp.solutions.face_mesh.FaceMesh(
                static_image_mode=False, max_num_faces=1,
                min_detection_confidence=0.5, min_tracking_confidence=0.5)
            logger.info("MediaPipe FaceMesh loaded")
        except ImportError:
            logger.warning("MediaPipe not installed, using basic detection")

    def detect(self, frame: np.ndarray) -> Dict:
        """Detect drowsiness from face frame."""
        h, w = frame.shape[:2]
        ear = 0.3
        yawn_detected = False
        head_tilt = 0.0

        if self.mp_face:
            try:
                import mediapipe as mp
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.mp_face.process(rgb)

                if results.multi_face_landmarks:
                    landmarks = results.multi_face_landmarks[0].landmark

                    # Calculate EAR from eye landmarks
                    left_eye = self._get_ear(landmarks, [(33, 160), (133, 159), (153, 145), (144, 153)])
                    right_eye = self._get_ear(landmarks, [(362, 385), (263, 374), (380, 373), (373, 380)])
                    ear = (left_eye + right_eye) / 2.0

                    # Yawn detection
                    mouth_open = self._calculate_mouth_opening(landmarks)
                    yawn_detected = mouth_open > self.YAWN_THRESH

                    # Head tilt
                    head_tilt = self._calculate_head_tilt(landmarks)
            except Exception as e:
                logger.error(f"MediaPipe error: {e}")

        # Blink detection
        if ear < self.EYE_AR_THRESH:
            self.frame_counter += 1
            if self.frame_counter >= self.EYE_AR_CONSEC_FRAMES:
                self.total_blinks += 1
                self.blink_history.append(1)
                self.frame_counter = 0
        else:
            self.frame_counter = 0
            self.blink_history.append(0)

        # Drowsiness logic
        blink_rate = sum(self.blink_history) / len(self.blink_history) if self.blink_history else 0
        is_drowsy = (ear < self.EAR_THRESH * 0.8) or (blink_rate > 0.5) or yawn_detected

        if is_drowsy:
            self.consecutive_drowsy += 1
        else:
            self.consecutive_drowsy = max(0, self.consecutive_drowsy - 1)

        confidence = min(1.0, self.consecutive_drowsy / 10.0) if is_drowsy else max(0, 1.0 - confidence)

        return {
            'is_drowsy': is_drowsy,
            'ear': round(float(ear), 4),
            'blink_count': self.total_blinks,
            'consecutive_drowsy': self.consecutive_drowsy,
            'yawn_detected': yawn_detected,
            'head_tilt': round(float(head_tilt), 4),
            'confidence': round(float(confidence), 4),
        }

    def _get_ear(self, landmarks, eye_indices):
        """Calculate Eye Aspect Ratio."""
        def dist(p1, p2):
            return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

        v1 = dist(landmarks[eye_indices[0][0]], landmarks[eye_indices[0][1]])
        v2 = dist(landmarks[eye_indices[1][0]], landmarks[eye_indices[1][1]])
        h = dist(landmarks[eye_indices[2][0]], landmarks[eye_indices[2][1]])
        return (v1 + v2) / (2.0 * h + 1e-6)

    def _calculate_mouth_opening(self, landmarks):
        def dist(p1, p2):
            return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
        return dist(landmarks[13], landmarks[14])

    def _calculate_head_tilt(self, landmarks):
        return abs(landmarks[1].y - landmarks[199].y)
