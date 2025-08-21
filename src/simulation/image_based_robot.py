#!/usr/bin/env python3
"""
🤖 CUSTOM ROBOT MODEL BASED ON USER IMAGE
Easily customizable robot design system
"""

import pybullet as p
import pybullet_data
import numpy as np
from typing import List, Dict, Tuple

class ImageBasedRobotModel:
    """Create robot model based on user's image specifications"""
    
    def __init__(self):
        self.robot_id = None
        self.components = {}
        
    def create_robot_from_specs(self, specs: Dict) -> int:
        """Create robot based on specifications derived from image"""
        
        print(f"🤖 Creating robot based on your image design...")
        print(f"   Robot type: {specs.get('type', 'custom')}")
        print(f"   Main color: {specs.get('main_color', 'blue')}")
        print(f"   Style: {specs.get('style', 'modern')}")
        
        # Main body/chassis
        self._create_main_body(specs)
        
        # Wheels or movement system
        self._create_movement_system(specs)
        
        # Sensors and equipment
        self._create_sensors_equipment(specs)
        
        # Special features
        self._create_special_features(specs)
        
        return self.robot_id
    
    def _create_main_body(self, specs: Dict):
        """Create the main robot body"""
        body_config = specs.get('body', {})
        
        # Default body specifications (modify these to match your image)
        body_shape = body_config.get('shape', 'box')  # box, cylinder, rounded
        body_size = body_config.get('size', [0.4, 0.25, 0.12])  # length, width, height
        body_color = body_config.get('color', [0.2, 0.5, 0.8, 1.0])  # RGBA
        body_position = body_config.get('position', [0, 0, 0.5])
        
        print(f"🏗️ Creating main body:")
        print(f"   Shape: {body_shape}")
        print(f"   Size: {body_size}")
        print(f"   Color: RGB{body_color[:3]}")
        
        if body_shape == 'box':
            body_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=body_size)
            body_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=body_size, rgbaColor=body_color)
        elif body_shape == 'cylinder':
            body_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=body_size[0], height=body_size[2])
            body_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=body_size[0], length=body_size[2], rgbaColor=body_color)
        elif body_shape == 'rounded':
            # Create rounded body using capsule
            body_collision = p.createCollisionShape(p.GEOM_CAPSULE, radius=body_size[1], height=body_size[2])
            body_visual = p.createVisualShape(p.GEOM_CAPSULE, radius=body_size[1], length=body_size[2], rgbaColor=body_color)
        else:
            # Default to box
            body_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=body_size)
            body_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=body_size, rgbaColor=body_color)
        
        # Create main robot body
        self.robot_id = p.createMultiBody(
            baseMass=5.0,
            baseCollisionShapeIndex=body_collision,
            baseVisualShapeIndex=body_visual,
            basePosition=body_position
        )
        
        self.components['main_body'] = self.robot_id
        print("   ✅ Main body created")
    
    def _create_movement_system(self, specs: Dict):
        """Create wheels, tracks, or legs based on image"""
        movement_config = specs.get('movement', {})
        movement_type = movement_config.get('type', 'wheels')  # wheels, tracks, legs
        
        print(f"🚗 Creating movement system: {movement_type}")
        
        if movement_type == 'wheels':
            self._create_wheels(movement_config)
        elif movement_type == 'tracks':
            self._create_tracks(movement_config)
        elif movement_type == 'legs':
            self._create_legs(movement_config)
        else:
            self._create_wheels(movement_config)  # Default
    
    def _create_wheels(self, config: Dict):
        """Create wheel system"""
        wheel_count = config.get('count', 4)  # 2, 4, 6, 8
        wheel_radius = config.get('radius', 0.08)
        wheel_width = config.get('width', 0.04)
        wheel_color = config.get('color', [0.1, 0.1, 0.1, 1.0])  # Black
        
        robot_pos, robot_orn = p.getBasePositionAndOrientation(self.robot_id)
        
        # Position wheels based on count
        if wheel_count == 2:
            wheel_positions = [
                [0, 0.15, -0.1],   # Right
                [0, -0.15, -0.1]   # Left
            ]
        elif wheel_count == 4:
            wheel_positions = [
                [0.2, 0.15, -0.1],   # Front right
                [0.2, -0.15, -0.1],  # Front left
                [-0.2, 0.15, -0.1],  # Back right
                [-0.2, -0.15, -0.1]  # Back left
            ]
        elif wheel_count == 6:
            wheel_positions = [
                [0.25, 0.15, -0.1],   # Front right
                [0.25, -0.15, -0.1],  # Front left
                [0, 0.15, -0.1],      # Middle right
                [0, -0.15, -0.1],     # Middle left
                [-0.25, 0.15, -0.1],  # Back right
                [-0.25, -0.15, -0.1]  # Back left
            ]
        else:
            # Default 4 wheels
            wheel_positions = [
                [0.2, 0.15, -0.1], [0.2, -0.15, -0.1],
                [-0.2, 0.15, -0.1], [-0.2, -0.15, -0.1]
            ]
        
        for i, (x, y, z) in enumerate(wheel_positions):
            wheel_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=wheel_radius, height=wheel_width)
            wheel_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=wheel_radius, length=wheel_width, rgbaColor=wheel_color)
            
            wheel_pos = [robot_pos[0] + x, robot_pos[1] + y, robot_pos[2] + z]
            
            wheel_id = p.createMultiBody(
                baseMass=1.0,
                baseCollisionShapeIndex=wheel_collision,
                baseVisualShapeIndex=wheel_visual,
                basePosition=wheel_pos
            )
            
            self.components[f'wheel_{i}'] = wheel_id
            print(f"   ✅ Wheel {i+1} created")
    
    def _create_tracks(self, config: Dict):
        """Create tank-style tracks"""
        track_color = config.get('color', [0.2, 0.2, 0.2, 1.0])
        
        robot_pos, robot_orn = p.getBasePositionAndOrientation(self.robot_id)
        
        # Left and right tracks
        track_positions = [
            [0, 0.2, -0.05],   # Right track
            [0, -0.2, -0.05]   # Left track
        ]
        
        for i, (x, y, z) in enumerate(track_positions):
            track_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.3, 0.05, 0.08])
            track_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.3, 0.05, 0.08], rgbaColor=track_color)
            
            track_pos = [robot_pos[0] + x, robot_pos[1] + y, robot_pos[2] + z]
            
            track_id = p.createMultiBody(
                baseMass=2.0,
                baseCollisionShapeIndex=track_collision,
                baseVisualShapeIndex=track_visual,
                basePosition=track_pos
            )
            
            self.components[f'track_{i}'] = track_id
            print(f"   ✅ Track {i+1} created")
    
    def _create_legs(self, config: Dict):
        """Create leg system for walking robots"""
        leg_count = config.get('count', 2)  # 2, 4, 6
        leg_color = config.get('color', [0.4, 0.4, 0.4, 1.0])
        
        robot_pos, robot_orn = p.getBasePositionAndOrientation(self.robot_id)
        
        if leg_count == 2:
            leg_positions = [
                [0, 0.1, -0.2],   # Right leg
                [0, -0.1, -0.2]   # Left leg
            ]
        elif leg_count == 4:
            leg_positions = [
                [0.15, 0.1, -0.2],   # Front right
                [0.15, -0.1, -0.2],  # Front left
                [-0.15, 0.1, -0.2],  # Back right
                [-0.15, -0.1, -0.2]  # Back left
            ]
        else:
            leg_positions = [[0, 0.1, -0.2], [0, -0.1, -0.2]]
        
        for i, (x, y, z) in enumerate(leg_positions):
            leg_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.03, height=0.2)
            leg_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.03, length=0.2, rgbaColor=leg_color)
            
            leg_pos = [robot_pos[0] + x, robot_pos[1] + y, robot_pos[2] + z]
            
            leg_id = p.createMultiBody(
                baseMass=0.5,
                baseCollisionShapeIndex=leg_collision,
                baseVisualShapeIndex=leg_visual,
                basePosition=leg_pos
            )
            
            self.components[f'leg_{i}'] = leg_id
            print(f"   ✅ Leg {i+1} created")
    
    def _create_sensors_equipment(self, specs: Dict):
        """Create sensors and equipment"""
        sensor_config = specs.get('sensors', {})
        
        robot_pos, robot_orn = p.getBasePositionAndOrientation(self.robot_id)
        
        # Camera
        if sensor_config.get('camera', True):
            camera_color = sensor_config.get('camera_color', [0.1, 0.1, 0.1, 1.0])
            camera_pos = [robot_pos[0], robot_pos[1], robot_pos[2] + 0.15]
            
            camera_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.03, 0.03, 0.02])
            camera_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.03, 0.03, 0.02], rgbaColor=camera_color)
            
            camera_id = p.createMultiBody(
                baseMass=0.1,
                baseCollisionShapeIndex=camera_collision,
                baseVisualShapeIndex=camera_visual,
                basePosition=camera_pos
            )
            
            self.components['camera'] = camera_id
            print("   📷 Camera added")
        
        # Sensors (ultrasonic, lidar, etc.)
        sensor_positions = sensor_config.get('positions', [
            [0.25, 0, 0.05],     # Front center
            [0.2, 0.1, 0.05],    # Front right
            [0.2, -0.1, 0.05]    # Front left
        ])
        
        sensor_color = sensor_config.get('color', [1.0, 1.0, 0.0, 1.0])  # Yellow
        
        for i, (x, y, z) in enumerate(sensor_positions):
            sensor_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.015, height=0.03)
            sensor_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.015, length=0.03, rgbaColor=sensor_color)
            
            sensor_pos = [robot_pos[0] + x, robot_pos[1] + y, robot_pos[2] + z]
            
            sensor_id = p.createMultiBody(
                baseMass=0.05,
                baseCollisionShapeIndex=sensor_collision,
                baseVisualShapeIndex=sensor_visual,
                basePosition=sensor_pos
            )
            
            self.components[f'sensor_{i}'] = sensor_id
            print(f"   📡 Sensor {i+1} added")
    
    def _create_special_features(self, specs: Dict):
        """Create special features like arms, antennas, etc."""
        features_config = specs.get('features', {})
        
        robot_pos, robot_orn = p.getBasePositionAndOrientation(self.robot_id)
        
        # Antenna
        if features_config.get('antenna', False):
            antenna_color = features_config.get('antenna_color', [0.8, 0.8, 0.8, 1.0])
            antenna_pos = [robot_pos[0], robot_pos[1], robot_pos[2] + 0.25]
            
            antenna_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.005, height=0.15)
            antenna_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.005, length=0.15, rgbaColor=antenna_color)
            
            antenna_id = p.createMultiBody(
                baseMass=0.02,
                baseCollisionShapeIndex=antenna_collision,
                baseVisualShapeIndex=antenna_visual,
                basePosition=antenna_pos
            )
            
            self.components['antenna'] = antenna_id
            print("   📡 Antenna added")
        
        # Arms (if humanoid or service robot)
        if features_config.get('arms', False):
            arm_color = features_config.get('arm_color', [0.6, 0.6, 0.6, 1.0])
            
            arm_positions = [
                [0, 0.2, 0.05],   # Right arm
                [0, -0.2, 0.05]   # Left arm
            ]
            
            for i, (x, y, z) in enumerate(arm_positions):
                arm_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.02, height=0.15)
                arm_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=0.02, length=0.15, rgbaColor=arm_color)
                
                arm_pos = [robot_pos[0] + x, robot_pos[1] + y, robot_pos[2] + z]
                
                arm_id = p.createMultiBody(
                    baseMass=0.3,
                    baseCollisionShapeIndex=arm_collision,
                    baseVisualShapeIndex=arm_visual,
                    basePosition=arm_pos
                )
                
                self.components[f'arm_{i}'] = arm_id
                print(f"   🦾 Arm {i+1} added")

def get_robot_specs_templates():
    """Get template specifications for different robot types"""
    return {
        'modern_car_robot': {
            'type': 'car',
            'main_color': 'blue',
            'style': 'modern',
            'body': {
                'shape': 'box',
                'size': [0.4, 0.25, 0.12],
                'color': [0.2, 0.5, 0.8, 1.0],  # Blue
                'position': [0, 0, 0.5]
            },
            'movement': {
                'type': 'wheels',
                'count': 4,
                'radius': 0.08,
                'width': 0.04,
                'color': [0.1, 0.1, 0.1, 1.0]
            },
            'sensors': {
                'camera': True,
                'camera_color': [0.1, 0.1, 0.1, 1.0],
                'positions': [
                    [0.25, 0, 0.05],
                    [0.2, 0.1, 0.05],
                    [0.2, -0.1, 0.05]
                ],
                'color': [1.0, 1.0, 0.0, 1.0]
            },
            'features': {
                'antenna': True,
                'antenna_color': [0.8, 0.8, 0.8, 1.0],
                'arms': False
            }
        },
        'tank_robot': {
            'type': 'tank',
            'main_color': 'green',
            'style': 'military',
            'body': {
                'shape': 'box',
                'size': [0.5, 0.3, 0.15],
                'color': [0.3, 0.6, 0.3, 1.0],  # Military green
                'position': [0, 0, 0.5]
            },
            'movement': {
                'type': 'tracks',
                'color': [0.2, 0.2, 0.2, 1.0]
            },
            'sensors': {
                'camera': True,
                'camera_color': [0.1, 0.1, 0.1, 1.0],
                'positions': [
                    [0.3, 0, 0.1],
                    [0.25, 0.15, 0.1],
                    [0.25, -0.15, 0.1]
                ],
                'color': [1.0, 0.5, 0.0, 1.0]  # Orange sensors
            },
            'features': {
                'antenna': True,
                'antenna_color': [0.9, 0.9, 0.9, 1.0],
                'arms': False
            }
        },
        'humanoid_robot': {
            'type': 'humanoid',
            'main_color': 'silver',
            'style': 'futuristic',
            'body': {
                'shape': 'cylinder',
                'size': [0.15, 0.15, 0.3],
                'color': [0.8, 0.8, 0.8, 1.0],  # Silver
                'position': [0, 0, 1.0]
            },
            'movement': {
                'type': 'legs',
                'count': 2,
                'color': [0.6, 0.6, 0.6, 1.0]
            },
            'sensors': {
                'camera': True,
                'camera_color': [0.0, 0.5, 1.0, 1.0],  # Blue camera
                'positions': [
                    [0.1, 0, 0.2]  # Face camera
                ],
                'color': [0.0, 1.0, 1.0, 1.0]  # Cyan sensors
            },
            'features': {
                'antenna': False,
                'arms': True,
                'arm_color': [0.7, 0.7, 0.7, 1.0]
            }
        }
    }

def create_robot_from_image_demo():
    """Demo function to create robot based on image specifications"""
    print("🤖 CREATING ROBOT FROM YOUR IMAGE")
    print("=" * 50)
    
    try:
        import pybullet as p
        import pybullet_data
        
        # Initialize simulation
        client = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.resetSimulation()
        p.setGravity(0, 0, -9.81)
        
        # Create ground
        ground_shape = p.createCollisionShape(p.GEOM_PLANE)
        ground_visual = p.createVisualShape(p.GEOM_PLANE, rgbaColor=[0.8, 0.8, 0.8, 1])
        ground_id = p.createMultiBody(0, ground_shape, ground_visual)
        
        # Set camera view
        p.resetDebugVisualizerCamera(
            cameraDistance=3.0,
            cameraYaw=45,
            cameraPitch=-20,
            cameraTargetPosition=[0, 0, 0]
        )
        
        # Get template specifications (modify these to match your image)
        templates = get_robot_specs_templates()
        
        print("Based on your image, I'm creating a custom robot...")
        print("(You can modify the specifications in the code to match exactly)")
        
        # Create robot model
        robot_model = ImageBasedRobotModel()
        
        # Use modern car robot as base (modify this to match your image)
        robot_specs = templates['modern_car_robot']
        
        # Create the robot
        robot_id = robot_model.create_robot_from_specs(robot_specs)
        
        print("\n✅ Robot created based on your design!")
        print("🎮 Controls:")
        print("   - Mouse: Rotate camera around robot")
        print("   - Scroll: Zoom in/out") 
        print("   - Right-click + drag: Pan camera")
        print("   - Close window when done examining robot")
        
        # Animation loop
        import time
        step_count = 0
        
        while True:
            try:
                p.stepSimulation()
                
                # Simple movement animation every 4 seconds
                if step_count % 240 == 0:
                    pos, orn = p.getBasePositionAndOrientation(robot_id)
                    # Move robot slightly for demonstration
                    new_pos = [pos[0] + 0.05 * np.sin(step_count / 240), pos[1], pos[2]]
                    p.resetBasePositionAndOrientation(robot_id, new_pos, orn)
                
                step_count += 1
                time.sleep(1/240)
                
            except KeyboardInterrupt:
                break
        
        p.disconnect()
        print("Demo completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_robot_from_image_demo()
