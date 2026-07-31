"""Accident Detection Module
Detects accidents from impact forces, sudden speed changes, and visual cues.
"""
import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
from collections import deque
import logging

logger = logging.getLogger('ai_detection')

class AccidentDetector:
    """Multi-modal accident detection combining IMU data and visual analysis."""

    ACCELERATION_THRESHOLD = 2.5  # g-force
    SPEED_DROP_THRESHOLD = 30  # km/h drop in 1 second
    ROTATION_THRESHOLD = 45  # degrees

    def __init__(self, window_size: int = 30):
        self.accel_history = deque(maxlen=window_size)
        self.speed_history = deque(maxlen=window_size)
        self.rotation_history = deque(maxlen=window_size)

    def analyze_imu(self, accel_x: float, accel_y: float, accel_z: float,
                    speed: float, gyro_x: float, gyro_y: float, gyro_z: float) -> Dict:
        """Analyze IMU sensor data for accident indicators."""
        total_accel = np.sqrt(accel_x**2 + accel_y**2 + accel_z**2)
        self.accel_history.append(total_accel)
        self.speed_history.append(speed)
        total_rotation = np.sqrt(gyro_x**2 + gyro_y**2 + gyro_z**2)
        self.rotation_history.append(total_rotation)

        # Check for sudden deceleration
        if len(self.speed_history) >= 2:
            speed_drop = self.speed_history[-2] - self.speed_history[-1]
        else:
            speed_drop = 0

        # Check for high impact
        if len(self.accel_history) >= 2:
            accel_change = abs(self.accel_history[-1] - self.accel_history[-2])
        else:
            accel_change = 0

        # Check for sudden rotation (rollover)
        if len(self.rotation_history) >= 2:
            rotation_change = abs(self.rotation_history[-1] - self.rotation_history[-2])
        else:
            rotation_change = 0

        accident_detected = (accel_change > self.ACCELERATION_THRESHOLD or
                           speed_drop > self.SPEED_DROP_THRESHOLD or
                           rotation_change > self.ROTATION_THRESHOLD)

        severity = 'minor'
        if accident_detected:
            impact_score = (accel_change / self.ACCELERATION_THRESHOLD +
                          speed_drop / self.SPEED_DROP_THRESHOLD +
                          rotation_change / self.ROTATION_THRESHOLD) / 3
            if impact_score > 2.5:
                severity = 'critical'
            elif impact_score > 1.8:
                severity = 'severe'
            elif impact_score > 1.2:
                severity = 'moderate'

        return {
            'accident_detected': accident_detected,
            'severity': severity,
            'g_force': round(float(total_accel), 4),
            'speed_drop': round(float(speed_drop), 2),
            'rotation': round(float(total_rotation), 4),
            'impact_score': round(float(impact_score if accident_detected else 0), 4),
        }

    def analyze_visual(self, detections: List[Dict], frame: Optional = None) -> Dict:
        """Analyze visual data for accident indicators."""
        # Look for collision indicators in detection data
        collision_detected = False
        for det in detections:
            if det.get('class_name') in ['car', 'truck', 'person'] and det.get('confidence', 0) > 0.8:
                bbox = det.get('bounding_box', [])
                if len(bbox) >= 4:
                    # Large object very close (occupies significant frame)
                    frame_area_ratio = (bbox[2] * bbox[3]) / (1920 * 1080)
                    if frame_area_ratio > 0.4:
                        collision_detected = True
                        break

        return {
            'visual_collision': collision_detected,
        }
