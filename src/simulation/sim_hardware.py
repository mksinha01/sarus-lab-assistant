"""
Simulation Hardware Controllers for Sarus Robot
These replace real hardware when running in simulation mode
"""
import asyncio
import time
import numpy as np
from typing import Optional, Dict, Any

class SimMotorController:
    """Simulated motor controller for demo"""
    
    def __init__(self, sim_world=None):
        self.sim_world = sim_world
        self.left_speed = 0.0
        self.right_speed = 0.0
        self.max_speed = 1.0
        self.enabled = True
        
    async def initialize(self):
        """Initialize simulated motors"""
        print("🚗 Simulated Motor Controller initialized")
        return True
    
    def move_forward(self, speed=0.5):
        """Move robot forward"""
        speed = max(0, min(self.max_speed, speed))
        self.left_speed = speed
        self.right_speed = speed
        if self.sim_world:
            self.sim_world.set_motor_speeds(speed, speed)
        print(f"🔄 Moving forward at speed {speed}")
    
    def move_backward(self, speed=0.5):
        """Move robot backward"""
        speed = max(0, min(self.max_speed, speed))
        self.left_speed = -speed
        self.right_speed = -speed
        if self.sim_world:
            self.sim_world.set_motor_speeds(-speed, -speed)
        print(f"🔄 Moving backward at speed {speed}")
    
    def turn_left(self, speed=0.3):
        """Turn robot left"""
        speed = max(0, min(self.max_speed, speed))
        self.left_speed = -speed
        self.right_speed = speed
        if self.sim_world:
            self.sim_world.set_motor_speeds(-speed, speed)
        print(f"🔄 Turning left at speed {speed}")
    
    def turn_right(self, speed=0.3):
        """Turn robot right"""
        speed = max(0, min(self.max_speed, speed))
        self.left_speed = speed
        self.right_speed = -speed
        if self.sim_world:
            self.sim_world.set_motor_speeds(speed, -speed)
        print(f"🔄 Turning right at speed {speed}")
    
    def stop(self):
        """Stop robot movement"""
        self.left_speed = 0.0
        self.right_speed = 0.0
        if self.sim_world:
            self.sim_world.set_motor_speeds(0, 0)
        print("🛑 Robot stopped")
    
    def set_speeds(self, left_speed: float, right_speed: float):
        """Set individual wheel speeds"""
        self.left_speed = max(-self.max_speed, min(self.max_speed, left_speed))
        self.right_speed = max(-self.max_speed, min(self.max_speed, right_speed))
        if self.sim_world:
            self.sim_world.set_motor_speeds(self.left_speed, self.right_speed)
        print(f"🔄 Set speeds: L={self.left_speed:.2f}, R={self.right_speed:.2f}")
    
    def cleanup(self):
        """Cleanup motor controller"""
        self.stop()
        print("🔄 Motor controller cleaned up")


class SimSensorManager:
    """Simulated sensor manager for demo"""
    
    def __init__(self, sim_world=None):
        self.sim_world = sim_world
        self.start_time = time.time()
        
    async def initialize(self):
        """Initialize simulated sensors"""
        print("📡 Simulated Sensor Manager initialized")
        return True
    
    def get_obstacle_map(self) -> Dict[str, Any]:
        """Get simulated obstacle detection data"""
        obstacles = {}
        
        if self.sim_world:
            # Get distances from ultrasonic sensors
            distances = {
                'front_left': self.sim_world.get_ultrasonic_distance(-0.5),
                'front_center': self.sim_world.get_ultrasonic_distance(0.0),
                'front_right': self.sim_world.get_ultrasonic_distance(0.5)
            }
            
            # Determine obstacles
            for direction, distance in distances.items():
                if distance < 0.5:  # Obstacle within 50cm
                    obstacles[direction] = {
                        'distance': round(distance, 2),
                        'threat_level': 'high' if distance < 0.3 else 'medium'
                    }
        else:
            # Fallback simulated data
            obstacles = {
                'front_center': {'distance': 1.2, 'threat_level': 'low'}
            }
        
        return {
            'timestamp': time.time(),
            'obstacles': obstacles,
            'paths_clear': len(obstacles) == 0,
            'emergency_distances': [obs['distance'] for obs in obstacles.values() if obs['distance'] < 0.3]
        }
    
    def get_navigation_data(self) -> Dict[str, Any]:
        """Get navigation sensor data"""
        if self.sim_world:
            pose = self.sim_world.get_robot_pose()
            return {
                'position': pose['position'],
                'orientation': pose['orientation'],
                'speed_estimate': abs(self.sim_world.left_wheel_speed + self.sim_world.right_wheel_speed) / 2,
                'heading': pose['orientation']['yaw']
            }
        else:
            return {
                'position': {'x': 0, 'y': 0, 'z': 0.1},
                'orientation': {'roll': 0, 'pitch': 0, 'yaw': 0},
                'speed_estimate': 0.0,
                'heading': 0.0
            }
    
    def get_battery_level(self) -> float:
        """Simulate battery discharge"""
        elapsed = time.time() - self.start_time
        # Simulate 2% discharge per minute
        battery = max(10.0, 100.0 - (elapsed / 60) * 2)
        return battery
    
    def get_temperature(self) -> float:
        """Simulate temperature reading"""
        # Simulate CPU temperature
        base_temp = 45.0
        variation = 5.0 * np.sin(time.time() / 30)  # Slow variation
        return base_temp + variation
    
    def cleanup(self):
        """Cleanup sensor manager"""
        print("📡 Sensor manager cleaned up")


class SimVisionManager:
    """Simulated vision manager for demo"""
    
    def __init__(self, sim_world=None):
        self.sim_world = sim_world
        self.frame_count = 0
        
    async def initialize(self):
        """Initialize simulated camera"""
        print("👁️ Simulated Vision Manager initialized")
        return True
    
    async def capture_frame(self) -> Optional[np.ndarray]:
        """Capture simulated camera frame"""
        if self.sim_world:
            # Get actual camera image from simulation
            image = self.sim_world.get_camera_image(640, 480)
            self.frame_count += 1
            return image
        else:
            # Generate a test pattern
            image = np.zeros((480, 640, 3), dtype=np.uint8)
            # Add some pattern
            image[100:200, 100:200] = [255, 0, 0]  # Red square
            image[300:400, 400:500] = [0, 255, 0]  # Green square
            self.frame_count += 1
            return image
    
    async def analyze_scene(self, image: Optional[np.ndarray] = None) -> Dict[str, Any]:
        """Analyze simulated scene"""
        if image is None:
            image = await self.capture_frame()
        
        # Simulate object detection
        objects = []
        
        if self.sim_world:
            # Simulate detecting lab equipment
            objects = [
                {'name': 'table', 'confidence': 0.95, 'bbox': [100, 150, 200, 250]},
                {'name': 'equipment', 'confidence': 0.87, 'bbox': [300, 100, 400, 200]}
            ]
        
        return {
            'timestamp': time.time(),
            'frame_number': self.frame_count,
            'objects_detected': objects,
            'scene_description': 'College laboratory environment with tables and equipment',
            'lighting_quality': 'good',
            'image_quality': 'high'
        }
    
    async def detect_obstacles(self) -> Dict[str, Any]:
        """Detect visual obstacles"""
        analysis = await self.analyze_scene()
        
        obstacles = []
        for obj in analysis['objects_detected']:
            if obj['name'] in ['table', 'equipment', 'obstacle']:
                obstacles.append({
                    'type': obj['name'],
                    'confidence': obj['confidence'],
                    'position': 'center' if obj['bbox'][0] > 200 and obj['bbox'][2] < 440 else 'side'
                })
        
        return {
            'timestamp': time.time(),
            'visual_obstacles': obstacles,
            'path_clear': len(obstacles) == 0
        }
    
    def cleanup(self):
        """Cleanup vision manager"""
        print("👁️ Vision manager cleaned up")
