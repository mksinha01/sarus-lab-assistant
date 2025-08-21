"""
3D Simulation World for Sarus Robot - College Demonstration
Creates a realistic 3D lab environment with physics simulation
"""
import pybullet as p
import pybullet_data
import numpy as np
import time
import math
from pathlib import Path
import os

class SarusSimWorld:
    """3D simulation world for Sarus robot demonstration"""
    
    def __init__(self, gui=True, lab_environment=True):
        self.gui = gui
        self.lab_environment = lab_environment
        
        # Connect to PyBullet
        if gui:
            self.client = p.connect(p.GUI)
            p.configureDebugVisualizer(p.COV_ENABLE_GUI, 1)
            p.configureDebugVisualizer(p.COV_ENABLE_SHADOWS, 1)
            p.configureDebugVisualizer(p.COV_ENABLE_WIREFRAME, 0)
            # Set better camera view for demo
            p.resetDebugVisualizerCamera(
                cameraDistance=3.0,
                cameraYaw=45,
                cameraPitch=-20,
                cameraTargetPosition=[0, 0, 0]
            )
        else:
            self.client = p.connect(p.DIRECT)
        
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.resetSimulation()
        p.setGravity(0, 0, -9.81)
        p.setTimeStep(1/240)  # High precision simulation
        
        # Create environment
        self.setup_environment()
        
        # Create robot
        self.robot_id = self.create_sarus_robot()
        self.robot_position = [0, 0, 0.1]
        self.robot_orientation = [0, 0, 0]
        
        # Robot state
        self.left_wheel_speed = 0.0
        self.right_wheel_speed = 0.0
        self.wheel_base = 0.25  # Distance between wheels
        
        # Simulation state
        self.simulation_time = 0
        self.objects = {}
        self.sensors = {}
        self.step_count = 0
        
        print("🌍 3D Simulation World Created for College Demo!")
        print(f"   - GUI Mode: {'ON' if gui else 'OFF'}")
        print(f"   - Lab Environment: {'ON' if lab_environment else 'OFF'}")
    
    def setup_environment(self):
        """Create a realistic college lab environment"""
        # Floor with grid pattern
        self.plane_id = p.loadURDF("plane.urdf")
        p.changeVisualShape(self.plane_id, -1, rgbaColor=[0.9, 0.9, 0.95, 1])
        
        if self.lab_environment:
            self.create_college_lab()
    
    def create_college_lab(self):
        """Create college laboratory environment"""
        # Lab tables
        table_positions = [
            [2.5, 1.5, 0], [2.5, -1.5, 0], 
            [-2.5, 1.5, 0], [-2.5, -1.5, 0],
            [0, 3, 0], [0, -3, 0]
        ]
        
        for i, pos in enumerate(table_positions):
            # Create table
            table_top = self.create_box(
                position=[pos[0], pos[1], 0.75],
                size=[0.8, 0.6, 0.05],
                color=[0.8, 0.6, 0.4, 1],
                mass=0  # Static
            )
            
            # Table legs
            leg_positions = [
                [pos[0] + 0.35, pos[1] + 0.25, 0.375],
                [pos[0] - 0.35, pos[1] + 0.25, 0.375],
                [pos[0] + 0.35, pos[1] - 0.25, 0.375],
                [pos[0] - 0.35, pos[1] - 0.25, 0.375]
            ]
            
            for leg_pos in leg_positions:
                self.create_box(
                    position=leg_pos,
                    size=[0.05, 0.05, 0.375],
                    color=[0.6, 0.4, 0.2, 1],
                    mass=0
                )
            
            self.objects[f"table_{i}"] = table_top
        
        # Lab equipment on tables
        equipment = [
            {"name": "oscilloscope", "pos": [2.5, 1.5, 0.85], "size": [0.3, 0.25, 0.15], "color": [0.2, 0.2, 0.3, 1]},
            {"name": "multimeter", "pos": [2.5, -1.5, 0.82], "size": [0.15, 0.12, 0.08], "color": [1, 0.8, 0.1, 1]},
            {"name": "computer", "pos": [-2.5, 1.5, 0.85], "size": [0.35, 0.25, 0.25], "color": [0.1, 0.1, 0.15, 1]},
            {"name": "microscope", "pos": [-2.5, -1.5, 0.82], "size": [0.2, 0.2, 0.3], "color": [0.7, 0.7, 0.8, 1]},
            {"name": "power_supply", "pos": [0, 3, 0.82], "size": [0.25, 0.2, 0.12], "color": [0.3, 0.3, 0.4, 1]},
            {"name": "signal_generator", "pos": [0, -3, 0.82], "size": [0.3, 0.2, 0.1], "color": [0.2, 0.4, 0.6, 1]}
        ]
        
        for item in equipment:
            obj_id = self.create_box(
                position=item["pos"],
                size=item["size"],
                color=item["color"],
                mass=0.5
            )
            self.objects[item["name"]] = obj_id
        
        # Walls
        wall_data = [
            {"pos": [0, 4.5, 1.5], "size": [5, 0.1, 1.5], "color": [0.9, 0.9, 0.95, 1]},  # Back wall
            {"pos": [4.5, 0, 1.5], "size": [0.1, 4.5, 1.5], "color": [0.9, 0.9, 0.95, 1]},  # Right wall
            {"pos": [-4.5, 0, 1.5], "size": [0.1, 4.5, 1.5], "color": [0.9, 0.9, 0.95, 1]}   # Left wall
        ]
        
        for wall in wall_data:
            wall_id = self.create_box(
                position=wall["pos"],
                size=wall["size"],
                color=wall["color"],
                mass=0
            )
            self.objects[f"wall_{len(self.objects)}"] = wall_id
        
        # Add some obstacles for navigation demo
        obstacles = [
            {"pos": [1, 0, 0.25], "size": [0.2, 0.2, 0.25], "color": [0.8, 0.2, 0.2, 1]},
            {"pos": [-1, 1, 0.15], "size": [0.15, 0.15, 0.15], "color": [0.2, 0.8, 0.2, 1]},
            {"pos": [0.5, -1.5, 0.2], "size": [0.3, 0.1, 0.2], "color": [0.2, 0.2, 0.8, 1]}
        ]
        
        for i, obs in enumerate(obstacles):
            obs_id = self.create_box(
                position=obs["pos"],
                size=obs["size"],
                color=obs["color"],
                mass=1
            )
            self.objects[f"obstacle_{i}"] = obs_id
    
    def create_box(self, position, size, color, mass=1):
        """Helper function to create boxes"""
        collision_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=size)
        visual_shape = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=size,
            rgbaColor=color
        )
        
        return p.createMultiBody(
            baseMass=mass,
            baseCollisionShapeIndex=collision_shape,
            baseVisualShapeIndex=visual_shape,
            basePosition=position
        )
    
    def create_sarus_robot(self):
        """Create a detailed 3D representation of Sarus robot"""
        # Robot base (main body)
        base_size = [0.15, 0.12, 0.08]
        base_collision = p.createCollisionShape(p.GEOM_BOX, halfExtents=base_size)
        base_visual = p.createVisualShape(
            p.GEOM_BOX, 
            halfExtents=base_size,
            rgbaColor=[0.2, 0.6, 0.9, 1]  # Sarus blue
        )
        
        # Create main robot body
        robot = p.createMultiBody(
            baseMass=3.0,
            baseCollisionShapeIndex=base_collision,
            baseVisualShapeIndex=base_visual,
            basePosition=[0, 0, 0.1]
        )
        
        # Add Raspberry Pi box on top
        pi_visual = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=[0.045, 0.03, 0.005],
            rgbaColor=[0.1, 0.8, 0.1, 1]
        )
        pi_id = p.createMultiBody(
            baseMass=0.1,
            baseVisualShapeIndex=pi_visual,
            basePosition=[0, 0, 0.19]
        )
        
        # Add camera module
        camera_visual = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=[0.02, 0.02, 0.01],
            rgbaColor=[0.1, 0.1, 0.1, 1]
        )
        camera_id = p.createMultiBody(
            baseMass=0.05,
            baseVisualShapeIndex=camera_visual,
            basePosition=[0.15, 0, 0.15]
        )
        
        # Add ultrasonic sensors
        sensor_positions = [
            [0.15, 0.08, 0.12],   # Front right
            [0.15, 0, 0.12],      # Front center  
            [0.15, -0.08, 0.12]   # Front left
        ]
        
        for i, sensor_pos in enumerate(sensor_positions):
            sensor_visual = p.createVisualShape(
                p.GEOM_CYLINDER,
                radius=0.01,
                length=0.02,
                rgbaColor=[0.7, 0.7, 0.7, 1]
            )
            sensor_id = p.createMultiBody(
                baseMass=0.02,
                baseVisualShapeIndex=sensor_visual,
                basePosition=sensor_pos
            )
        
        # Add wheels (visual only)
        wheel_positions = [
            [0.05, 0.15, 0.05],   # Right wheel
            [0.05, -0.15, 0.05]   # Left wheel
        ]
        
        for wheel_pos in wheel_positions:
            wheel_visual = p.createVisualShape(
                p.GEOM_CYLINDER,
                radius=0.06,
                length=0.03,
                rgbaColor=[0.1, 0.1, 0.1, 1]
            )
            wheel_id = p.createMultiBody(
                baseMass=0.2,
                baseVisualShapeIndex=wheel_visual,
                basePosition=wheel_pos
            )
        
        # Add caster wheel
        caster_visual = p.createVisualShape(
            p.GEOM_SPHERE,
            radius=0.03,
            rgbaColor=[0.3, 0.3, 0.3, 1]
        )
        caster_id = p.createMultiBody(
            baseMass=0.1,
            baseVisualShapeIndex=caster_visual,
            basePosition=[-0.12, 0, 0.05]
        )
        
        return robot
    
    def set_motor_speeds(self, left_speed, right_speed):
        """Set motor speeds for differential drive"""
        self.left_wheel_speed = max(-1.0, min(1.0, left_speed))
        self.right_wheel_speed = max(-1.0, min(1.0, right_speed))
    
    def update_robot_movement(self, dt=1/240):
        """Update robot position based on motor speeds"""
        # Get current position and orientation
        pos, orn = p.getBasePositionAndOrientation(self.robot_id)
        euler = p.getEulerFromQuaternion(orn)
        
        # Calculate movement based on differential drive
        v_left = self.left_wheel_speed * 0.5  # Max speed 0.5 m/s
        v_right = self.right_wheel_speed * 0.5
        
        # Robot kinematics
        v_linear = (v_left + v_right) / 2.0
        v_angular = (v_right - v_left) / self.wheel_base
        
        # Update position
        yaw = euler[2]
        new_x = pos[0] + v_linear * math.cos(yaw) * dt
        new_y = pos[1] + v_linear * math.sin(yaw) * dt
        new_yaw = yaw + v_angular * dt
        
        # Apply new position and orientation
        new_orn = p.getQuaternionFromEuler([0, 0, new_yaw])
        p.resetBasePositionAndOrientation(
            self.robot_id, 
            [new_x, new_y, pos[2]], 
            new_orn
        )
    
    def get_ultrasonic_distance(self, sensor_angle=0.0, max_distance=2.0):
        """Simulate ultrasonic sensor readings"""
        pos, orn = p.getBasePositionAndOrientation(self.robot_id)
        euler = p.getEulerFromQuaternion(orn)
        
        # Calculate ray start and end points
        yaw = euler[2] + sensor_angle
        start_pos = [pos[0] + 0.15*math.cos(euler[2]), 
                    pos[1] + 0.15*math.sin(euler[2]), 
                    pos[2] + 0.1]
        end_pos = [start_pos[0] + max_distance*math.cos(yaw),
                  start_pos[1] + max_distance*math.sin(yaw),
                  start_pos[2]]
        
        # Cast ray
        hit_info = p.rayTest(start_pos, end_pos)[0]
        
        if hit_info[0] == -1:  # No collision
            return max_distance
        else:
            hit_pos = hit_info[3]
            distance = math.sqrt(
                (hit_pos[0] - start_pos[0])**2 + 
                (hit_pos[1] - start_pos[1])**2
            )
            return distance
    
    def get_robot_pose(self):
        """Get robot position and orientation"""
        pos, orn = p.getBasePositionAndOrientation(self.robot_id)
        euler = p.getEulerFromQuaternion(orn)
        return {
            'position': {'x': pos[0], 'y': pos[1], 'z': pos[2]},
            'orientation': {'roll': euler[0], 'pitch': euler[1], 'yaw': euler[2]}
        }
    
    def get_camera_image(self, width=640, height=480):
        """Simulate camera image from robot perspective"""
        pos, orn = p.getBasePositionAndOrientation(self.robot_id)
        euler = p.getEulerFromQuaternion(orn)
        
        # Camera position (front of robot)
        camera_pos = [
            pos[0] + 0.15 * math.cos(euler[2]),
            pos[1] + 0.15 * math.sin(euler[2]),
            pos[2] + 0.1
        ]
        
        # Target position (looking forward)
        target_pos = [
            camera_pos[0] + math.cos(euler[2]),
            camera_pos[1] + math.sin(euler[2]),
            camera_pos[2]
        ]
        
        # Get camera image
        view_matrix = p.computeViewMatrix(
            cameraEyePosition=camera_pos,
            cameraTargetPosition=target_pos,
            cameraUpVector=[0, 0, 1]
        )
        
        proj_matrix = p.computeProjectionMatrixFOV(
            fov=60, aspect=width/height, nearVal=0.1, farVal=5.0
        )
        
        _, _, rgb_img, _, _ = p.getCameraImage(
            width, height, view_matrix, proj_matrix
        )
        
        return np.array(rgb_img[:, :, :3])  # Remove alpha channel
    
    def step(self):
        """Step the simulation forward"""
        self.update_robot_movement()
        p.stepSimulation()
        self.simulation_time += 1/240
        self.step_count += 1
        
        # Add some visual effects for demo
        if self.step_count % 60 == 0:  # Every second
            self.add_debug_info()
    
    def add_debug_info(self):
        """Add debug information for demonstration"""
        if self.gui:
            # Clear previous debug info
            p.removeAllUserDebugItems()
            
            # Show robot status
            pos = self.get_robot_pose()['position']
            
            # Speed indicators
            speed_text = f"Speeds: L={self.left_wheel_speed:.2f}, R={self.right_wheel_speed:.2f}"
            p.addUserDebugText(
                speed_text,
                [pos['x'], pos['y'], pos['z'] + 0.3],
                textColorRGB=[1, 1, 1],
                textSize=1.2,
                lifeTime=1
            )
            
            # Sensor rays
            for angle in [-0.5, 0, 0.5]:
                distance = self.get_ultrasonic_distance(angle)
                robot_pos, robot_orn = p.getBasePositionAndOrientation(self.robot_id)
                euler = p.getEulerFromQuaternion(robot_orn)
                
                start = [robot_pos[0] + 0.15*math.cos(euler[2]), 
                        robot_pos[1] + 0.15*math.sin(euler[2]), 
                        robot_pos[2] + 0.1]
                
                end = [start[0] + distance*math.cos(euler[2] + angle),
                      start[1] + distance*math.sin(euler[2] + angle),
                      start[2]]
                
                color = [1, 0, 0] if distance < 0.5 else [0, 1, 0]
                p.addUserDebugLine(start, end, lineColorRGB=color, lineWidth=2, lifeTime=1)
    
    def cleanup(self):
        """Clean up simulation"""
        p.disconnect()
        print("🔄 Simulation cleaned up")

# Demo function
def run_demo():
    """Run a simple demonstration"""
    world = SarusSimWorld(gui=True, lab_environment=True)
    
    print("🎭 Starting College Demo...")
    print("   - Use arrow keys or commands to control robot")
    print("   - Robot will navigate around lab equipment")
    
    try:
        # Demo movement pattern
        demo_commands = [
            (0.5, 0.5, 2),    # Move forward
            (0.3, -0.3, 1),   # Turn right  
            (0.5, 0.5, 2),    # Move forward
            (-0.3, 0.3, 1),   # Turn left
            (0.5, 0.5, 1),    # Move forward
            (0, 0, 1)         # Stop
        ]
        
        for left, right, duration in demo_commands:
            world.set_motor_speeds(left, right)
            start_time = time.time()
            
            while time.time() - start_time < duration:
                world.step()
                time.sleep(1/60)  # 60 FPS
            
        world.set_motor_speeds(0, 0)  # Stop
        
        # Keep simulation running
        print("Demo complete! Simulation will continue running...")
        while True:
            world.step()
            time.sleep(1/60)
            
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")
    finally:
        world.cleanup()

if __name__ == "__main__":
    run_demo()
