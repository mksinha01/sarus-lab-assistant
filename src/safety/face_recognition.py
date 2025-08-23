"""
👤 FACE RECOGNITION - Security Feature
User authentication and access control system

Recognizes authorized users and provides security monitoring
for lab access control.
"""

import asyncio
import logging
import cv2
import face_recognition
import numpy as np
import pickle
import time
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

@dataclass
class RecognitionResult:
    """Face recognition result data"""
    user_id: Optional[str]
    confidence: float
    timestamp: datetime
    authorized: bool
    face_location: Tuple[int, int, int, int]

class FaceRecognition:
    """
    🔐 Face Recognition and Access Control System
    
    Features:
    - User enrollment and recognition
    - Authorized access control
    - Intruder detection and alerts
    - Real-time face tracking
    """
    
    def __init__(self, config, alert_callback: Optional[Callable] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.alert_callback = alert_callback
        
        # Recognition settings
        self.confidence_threshold = 0.6
        self.unknown_face_threshold = 5  # Consecutive unknown faces before alert
        
        # State tracking
        self.known_encodings: List[np.ndarray] = []
        self.known_names: List[str] = []
        self.is_monitoring = False
        self.camera = None
        self.last_recognition: Optional[RecognitionResult] = None
        
        # Security tracking
        self.unknown_face_count = 0
        self.last_unknown_time = 0
        self.access_log: List[Dict] = []
        
        # Paths
        self.encodings_file = Path(config.data_dir) / "face_encodings" / "known_faces.pkl"
        self.faces_dir = Path(config.data_dir) / "face_encodings"
        
        # Ensure directories exist
        self.faces_dir.mkdir(parents=True, exist_ok=True)
        
        # Load known faces
        self._load_known_faces()
        
        self.logger.info("Face Recognition system initialized")
    
    async def start_monitoring(self):
        """Start face recognition monitoring"""
        try:
            self.is_monitoring = True
            
            # Initialize camera
            if not self.config.simulation_mode:
                self.camera = cv2.VideoCapture(0)
                if not self.camera.isOpened():
                    raise Exception("Could not open camera")
            
            self.logger.info("Face recognition monitoring started")
            
            # Start monitoring loop
            asyncio.create_task(self._monitoring_loop())
            
        except Exception as e:
            self.logger.error(f"Failed to start face recognition: {e}")
            self.is_monitoring = False
    
    async def stop_monitoring(self):
        """Stop face recognition monitoring"""
        self.is_monitoring = False
        
        if self.camera:
            self.camera.release()
            self.camera = None
        
        self.logger.info("Face recognition monitoring stopped")
    
    async def _monitoring_loop(self):
        """Main face recognition monitoring loop"""
        while self.is_monitoring:
            try:
                if self.config.simulation_mode:
                    # Simulate face recognition for testing
                    await self._simulate_recognition()
                else:
                    # Real camera-based recognition
                    await self._process_camera_frame()
                
                await asyncio.sleep(0.5)  # Process 2 frames per second
                
            except Exception as e:
                self.logger.error(f"Error in face recognition loop: {e}")
                await asyncio.sleep(1.0)
    
    async def _simulate_recognition(self):
        """Simulate face recognition for development"""
        import random
        
        # Occasionally simulate different recognition scenarios
        scenario = random.random()
        
        if scenario < 0.7:  # 70% known user
            user_id = random.choice(self.known_names) if self.known_names else "admin"
            confidence = random.uniform(0.7, 0.95)
            authorized = True
        elif scenario < 0.9:  # 20% unknown user
            user_id = None
            confidence = random.uniform(0.3, 0.6)
            authorized = False
        else:  # 10% no face detected
            return
        
        result = RecognitionResult(
            user_id=user_id,
            confidence=confidence,
            timestamp=datetime.now(),
            authorized=authorized,
            face_location=(100, 200, 300, 400)  # Mock location
        )
        
        await self._process_recognition_result(result)
    
    async def _process_camera_frame(self):
        """Process camera frame for face recognition"""
        if not self.camera:
            return
        
        ret, frame = self.camera.read()
        if not ret:
            return
        
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]  # BGR to RGB
        
        # Find faces in current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Scale back up face locations
            scaled_location = tuple(coord * 4 for coord in face_location)
            
            # Compare with known faces
            result = self._recognize_face(face_encoding, scaled_location)
            await self._process_recognition_result(result)
    
    def _recognize_face(self, face_encoding: np.ndarray, face_location: Tuple[int, int, int, int]) -> RecognitionResult:
        """Recognize a face encoding against known faces"""
        user_id = None
        confidence = 0.0
        authorized = False
        
        if len(self.known_encodings) > 0:
            # Compare with known faces
            matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
            face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
            
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    confidence = 1.0 - face_distances[best_match_index]
                    
                    if confidence >= self.confidence_threshold:
                        user_id = self.known_names[best_match_index]
                        authorized = True
        
        return RecognitionResult(
            user_id=user_id,
            confidence=confidence,
            timestamp=datetime.now(),
            authorized=authorized,
            face_location=face_location
        )
    
    async def _process_recognition_result(self, result: RecognitionResult):
        """Process recognition result and handle security"""
        self.last_recognition = result
        
        # Log access attempt
        access_entry = {
            'timestamp': result.timestamp.isoformat(),
            'user_id': result.user_id,
            'authorized': result.authorized,
            'confidence': result.confidence
        }
        self.access_log.append(access_entry)
        
        if result.authorized:
            # Reset unknown face counter
            self.unknown_face_count = 0
            
            self.logger.info(f"Authorized user recognized: {result.user_id} (confidence: {result.confidence:.2f})")
            
            if self.alert_callback:
                await self.alert_callback({
                    'type': 'authorized_access',
                    'severity': 'info',
                    'user_id': result.user_id,
                    'confidence': result.confidence,
                    'timestamp': result.timestamp
                })
        else:
            # Handle unknown/unauthorized face
            self.unknown_face_count += 1
            current_time = time.time()
            
            self.logger.warning(f"Unknown face detected (count: {self.unknown_face_count})")
            
            # Trigger security alert if too many unknown faces
            if (self.unknown_face_count >= self.unknown_face_threshold and 
                current_time - self.last_unknown_time > 30):  # Max one alert per 30 seconds
                
                await self._trigger_security_alert(result)
                self.last_unknown_time = current_time
                self.unknown_face_count = 0
    
    async def _trigger_security_alert(self, result: RecognitionResult):
        """Trigger security alert for unauthorized access"""
        alert_message = (
            f"🚨 SECURITY ALERT! 🚨\n"
            f"Unauthorized person detected!\n"
            f"Time: {result.timestamp.strftime('%H:%M:%S')}\n"
            f"Multiple unknown faces detected"
        )
        
        self.logger.critical(alert_message)
        
        if self.alert_callback:
            await self.alert_callback({
                'type': 'security_breach',
                'severity': 'critical',
                'message': alert_message,
                'confidence': result.confidence,
                'timestamp': result.timestamp,
                'face_location': result.face_location
            })
    
    def enroll_user(self, user_id: str, image_path: str) -> bool:
        """Enroll a new user from an image"""
        try:
            # Load image
            image = face_recognition.load_image_file(image_path)
            
            # Find face encodings
            encodings = face_recognition.face_encodings(image)
            
            if len(encodings) == 0:
                self.logger.error(f"No face found in image: {image_path}")
                return False
            
            if len(encodings) > 1:
                self.logger.warning(f"Multiple faces found in image: {image_path}, using first one")
            
            # Add to known faces
            self.known_encodings.append(encodings[0])
            self.known_names.append(user_id)
            
            # Save updated encodings
            self._save_known_faces()
            
            self.logger.info(f"User {user_id} enrolled successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to enroll user {user_id}: {e}")
            return False
    
    def remove_user(self, user_id: str) -> bool:
        """Remove a user from known faces"""
        try:
            if user_id in self.known_names:
                index = self.known_names.index(user_id)
                del self.known_names[index]
                del self.known_encodings[index]
                
                self._save_known_faces()
                
                self.logger.info(f"User {user_id} removed successfully")
                return True
            else:
                self.logger.warning(f"User {user_id} not found")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to remove user {user_id}: {e}")
            return False
    
    def _load_known_faces(self):
        """Load known face encodings from file"""
        try:
            if self.encodings_file.exists():
                with open(self.encodings_file, 'rb') as f:
                    data = pickle.load(f)
                    self.known_encodings = data.get('encodings', [])
                    self.known_names = data.get('names', [])
                
                self.logger.info(f"Loaded {len(self.known_names)} known faces")
            else:
                self.logger.info("No existing face encodings found")
                
        except Exception as e:
            self.logger.error(f"Failed to load known faces: {e}")
    
    def _save_known_faces(self):
        """Save known face encodings to file"""
        try:
            data = {
                'encodings': self.known_encodings,
                'names': self.known_names
            }
            
            with open(self.encodings_file, 'wb') as f:
                pickle.dump(data, f)
            
            self.logger.info(f"Saved {len(self.known_names)} known faces")
            
        except Exception as e:
            self.logger.error(f"Failed to save known faces: {e}")
    
    def get_known_users(self) -> List[str]:
        """Get list of enrolled users"""
        return self.known_names.copy()
    
    def get_last_recognition(self) -> Optional[RecognitionResult]:
        """Get last recognition result"""
        return self.last_recognition
    
    def is_user_authorized(self, user_id: str) -> bool:
        """Check if user is authorized"""
        return user_id in self.known_names
    
    def get_access_log(self, limit: int = 100) -> List[Dict]:
        """Get recent access log entries"""
        return self.access_log[-limit:]
    
    def get_status_report(self) -> str:
        """Get human-readable status report"""
        if not self.last_recognition:
            return "Face recognition active, no recent activity."
        
        result = self.last_recognition
        time_ago = (datetime.now() - result.timestamp).total_seconds()
        
        if result.authorized:
            return f"✅ Last authorized user: {result.user_id} ({time_ago:.0f}s ago, confidence: {result.confidence:.2f})"
        else:
            return f"⚠️ Unknown face detected {time_ago:.0f}s ago (confidence: {result.confidence:.2f})"
