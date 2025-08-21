"""
Enhanced 3D Simulation World for Sarus Robot
Improved version with better visuals, camera controls, and realistic robot model
"""
import pybullet as p
import pybullet_data
import numpy as np
import time
import math
import os
from typing import Dict, List, Tuple, Optional

class EnhancedSarusSimWorld:
    def __init__(self, gui_mode: bool = True, lab_environment: bool = True):
        """Initialize enhanced simulation world with better visuals"""
        print("🌍 Creating Enhanced 3D Simulation World...")
        
        # Initialize objects dictionary first
        self.objects = {}
        self.robot_id = None
        self.camera_distance = 3.0
        self.camera_yaw = 50
        self.camera_pitch = -35
        self.camera_target = [0, 0, 0]
        self.current_camera_mode = "follow"  # follow, fixed, top_down, first_person
        
        # Connect to physics server with enhanced settings
        if gui_mode:
            self.physics_client = p.connect(p.GUI)
            # Set window title and size
            p.configureDebugVisualizer(p.COV_ENABLE_GUI, 1)
            p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 1)
            p.configureDebugVisualizer(p.COV_ENABLE_WIREFRAME, 0)
            p.configureDebugVisualizer(p.COV_ENABLE_RGB_BUFFER_PREVIEW, 0)
            p.configureDebugVisualizer(p.COV_ENABLE_DEPTH_BUFFER_PREVIEW, 0)
            p.configureDebugVisualizer(p.COV_ENABLE_SEGMENTATION_MARK_PREVIEW, 0)
        else:
            self.physics_client = p.connect(p.DIRECT)
        
        # Set enhanced physics parameters
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        p.setRealTimeSimulation(0)
        
        # Enhanced lighting
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING, 1)
        
        if lab_environment:
            self.setup_enhanced_environment()
        
        # Add camera control buttons
        self.add_camera_controls()
        
        print("🌍 Enhanced 3D Simulation World Created!")
        print("   - GUI Mode: ON" if gui_mode else "   - GUI Mode: OFF")
        print("   - Enhanced Lab Environment: ON" if lab_environment else "   - Basic Environment")
        print("   - Camera Controls: ENABLED")
        print("   - Realistic Physics: ON")

    def add_camera_controls(self):
        """Add interactive camera control buttons"""
        # Camera mode buttons
        self.camera_follow_btn = p.addUserDebugParameter("Follow Camera", 1, 0, 1)
        self.camera_fixed_btn = p.addUserDebugParameter("Fixed Camera", 1, 0, 0)
        self.camera_top_btn = p.addUserDebugParameter("Top View", 1, 0, 0)
        self.camera_first_person_btn = p.addUserDebugParameter("First Person", 1, 0, 0)
        
        # Camera position controls
        self.camera_distance_slider = p.addUserDebugParameter("Camera Distance", 1, 10, 3)
        self.camera_yaw_slider = p.addUserDebugParameter("Camera Yaw", -180, 180, 50)
        self.camera_pitch_slider = p.addUserDebugParameter("Camera Pitch", -89, 89, -35)

    def setup_enhanced_environment(self):
        """Create an enhanced college laboratory environment"""
        # Load enhanced ground plane
        plane_id = p.loadURDF("plane.urdf")
        
        # Change ground color to look like lab floor
        p.changeVisualShape(plane_id, -1, rgbaColor=[0.8, 0.8, 0.9, 1.0])
        self.objects['ground'] = plane_id
        
        # Create lab walls with better materials
        self.create_lab_walls()
        
        # Add lab tables with realistic materials
        self.create_lab_tables()
        
        # Add lab equipment
        self.create_lab_equipment()
        
        # Add lighting
        self.setup_enhanced_lighting()
        
        # Add navigation markers
        self.add_navigation_markers()

    def create_lab_walls(self):
        """Create realistic lab walls"""
        wall_height = 3.0
        wall_thickness = 0.2
        room_size = 10.0
        
        # Wall positions (x, y, z, width, height, depth)
        walls = [
            # Back wall
            (0, room_size/2, wall_height/2, room_size, wall_thickness, wall_height),
            # Front wall  
            (0, -room_size/2, wall_height/2, room_size, wall_thickness, wall_height),
            # Left wall
            (-room_size/2, 0, wall_height/2, wall_thickness, room_size, wall_height),
            # Right wall
            (room_size/2, 0, wall_height/2, wall_thickness, room_size, wall_height),
        ]
        
        for i, (x, y, z, w, h, d) in enumerate(walls):
            wall_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[w/2, h/2, d/2])
            wall_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[w/2, h/2, d/2], 
                                           rgbaColor=[0.9, 0.9, 0.95, 1.0])
            wall_id = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=wall_shape,
                                      baseVisualShapeIndex=wall_visual, basePosition=[x, y, z])
            self.objects[f'wall_{i}'] = wall_id

    def create_lab_tables(self):
        """Create realistic lab tables"""
        table_positions = [
            (2, 2, 0.4),    # Table 1
            (-2, 2, 0.4),   # Table 2  
            (2, -2, 0.4),   # Table 3
            (-2, -2, 0.4),  # Table 4
            (0, 3, 0.4),    # Central table
        ]
        
        for i, (x, y, z) in enumerate(table_positions):
            # Table top
            table_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.8, 0.6, 0.05])
            table_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.8, 0.6, 0.05],
                                             rgbaColor=[0.6, 0.4, 0.2, 1.0])
            table_id = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=table_shape,
                                       baseVisualShapeIndex=table_visual, basePosition=[x, y, z])
            self.objects[f'table_{i}'] = table_id
            
            # Table legs
            leg_positions = [(x-0.7, y-0.5, z-0.2), (x+0.7, y-0.5, z-0.2),
                           (x-0.7, y+0.5, z-0.2), (x+0.7, y+0.5, z-0.2)]
            
            for j, (lx, ly, lz) in enumerate(leg_positions):
                leg_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.2])
                leg_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.2],
                                               rgbaColor=[0.4, 0.2, 0.1, 1.0])
                leg_id = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=leg_shape,
                                         baseVisualShapeIndex=leg_visual, basePosition=[lx, ly, lz])
                self.objects[f'table_{i}_leg_{j}'] = leg_id

    def create_lab_equipment(self):
        """Add lab equipment for realism"""
        # Microscopes
        microscope_pos = [(2, 2, 0.5), (-2, 2, 0.5)]
        for i, (x, y, z) in enumerate(microscope_pos):
            mic_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.2, 0.2, 0.3])
            mic_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.2, 0.2, 0.3],
                                           rgbaColor=[0.1, 0.1, 0.1, 1.0])
            mic_id = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=mic_shape,
                                     baseVisualShapeIndex=mic_visual, basePosition=[x, y, z])
            self.objects[f'microscope_{i}'] = mic_id
        
        # Computers
        computer_pos = [(2, -2, 0.5), (-2, -2, 0.5)]
        for i, (x, y, z) in enumerate(computer_pos):
            comp_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.3, 0.2, 0.25])
            comp_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.3, 0.2, 0.25],
                                            rgbaColor=[0.2, 0.2, 0.2, 1.0])
            comp_id = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=comp_shape,
                                      baseVisualShapeIndex=comp_visual, basePosition=[x, y, z])
            self.objects[f'computer_{i}'] = comp_id

    def setup_enhanced_lighting(self):
        """Setup enhanced lighting for better visuals"""
        # Add multiple light sources for better illumination
        light_positions = [
            [2, 2, 4],     # Corner lights
            [-2, 2, 4],
            [2, -2, 4], 
            [-2, -2, 4],
            [0, 0, 5]      # Central light
        ]
        
        for pos in light_positions:
            p.loadURDF("sphere_small.urdf", pos, globalScaling=0.1)

    def add_navigation_markers(self):
        """Add visual markers to help with navigation"""
        # Start position marker (green)
        start_shape = p.createVisualShape(p.GEOM_CYLINDER, radius=0.2, length=0.1,
                                        rgbaColor=[0, 1, 0, 0.7])
        start_id = p.createMultiBody(baseMass=0, baseVisualShapeIndex=start_shape,
                                   basePosition=[0, 0, 0.05])
        self.objects['start_marker'] = start_id
        
        # Goal markers (red)
        goal_positions = [(3, 3, 0.05), (-3, -3, 0.05)]
        for i, pos in enumerate(goal_positions):
            goal_shape = p.createVisualShape(p.GEOM_CYLINDER, radius=0.15, length=0.08,
                                           rgbaColor=[1, 0, 0, 0.7])
            goal_id = p.createMultiBody(baseMass=0, baseVisualShapeIndex=goal_shape,
                                      basePosition=pos)
            self.objects[f'goal_marker_{i}'] = goal_id

    def create_enhanced_robot(self, position: List[float] = [0, 0, 0.5]) -> int:
        """Create a realistic robot car model"""
        print("🚗 Creating Enhanced Robot Car Model...")
        
        # Robot chassis (main body)
        chassis_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.4, 0.2, 0.1])
        chassis_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.4, 0.2, 0.1],
                                           rgbaColor=[0.2, 0.5, 0.8, 1.0])  # Blue color
        
        # Create robot with enhanced visuals
        robot_id = p.createMultiBody(baseMass=5.0,
                                   baseCollisionShapeIndex=chassis_shape,
                                   baseVisualShapeIndex=chassis_visual,
                                   basePosition=position)
        
        # Add wheels
        self.add_robot_wheels(robot_id)
        
        # Add sensors (visual indicators)
        self.add_robot_sensors(robot_id)
        
        # Add robot camera
        self.add_robot_camera(robot_id)
        
        self.robot_id = robot_id
        self.objects['robot'] = robot_id
        
        print("🚗 Enhanced Robot Car Created!")
        print("   - Realistic chassis design")
        print("   - 4-wheel drive system")
        print("   - Sensor indicators")
        print("   - Onboard camera")
        
        return robot_id

    def add_robot_wheels(self, robot_id: int):
        """Add realistic wheels to the robot"""
        wheel_positions = [
            [0.3, 0.25, 0],    # Front right
            [0.3, -0.25, 0],   # Front left
            [-0.3, 0.25, 0],   # Back right
            [-0.3, -0.25, 0]   # Back left
        ]
        
        for i, (x, y, z) in enumerate(wheel_positions):
            # Wheel visual
            wheel_shape = p.createVisualShape(p.GEOM_CYLINDER, radius=0.1, length=0.05,
                                            rgbaColor=[0.1, 0.1, 0.1, 1.0])
            wheel_collision = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.1, height=0.05)
            
            # Attach wheel to robot (simplified - for visual only)
            robot_pos = p.getBasePositionAndOrientation(robot_id)[0]
            wheel_pos = [robot_pos[0] + x, robot_pos[1] + y, robot_pos[2] + z]
            
            wheel_id = p.createMultiBody(baseMass=0.5,
                                       baseCollisionShapeIndex=wheel_collision,
                                       baseVisualShapeIndex=wheel_shape,
                                       basePosition=wheel_pos)
            
            self.objects[f'wheel_{i}'] = wheel_id

    def add_robot_sensors(self, robot_id: int):
        """Add visual sensor indicators"""
        # Ultrasonic sensor indicators (small cylinders)
        sensor_positions = [
            [0.4, 0, 0.05],     # Front center
            [0.35, 0.15, 0.05], # Front right
            [0.35, -0.15, 0.05] # Front left
        ]
        
        for i, (x, y, z) in enumerate(sensor_positions):
            sensor_shape = p.createVisualShape(p.GEOM_CYLINDER, radius=0.02, length=0.03,
                                             rgbaColor=[1, 1, 0, 1.0])  # Yellow sensors
            robot_pos = p.getBasePositionAndOrientation(robot_id)[0]
            sensor_pos = [robot_pos[0] + x, robot_pos[1] + y, robot_pos[2] + z]
            
            sensor_id = p.createMultiBody(baseMass=0, baseVisualShapeIndex=sensor_shape,
                                        basePosition=sensor_pos)
            self.objects[f'sensor_{i}'] = sensor_id

    def add_robot_camera(self, robot_id: int):
        """Add robot camera visual"""
        # Camera housing
        robot_pos = p.getBasePositionAndOrientation(robot_id)[0]
        camera_pos = [robot_pos[0] + 0.2, robot_pos[1], robot_pos[2] + 0.15]
        
        camera_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.05, 0.05, 0.05],
                                         rgbaColor=[0, 0, 0, 1.0])
        camera_id = p.createMultiBody(baseMass=0, baseVisualShapeIndex=camera_shape,
                                    basePosition=camera_pos)
        self.objects['robot_camera'] = camera_id

    def update_camera(self):
        """Update camera based on current mode and robot position"""
        if self.robot_id is None:
            return
            
        robot_pos, robot_orn = p.getBasePositionAndOrientation(self.robot_id)
        
        # Update camera based on mode
        if self.current_camera_mode == "follow":
            # Follow the robot
            self.camera_target = [robot_pos[0], robot_pos[1], robot_pos[2]]
            p.resetDebugVisualizerCamera(
                cameraDistance=self.camera_distance,
                cameraYaw=self.camera_yaw,
                cameraPitch=self.camera_pitch,
                cameraTargetPosition=self.camera_target
            )
        elif self.current_camera_mode == "top_down":
            # Top-down view
            p.resetDebugVisualizerCamera(
                cameraDistance=8.0,
                cameraYaw=0,
                cameraPitch=-90,
                cameraTargetPosition=[robot_pos[0], robot_pos[1], robot_pos[2]]
            )
        elif self.current_camera_mode == "first_person":
            # First-person view from robot
            p.resetDebugVisualizerCamera(
                cameraDistance=0.5,
                cameraYaw=self.camera_yaw,
                cameraPitch=0,
                cameraTargetPosition=[robot_pos[0] + 1, robot_pos[1], robot_pos[2] + 0.2]
            )

    def check_camera_controls(self):
        """Check and update camera controls"""
        # Check camera mode buttons
        follow = p.readUserDebugParameter(self.camera_follow_btn)
        fixed = p.readUserDebugParameter(self.camera_fixed_btn)
        top = p.readUserDebugParameter(self.camera_top_btn)
        first_person = p.readUserDebugParameter(self.camera_first_person_btn)
        
        if follow > 0.5:
            self.current_camera_mode = "follow"
        elif fixed > 0.5:
            self.current_camera_mode = "fixed"
        elif top > 0.5:
            self.current_camera_mode = "top_down"
        elif first_person > 0.5:
            self.current_camera_mode = "first_person"
        
        # Update camera parameters
        self.camera_distance = p.readUserDebugParameter(self.camera_distance_slider)
        self.camera_yaw = p.readUserDebugParameter(self.camera_yaw_slider)
        self.camera_pitch = p.readUserDebugParameter(self.camera_pitch_slider)
        
        # Update camera
        self.update_camera()

    def get_robot_position(self) -> Tuple[List[float], List[float]]:
        """Get current robot position and orientation"""
        if self.robot_id is None:
            return [0, 0, 0], [0, 0, 0, 1]
        return p.getBasePositionAndOrientation(self.robot_id)

    def move_robot(self, linear_velocity: float, angular_velocity: float):
        """Move robot with enhanced physics"""
        if self.robot_id is None:
            return
            
        # Get current position and orientation
        pos, orn = p.getBasePositionAndOrientation(self.robot_id)
        euler = p.getEulerFromQuaternion(orn)
        
        # Calculate new position
        dt = 1.0/240.0  # PyBullet default timestep
        
        # Forward/backward movement
        new_x = pos[0] + linear_velocity * math.cos(euler[2]) * dt
        new_y = pos[1] + linear_velocity * math.sin(euler[2]) * dt
        
        # Rotation
        new_yaw = euler[2] + angular_velocity * dt
        new_orn = p.getQuaternionFromEuler([0, 0, new_yaw])
        
        # Apply movement
        p.resetBasePositionAndOrientation(self.robot_id, [new_x, new_y, pos[2]], new_orn)
        
        # Update camera
        self.check_camera_controls()

    def step_simulation(self):
        """Step the physics simulation"""
        p.stepSimulation()
        self.check_camera_controls()

    def close(self):
        """Clean up simulation"""
        print("🔄 Cleaning up Enhanced Simulation...")
        p.disconnect()
        print("🔄 Enhanced Simulation cleaned up")

    def reset_robot_position(self, position: List[float] = [0, 0, 0.5]):
        """Reset robot to starting position"""
        if self.robot_id is not None:
            p.resetBasePositionAndOrientation(self.robot_id, position, [0, 0, 0, 1])
            print(f"🔄 Robot reset to position: {position}")

    def get_obstacle_detection(self) -> Dict[str, bool]:
        """Enhanced obstacle detection using ray casting"""
        if self.robot_id is None:
            return {}
            
        pos, orn = p.getBasePositionAndOrientation(self.robot_id)
        euler = p.getEulerFromQuaternion(orn)
        
        # Ray casting directions (relative to robot)
        ray_directions = {
            'front_left': math.radians(30),
            'front_center': 0,
            'front_right': math.radians(-30),
            'left': math.radians(90),
            'right': math.radians(-90)
        }
        
        obstacles = {}
        ray_length = 1.0
        
        for direction_name, angle_offset in ray_directions.items():
            # Calculate ray direction
            total_angle = euler[2] + angle_offset
            end_x = pos[0] + ray_length * math.cos(total_angle)
            end_y = pos[1] + ray_length * math.sin(total_angle)
            end_z = pos[2]
            
            # Cast ray
            ray_result = p.rayTest(pos, [end_x, end_y, end_z])
            
            # Check if ray hit something
            if ray_result[0][0] != -1:  # Hit detected
                hit_distance = ray_result[0][2] * ray_length
                obstacles[direction_name] = hit_distance < 0.8  # Obstacle within 0.8 units
            else:
                obstacles[direction_name] = False
        
        return obstacles

if __name__ == "__main__":
    # Test the enhanced simulation
    print("🧪 Testing Enhanced Simulation World...")
    world = EnhancedSarusSimWorld(gui_mode=True, lab_environment=True)
    robot_id = world.create_enhanced_robot()
    
    print("🎮 Enhanced simulation running... Press Ctrl+C to exit")
    try:
        while True:
            world.step_simulation()
            time.sleep(1/60)  # 60 FPS
    except KeyboardInterrupt:
        print("👋 Stopping enhanced simulation...")
        world.close()
