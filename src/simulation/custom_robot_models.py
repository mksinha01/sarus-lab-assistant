#!/usr/bin/env python3
"""
Custom Robot Models for Sarus Robot Simulation
Easy-to-modify robot designs for different use cases
"""

import pybullet as p
import numpy as np
from typing import List, Tuple, Dict

class RobotModelFactory:
    """Factory for creating different robot models"""
    
    def __init__(self):
        self.robot_models = {
            'car': self.create_car_robot,
            'tank': self.create_tank_robot,
            'humanoid': self.create_humanoid_robot,
            'rover': self.create_rover_robot,
            'custom': self.create_custom_robot
        }
    
    def create_robot(self, model_type: str = 'car', position: List[float] = [0, 0, 0.5], **kwargs) -> int:
        """Create a robot of the specified type"""
        if model_type not in self.robot_models:
            print(f"❌ Unknown robot model: {model_type}")
            print(f"Available models: {list(self.robot_models.keys())}")
            model_type = 'car'  # Default fallback
        
        print(f"🤖 Creating {model_type.upper()} robot model...")
        return self.robot_models[model_type](position, **kwargs)
    
    def create_car_robot(self, position: List[float], **kwargs) -> int:
        """Create a realistic car-like robot"""
        # Customizable parameters
        chassis_size = kwargs.get('chassis_size', [0.4, 0.2, 0.1])
        chassis_color = kwargs.get('chassis_color', [0.2, 0.5, 0.8, 1.0])  # Blue
        wheel_radius = kwargs.get('wheel_radius', 0.1)
        wheel_width = kwargs.get('wheel_width', 0.05)
        
        print("🚗 Building Car-Style Robot:")
        print(f"   - Chassis: {chassis_size}")
        print(f"   - Color: RGB{chassis_color[:3]}")
        print(f"   - Wheel size: {wheel_radius}m radius")
        
        # Main chassis
        chassis_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=chassis_size)
        chassis_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=chassis_size,
                                           rgbaColor=chassis_color)
        
        robot_id = p.createMultiBody(baseMass=5.0,
                                   baseCollisionShapeIndex=chassis_shape,
                                   baseVisualShapeIndex=chassis_visual,
                                   basePosition=position)
        
        # Add wheels
        self._add_car_wheels(robot_id, wheel_radius, wheel_width, chassis_size)
        
        # Add sensors and equipment
        self._add_car_equipment(robot_id, chassis_size)
        
        return robot_id
    
    def create_tank_robot(self, position: List[float], **kwargs) -> int:
        """Create a tank-style robot with tracks"""
        # Customizable parameters
        chassis_size = kwargs.get('chassis_size', [0.5, 0.3, 0.15])
        chassis_color = kwargs.get('chassis_color', [0.3, 0.6, 0.3, 1.0])  # Green
        
        print("🛡️ Building Tank-Style Robot:")
        print(f"   - Heavy chassis: {chassis_size}")
        print(f"   - Military green color")
        
        # Heavy chassis
        chassis_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=chassis_size)
        chassis_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=chassis_size,
                                           rgbaColor=chassis_color)
        
        robot_id = p.createMultiBody(baseMass=10.0,  # Heavier than car
                                   baseCollisionShapeIndex=chassis_shape,
                                   baseVisualShapeIndex=chassis_visual,
                                   basePosition=position)
        
        # Add tank tracks
        self._add_tank_tracks(robot_id, chassis_size)
        
        # Add military equipment
        self._add_tank_equipment(robot_id, chassis_size)
        
        return robot_id
    
    def create_rover_robot(self, position: List[float], **kwargs) -> int:
        """Create a Mars rover-style robot"""
        # Customizable parameters
        chassis_size = kwargs.get('chassis_size', [0.6, 0.4, 0.12])
        chassis_color = kwargs.get('chassis_color', [0.8, 0.8, 0.8, 1.0])  # Silver
        
        print("🚀 Building Rover-Style Robot:")
        print(f"   - Space-grade chassis: {chassis_size}")
        print(f"   - Silver metallic finish")
        
        # Space-grade chassis
        chassis_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=chassis_size)
        chassis_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=chassis_size,
                                           rgbaColor=chassis_color)
        
        robot_id = p.createMultiBody(baseMass=8.0,
                                   baseCollisionShapeIndex=chassis_shape,
                                   baseVisualShapeIndex=chassis_visual,
                                   basePosition=position)
        
        # Add 6-wheel suspension system
        self._add_rover_wheels(robot_id, chassis_size)
        
        # Add scientific equipment
        self._add_rover_equipment(robot_id, chassis_size)
        
        return robot_id
    
    def create_humanoid_robot(self, position: List[float], **kwargs) -> int:
        """Create a humanoid robot"""
        print("🤖 Building Humanoid Robot:")
        print("   - Bipedal design")
        print("   - Human-like proportions")
        
        # Torso
        torso_size = [0.15, 0.1, 0.3]
        torso_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=torso_size)
        torso_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=torso_size,
                                         rgbaColor=[0.7, 0.7, 0.7, 1.0])
        
        robot_id = p.createMultiBody(baseMass=50.0,
                                   baseCollisionShapeIndex=torso_shape,
                                   baseVisualShapeIndex=torso_visual,
                                   basePosition=position)
        
        # Add humanoid features
        self._add_humanoid_parts(robot_id)
        
        return robot_id
    
    def create_custom_robot(self, position: List[float], **kwargs) -> int:
        """Create a custom robot based on user specifications"""
        print("⚙️ Building Custom Robot:")
        print("   - User-defined specifications")
        
        # Get custom parameters
        parts = kwargs.get('parts', [])
        base_config = kwargs.get('base_config', {
            'size': [0.3, 0.3, 0.1],
            'color': [1.0, 0.5, 0.0, 1.0],  # Orange
            'mass': 5.0
        })
        
        # Create base
        base_size = base_config['size']
        base_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=base_size)
        base_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=base_size,
                                        rgbaColor=base_config['color'])
        
        robot_id = p.createMultiBody(baseMass=base_config['mass'],
                                   baseCollisionShapeIndex=base_shape,
                                   baseVisualShapeIndex=base_visual,
                                   basePosition=position)
        
        # Add custom parts
        for part in parts:
            self._add_custom_part(robot_id, part)
        
        return robot_id
    
    def _add_car_wheels(self, robot_id: int, radius: float, width: float, chassis_size: List[float]):
        """Add wheels to car robot"""
        wheel_positions = [
            [chassis_size[0] * 0.7, chassis_size[1] + 0.05, -chassis_size[2] * 0.5],  # Front right
            [chassis_size[0] * 0.7, -(chassis_size[1] + 0.05), -chassis_size[2] * 0.5],  # Front left
            [-chassis_size[0] * 0.7, chassis_size[1] + 0.05, -chassis_size[2] * 0.5],  # Back right
            [-chassis_size[0] * 0.7, -(chassis_size[1] + 0.05), -chassis_size[2] * 0.5]  # Back left
        ]
        
        robot_pos = p.getBasePositionAndOrientation(robot_id)[0]
        
        for i, (x, y, z) in enumerate(wheel_positions):
            # Create wheel
            wheel_shape = p.createCollisionShape(p.GEOM_CYLINDER, radius=radius, height=width)
            wheel_visual = p.createVisualShape(p.GEOM_CYLINDER, radius=radius, length=width,
                                             rgbaColor=[0.1, 0.1, 0.1, 1.0])
            
            wheel_pos = [robot_pos[0] + x, robot_pos[1] + y, robot_pos[2] + z]
            
            wheel_id = p.createMultiBody(baseMass=1.0,
                                       baseCollisionShapeIndex=wheel_shape,
                                       baseVisualShapeIndex=wheel_visual,
                                       basePosition=wheel_pos)
            
            print(f"   ✅ Wheel {i+1} added at {wheel_pos}")
    
    def _add_car_equipment(self, robot_id: int, chassis_size: List[float]):
        """Add sensors and equipment to car robot"""
        robot_pos = p.getBasePositionAndOrientation(robot_id)[0]
        
        # Front sensors
        sensor_positions = [
            [chassis_size[0] + 0.05, 0, 0.05],  # Front center
            [chassis_size[0] * 0.8, chassis_size[1] * 0.7, 0.05],  # Front right
            [chassis_size[0] * 0.8, -chassis_size[1] * 0.7, 0.05]  # Front left
        ]
        
        for i, (x, y, z) in enumerate(sensor_positions):
            sensor_shape = p.createVisualShape(p.GEOM_CYLINDER, radius=0.02, length=0.04,
                                             rgbaColor=[1, 1, 0, 1.0])  # Yellow
            sensor_pos = [robot_pos[0] + x, robot_pos[1] + y, robot_pos[2] + z]
            
            sensor_id = p.createMultiBody(baseMass=0.1,
                                        baseVisualShapeIndex=sensor_shape,
                                        basePosition=sensor_pos)
            
            print(f"   📡 Sensor {i+1} added")
        
        # Camera on top
        camera_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.03, 0.03, 0.02],
                                         rgbaColor=[0.1, 0.1, 0.1, 1.0])
        camera_pos = [robot_pos[0], robot_pos[1], robot_pos[2] + chassis_size[2] + 0.05]
        
        camera_id = p.createMultiBody(baseMass=0.1,
                                    baseVisualShapeIndex=camera_shape,
                                    basePosition=camera_pos)
        
        print("   📷 Camera module added")
    
    def _add_tank_tracks(self, robot_id: int, chassis_size: List[float]):
        """Add tank tracks"""
        robot_pos = p.getBasePositionAndOrientation(robot_id)[0]
        
        # Left track
        left_track_shape = p.createVisualShape(p.GEOM_BOX, 
                                             halfExtents=[chassis_size[0], 0.05, 0.1],
                                             rgbaColor=[0.2, 0.2, 0.2, 1.0])
        left_track_pos = [robot_pos[0], robot_pos[1] - chassis_size[1] - 0.05, robot_pos[2] - 0.1]
        
        left_track_id = p.createMultiBody(baseMass=2.0,
                                        baseVisualShapeIndex=left_track_shape,
                                        basePosition=left_track_pos)
        
        # Right track
        right_track_pos = [robot_pos[0], robot_pos[1] + chassis_size[1] + 0.05, robot_pos[2] - 0.1]
        right_track_id = p.createMultiBody(baseMass=2.0,
                                         baseVisualShapeIndex=left_track_shape,
                                         basePosition=right_track_pos)
        
        print("   🚂 Tank tracks added")
    
    def _add_tank_equipment(self, robot_id: int, chassis_size: List[float]):
        """Add military-style equipment"""
        robot_pos = p.getBasePositionAndOrientation(robot_id)[0]
        
        # Turret
        turret_shape = p.createVisualShape(p.GEOM_CYLINDER, radius=0.15, length=0.1,
                                         rgbaColor=[0.4, 0.4, 0.4, 1.0])
        turret_pos = [robot_pos[0], robot_pos[1], robot_pos[2] + chassis_size[2] + 0.1]
        
        turret_id = p.createMultiBody(baseMass=1.0,
                                    baseVisualShapeIndex=turret_shape,
                                    basePosition=turret_pos)
        
        print("   🛡️ Turret added")
    
    def _add_rover_wheels(self, robot_id: int, chassis_size: List[float]):
        """Add 6-wheel rover suspension"""
        robot_pos = p.getBasePositionAndOrientation(robot_id)[0]
        
        # 6 wheels for rover
        wheel_positions = [
            [chassis_size[0] * 0.8, chassis_size[1] + 0.1, -chassis_size[2]],    # Front right
            [chassis_size[0] * 0.8, -(chassis_size[1] + 0.1), -chassis_size[2]], # Front left
            [0, chassis_size[1] + 0.1, -chassis_size[2]],                       # Middle right
            [0, -(chassis_size[1] + 0.1), -chassis_size[2]],                    # Middle left
            [-chassis_size[0] * 0.8, chassis_size[1] + 0.1, -chassis_size[2]],  # Back right
            [-chassis_size[0] * 0.8, -(chassis_size[1] + 0.1), -chassis_size[2]] # Back left
        ]
        
        for i, (x, y, z) in enumerate(wheel_positions):
            wheel_shape = p.createVisualShape(p.GEOM_CYLINDER, radius=0.12, length=0.06,
                                            rgbaColor=[0.3, 0.3, 0.3, 1.0])
            wheel_pos = [robot_pos[0] + x, robot_pos[1] + y, robot_pos[2] + z]
            
            wheel_id = p.createMultiBody(baseMass=1.5,
                                       baseVisualShapeIndex=wheel_shape,
                                       basePosition=wheel_pos)
        
        print("   🚀 6-wheel suspension system added")
    
    def _add_rover_equipment(self, robot_id: int, chassis_size: List[float]):
        """Add scientific equipment to rover"""
        robot_pos = p.getBasePositionAndOrientation(robot_id)[0]
        
        # Mast with cameras
        mast_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.02, 0.02, 0.3],
                                       rgbaColor=[0.9, 0.9, 0.9, 1.0])
        mast_pos = [robot_pos[0] + chassis_size[0] * 0.3, robot_pos[1], 
                   robot_pos[2] + chassis_size[2] + 0.3]
        
        mast_id = p.createMultiBody(baseMass=0.5,
                                  baseVisualShapeIndex=mast_shape,
                                  basePosition=mast_pos)
        
        # Solar panels
        panel_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.4, 0.3, 0.01],
                                        rgbaColor=[0.1, 0.1, 0.8, 1.0])  # Blue panels
        panel_pos = [robot_pos[0], robot_pos[1], robot_pos[2] + chassis_size[2] + 0.15]
        
        panel_id = p.createMultiBody(baseMass=0.3,
                                   baseVisualShapeIndex=panel_shape,
                                   basePosition=panel_pos)
        
        print("   🔬 Scientific equipment added")
        print("   ☀️ Solar panels installed")
    
    def _add_humanoid_parts(self, robot_id: int):
        """Add humanoid body parts"""
        robot_pos = p.getBasePositionAndOrientation(robot_id)[0]
        
        # Head
        head_shape = p.createVisualShape(p.GEOM_SPHERE, radius=0.1,
                                       rgbaColor=[0.8, 0.7, 0.6, 1.0])  # Skin tone
        head_pos = [robot_pos[0], robot_pos[1], robot_pos[2] + 0.4]
        
        head_id = p.createMultiBody(baseMass=2.0,
                                  baseVisualShapeIndex=head_shape,
                                  basePosition=head_pos)
        
        print("   🤖 Humanoid features added")
    
    def _add_custom_part(self, robot_id: int, part_config: Dict):
        """Add a custom part based on configuration"""
        part_type = part_config.get('type', 'box')
        size = part_config.get('size', [0.1, 0.1, 0.1])
        color = part_config.get('color', [0.5, 0.5, 0.5, 1.0])
        position = part_config.get('position', [0, 0, 0.2])
        
        robot_pos = p.getBasePositionAndOrientation(robot_id)[0]
        
        if part_type == 'box':
            shape = p.createVisualShape(p.GEOM_BOX, halfExtents=size, rgbaColor=color)
        elif part_type == 'cylinder':
            shape = p.createVisualShape(p.GEOM_CYLINDER, radius=size[0], length=size[1], rgbaColor=color)
        elif part_type == 'sphere':
            shape = p.createVisualShape(p.GEOM_SPHERE, radius=size[0], rgbaColor=color)
        else:
            shape = p.createVisualShape(p.GEOM_BOX, halfExtents=size, rgbaColor=color)
        
        part_pos = [robot_pos[0] + position[0], robot_pos[1] + position[1], robot_pos[2] + position[2]]
        
        part_id = p.createMultiBody(baseMass=0.1,
                                  baseVisualShapeIndex=shape,
                                  basePosition=part_pos)
        
        print(f"   ⚙️ Custom {part_type} part added")

def get_robot_presets():
    """Get predefined robot configurations"""
    return {
        'compact_car': {
            'model_type': 'car',
            'chassis_size': [0.3, 0.15, 0.08],
            'chassis_color': [1.0, 0.2, 0.2, 1.0],  # Red
            'wheel_radius': 0.08
        },
        'heavy_truck': {
            'model_type': 'car', 
            'chassis_size': [0.6, 0.25, 0.15],
            'chassis_color': [0.1, 0.1, 0.1, 1.0],  # Black
            'wheel_radius': 0.15
        },
        'military_tank': {
            'model_type': 'tank',
            'chassis_size': [0.7, 0.4, 0.2],
            'chassis_color': [0.2, 0.4, 0.2, 1.0]  # Dark green
        },
        'mars_rover': {
            'model_type': 'rover',
            'chassis_size': [0.8, 0.5, 0.15],
            'chassis_color': [0.9, 0.9, 0.9, 1.0]  # Silver
        },
        'racing_car': {
            'model_type': 'car',
            'chassis_size': [0.5, 0.18, 0.06],
            'chassis_color': [1.0, 0.8, 0.0, 1.0],  # Gold
            'wheel_radius': 0.12
        }
    }

if __name__ == "__main__":
    print("🤖 Custom Robot Models Module")
    print("Available robot types:")
    factory = RobotModelFactory()
    for model_type in factory.robot_models.keys():
        print(f"  - {model_type}")
    
    print("\nAvailable presets:")
    presets = get_robot_presets()
    for preset_name in presets.keys():
        print(f"  - {preset_name}")
