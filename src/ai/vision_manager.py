"""
Computer vision manager for Sarus robot

Handles image capture, object detection, scene analysis, and visual
context generation using various computer vision models.
"""

import asyncio
import logging
import time
from typing import Dict, Any, List, Optional, Tuple
import base64
import io

# Computer vision libraries
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# AI models
try:
    import torch
    import torchvision.transforms as transforms
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

# HTTP client for API calls
import httpx

from ..config.settings import SYSTEM_CONFIG
from ..utils.logger import get_logger, PerformanceLogger

class VisionManager:
    """
    Manages computer vision functionality including object detection,
    scene analysis, and visual context generation
    """
    
    def __init__(self):
        self.logger = get_logger(__name__)
        
        # Configuration
        self.camera_device = SYSTEM_CONFIG.get('camera_device', 0)
        self.resolution = SYSTEM_CONFIG.get('camera_resolution', (640, 480))
        self.fps = SYSTEM_CONFIG.get('camera_fps', 30)
        self.confidence_threshold = SYSTEM_CONFIG.get('vision_confidence_threshold', 0.5)
        self.vision_model = SYSTEM_CONFIG.get('vision_model', 'llava')
        
        # Camera
        self.camera = None
        self.camera_available = False
        
        # Models
        self.object_detector = None
        self.scene_analyzer = None
        
        # Cache for recent frames
        self.current_frame = None
        self.last_analysis = None
        self.last_analysis_time = 0
        self.analysis_cache_duration = 2.0  # seconds
        
    async def initialize(self):
        """Initialize computer vision system"""
        self.logger.info("👁️ Initializing computer vision...")
        
        try:
            # Initialize camera
            await self._initialize_camera()
            
            # Initialize vision models
            await self._initialize_models()
            
            self.logger.info("✅ Computer vision initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize computer vision: {e}")
            # Don't raise - vision is optional for basic operation
    
    async def _initialize_camera(self):
        """Initialize camera for image capture"""
        if not CV2_AVAILABLE:
            self.logger.warning("OpenCV not available - camera disabled")
            return
        
        try:
            self.camera = cv2.VideoCapture(self.camera_device)
            
            if self.camera.isOpened():
                # Configure camera
                self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
                self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
                self.camera.set(cv2.CAP_PROP_FPS, self.fps)
                
                # Test capture
                ret, frame = self.camera.read()
                if ret:
                    self.camera_available = True
                    self.current_frame = frame
                    self.logger.info(f"✅ Camera initialized at {self.resolution}")
                else:
                    self.logger.warning("Camera test capture failed")
            else:
                self.logger.warning(f"Could not open camera device {self.camera_device}")
                
        except Exception as e:
            self.logger.error(f"Camera initialization failed: {e}")
    
    async def _initialize_models(self):
        """Initialize computer vision models"""
        model_type = self.vision_model.lower()
        
        if model_type == 'llava':
            await self._initialize_llava()
        elif model_type == 'yolo':
            await self._initialize_yolo()
        else:
            self.logger.info("Using basic computer vision (no AI models)")
    
    async def _initialize_llava(self):
        """Initialize LLaVA or similar vision-language model"""
        try:
            # Check if LLaVA is available via Ollama
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get("http://localhost:11434/api/tags")
                if response.status_code == 200:
                    models = response.json()
                    available_models = [model['name'] for model in models.get('models', [])]
                    
                    # Look for vision models
                    vision_models = [m for m in available_models if 'llava' in m.lower() or 'vision' in m.lower()]
                    
                    if vision_models:
                        self.scene_analyzer = vision_models[0]
                        self.logger.info(f"✅ Using vision model: {self.scene_analyzer}")
                    else:
                        self.logger.info("No vision models found in Ollama")
                        
        except Exception as e:
            self.logger.warning(f"Could not initialize LLaVA: {e}")
    
    async def _initialize_yolo(self):
        """Initialize YOLO object detection model"""
        if TORCH_AVAILABLE:
            try:
                # This would load a YOLO model - simplified for now
                self.logger.info("YOLO initialization placeholder")
                # self.object_detector = torch.hub.load('ultralytics/yolov5', 'yolov5s')
                
            except Exception as e:
                self.logger.warning(f"Could not initialize YOLO: {e}")
        else:
            self.logger.warning("PyTorch not available for YOLO")
    
    async def capture_frame(self) -> Optional[np.ndarray]:
        """
        Capture a single frame from the camera
        
        Returns:
            Captured frame as numpy array or None if failed
        """
        if not self.camera_available or not self.camera:
            # Return simulation frame for development
            if NUMPY_AVAILABLE:
                # Create a simple test pattern
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                frame[100:380, 160:480] = [100, 150, 200]  # Blue rectangle
                return frame
            return None
        
        try:
            ret, frame = self.camera.read()
            if ret:
                self.current_frame = frame
                return frame
            else:
                self.logger.warning("Failed to capture frame")
                
        except Exception as e:
            self.logger.error(f"Frame capture error: {e}")
        
        return None
    
    async def analyze_scene(self, force_refresh: bool = False) -> Optional[str]:
        """
        Analyze current scene and generate description
        
        Args:
            force_refresh: Force new analysis even if cache is valid
        
        Returns:
            Scene description text or None if failed
        """
        current_time = time.time()
        
        # Check cache
        if (not force_refresh and 
            self.last_analysis and 
            current_time - self.last_analysis_time < self.analysis_cache_duration):
            return self.last_analysis
        
        try:
            with PerformanceLogger("Scene analysis"):
                # Capture new frame
                frame = await self.capture_frame()
                if frame is None:
                    return "I cannot see anything right now - camera unavailable."
                
                # Analyze scene
                description = await self._analyze_frame(frame)
                
                # Cache result
                if description:
                    self.last_analysis = description
                    self.last_analysis_time = current_time
                
                return description
                
        except Exception as e:
            self.logger.error(f"Scene analysis failed: {e}")
            return "I'm having trouble analyzing what I see right now."
    
    async def _analyze_frame(self, frame: np.ndarray) -> Optional[str]:
        """Analyze a frame and generate description"""
        
        # Try vision-language model first
        if self.scene_analyzer:
            description = await self._analyze_with_llava(frame)
            if description:
                return description
        
        # Fallback to basic computer vision
        return await self._analyze_with_basic_cv(frame)
    
    async def _analyze_with_llava(self, frame: np.ndarray) -> Optional[str]:
        """Analyze frame using LLaVA or similar vision-language model"""
        try:
            # Convert frame to base64 for API
            image_b64 = self._frame_to_base64(frame)
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {
                    "model": self.scene_analyzer,
                    "prompt": "Describe what you see in this image. Focus on objects, people, and the environment. Be concise but specific.",
                    "images": [image_b64],
                    "stream": False
                }
                
                response = await client.post(
                    "http://localhost:11434/api/generate",
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    description = result.get('response', '').strip()
                    
                    if description:
                        self.logger.info(f"👁️ Scene analysis: {description}")
                        return description
                        
        except Exception as e:
            self.logger.error(f"LLaVA analysis failed: {e}")
        
        return None
    
    async def _analyze_with_basic_cv(self, frame: np.ndarray) -> str:
        """Basic computer vision analysis without AI models"""
        try:
            height, width = frame.shape[:2]
            
            # Basic analysis
            analysis_parts = []
            
            # Color analysis
            avg_color = np.mean(frame, axis=(0, 1))
            if avg_color[2] > avg_color[1] and avg_color[2] > avg_color[0]:
                analysis_parts.append("reddish lighting")
            elif avg_color[1] > avg_color[0] and avg_color[1] > avg_color[2]:
                analysis_parts.append("greenish lighting")
            elif avg_color[0] > avg_color[1] and avg_color[0] > avg_color[2]:
                analysis_parts.append("bluish lighting")
            else:
                analysis_parts.append("neutral lighting")
            
            # Brightness analysis
            brightness = np.mean(avg_color)
            if brightness < 50:
                analysis_parts.append("dark environment")
            elif brightness > 200:
                analysis_parts.append("bright environment")
            else:
                analysis_parts.append("well-lit environment")
            
            # Edge detection for complexity
            if CV2_AVAILABLE:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 50, 150)
                edge_density = np.sum(edges > 0) / (width * height)
                
                if edge_density > 0.1:
                    analysis_parts.append("complex scene with many objects")
                elif edge_density > 0.05:
                    analysis_parts.append("moderate complexity scene")
                else:
                    analysis_parts.append("simple scene")
            
            description = f"I can see a {', '.join(analysis_parts)}."
            return description
            
        except Exception as e:
            self.logger.error(f"Basic CV analysis failed: {e}")
            return "I can see something but cannot analyze it clearly."
    
    def _frame_to_base64(self, frame: np.ndarray) -> str:
        """Convert frame to base64 string for API calls"""
        try:
            if PIL_AVAILABLE:
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert to PIL Image
                pil_image = Image.fromarray(rgb_frame)
                
                # Convert to base64
                buffer = io.BytesIO()
                pil_image.save(buffer, format='JPEG', quality=85)
                image_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
                return image_b64
            else:
                # Fallback without PIL
                _, buffer = cv2.imencode('.jpg', frame)
                image_b64 = base64.b64encode(buffer).decode('utf-8')
                return image_b64
                
        except Exception as e:
            self.logger.error(f"Frame to base64 conversion failed: {e}")
            return ""
    
    async def detect_objects(self, confidence_threshold: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        Detect objects in current frame
        
        Args:
            confidence_threshold: Minimum confidence for detections
        
        Returns:
            List of detected objects with bounding boxes and labels
        """
        if confidence_threshold is None:
            confidence_threshold = self.confidence_threshold
        
        frame = await self.capture_frame()
        if frame is None:
            return []
        
        try:
            # If we have an object detector, use it
            if self.object_detector:
                return await self._detect_with_model(frame, confidence_threshold)
            else:
                # Basic object detection simulation
                return await self._simulate_object_detection(frame)
                
        except Exception as e:
            self.logger.error(f"Object detection failed: {e}")
            return []
    
    async def _detect_with_model(self, frame: np.ndarray, threshold: float) -> List[Dict[str, Any]]:
        """Detect objects using AI model"""
        # Placeholder for actual model inference
        detections = []
        
        # This would use YOLO or similar model
        # results = self.object_detector(frame)
        # for detection in results:
        #     if detection.confidence > threshold:
        #         detections.append({
        #             'name': detection.label,
        #             'confidence': detection.confidence,
        #             'bbox': detection.bbox,
        #             'center': detection.center
        #         })
        
        return detections
    
    async def _simulate_object_detection(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """Simulate object detection for development"""
        # Simple simulation based on frame properties
        height, width = frame.shape[:2]
        
        # Simulate finding some objects
        objects = [
            {
                'name': 'table',
                'confidence': 0.85,
                'bbox': (50, 100, 200, 300),
                'center': (125, 200)
            },
            {
                'name': 'chair',
                'confidence': 0.72,
                'bbox': (300, 200, 100, 150),
                'center': (350, 275)
            }
        ]
        
        return objects
    
    async def find_object(self, object_name: str) -> Optional[Dict[str, Any]]:
        """
        Look for a specific object in the scene
        
        Args:
            object_name: Name of object to find
        
        Returns:
            Object information if found, None otherwise
        """
        objects = await self.detect_objects()
        
        for obj in objects:
            if object_name.lower() in obj['name'].lower():
                self.logger.info(f"🎯 Found {object_name}: {obj}")
                return obj
        
        self.logger.info(f"❌ Object '{object_name}' not found")
        return None
    
    async def get_navigation_info(self) -> Dict[str, Any]:
        """
        Get visual information useful for navigation
        
        Returns:
            Navigation-relevant visual information
        """
        frame = await self.capture_frame()
        if frame is None:
            return {'obstacles': [], 'clear_path': False}
        
        try:
            # Basic obstacle detection
            obstacles = await self._detect_obstacles(frame)
            
            # Path analysis
            clear_path = await self._analyze_path_clearance(frame)
            
            return {
                'obstacles': obstacles,
                'clear_path': clear_path,
                'frame_size': frame.shape[:2],
                'timestamp': time.time()
            }
            
        except Exception as e:
            self.logger.error(f"Navigation info extraction failed: {e}")
            return {'obstacles': [], 'clear_path': False}
    
    async def _detect_obstacles(self, frame: np.ndarray) -> List[Dict[str, Any]]:
        """Detect obstacles in the path"""
        obstacles = []
        
        # Simple obstacle detection based on edges and contours
        if CV2_AVAILABLE:
            try:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 50, 150)
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                height, width = frame.shape[:2]
                bottom_half = height // 2
                
                for contour in contours:
                    area = cv2.contourArea(contour)
                    if area > 500:  # Minimum obstacle size
                        x, y, w, h = cv2.boundingRect(contour)
                        
                        # Only consider obstacles in lower half of frame (closer to robot)
                        if y + h > bottom_half:
                            obstacles.append({
                                'bbox': (x, y, w, h),
                                'area': area,
                                'distance_estimate': self._estimate_distance(w, h)
                            })
            
            except Exception as e:
                self.logger.error(f"Obstacle detection error: {e}")
        
        return obstacles
    
    async def _analyze_path_clearance(self, frame: np.ndarray) -> bool:
        """Analyze if path ahead is clear"""
        obstacles = await self._detect_obstacles(frame)
        
        # Consider path clear if no large obstacles in central area
        height, width = frame.shape[:2]
        center_x = width // 2
        path_width = width // 3
        
        for obstacle in obstacles:
            x, y, w, h = obstacle['bbox']
            obstacle_center = x + w // 2
            
            # Check if obstacle is in central path
            if (center_x - path_width // 2 < obstacle_center < center_x + path_width // 2 and
                obstacle['area'] > 1000):  # Significant obstacle
                return False
        
        return True
    
    def _estimate_distance(self, width: int, height: int) -> float:
        """Estimate distance to object based on size (very rough)"""
        # This is a very simplified distance estimation
        # In reality, would need calibration and known object sizes
        size = width * height
        
        if size > 10000:
            return 0.5  # Very close
        elif size > 5000:
            return 1.0  # Close
        elif size > 1000:
            return 2.0  # Medium distance
        else:
            return 3.0  # Far
    
    def cleanup(self):
        """Clean up vision resources"""
        if self.camera:
            self.camera.release()
        
        self.logger.info("🧹 Computer vision cleanup complete")
