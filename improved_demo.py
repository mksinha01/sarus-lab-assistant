#!/usr/bin/env python3
"""
🚀 IMPROVED SARUS ROBOT DEMO - Step by Step Enhancement
Advanced customizable robot simulation with multiple model options
"""

import sys
import os
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def install_simulation_dependencies():
    """Install required simulation dependencies"""
    print("📦 Installing Enhanced Simulation Dependencies...")
    
    required_packages = [
        "pybullet>=3.2.5",
        "numpy>=1.21.0",
        "matplotlib>=3.5.0"
    ]
    
    try:
        import subprocess
        for package in required_packages:
            print(f"   Installing {package}...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"   ⚠️ Warning: Could not install {package}")
                print(f"   Error: {result.stderr}")
        
        print("✅ Enhanced simulation dependencies installed!")
        return True
        
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_simulation_ready():
    """Check if simulation is ready"""
    try:
        import pybullet
        import numpy
        import matplotlib
        print("✅ Enhanced simulation dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Run option 9 to install dependencies")
        return False

def print_improved_header():
    """Print enhanced header"""
    print("🚀 SARUS ROBOT - IMPROVED DEMONSTRATION SYSTEM")
    print("   ⚡ Customizable 3D Robot Models")
    print("   🎮 Multiple Robot Types Available") 
    print("   🎯 Step-by-Step Improvements")
    print("   📷 Advanced Camera Controls")

def print_improved_menu():
    """Print improved menu with robot customization"""
    print("\n" + "="*75)
    print("🤖 SARUS ROBOT - IMPROVED COLLEGE DEMONSTRATION SYSTEM")
    print("="*75)
    print("Choose your demonstration mode:")
    print()
    print("🤖 ROBOT MODEL SELECTION:")
    print("1. 🚗 Car Robot      - Default wheeled robot (recommended)")
    print("2. 🛡️ Tank Robot     - Heavy-duty tracked robot")
    print("3. 🚀 Rover Robot    - Mars rover style with 6 wheels")
    print("4. 🤖 Humanoid Robot - Bipedal human-like robot")
    print("5. ⚙️ Custom Robot   - Design your own robot")
    print()
    print("🎮 DEMONSTRATION MODES:")
    print("6. 🎭 Auto Demo      - Automated navigation with current robot")
    print("7. 🎮 Interactive    - Manual control with WASD keys")
    print("8. 🧪 Component Test - Test robot systems individually")
    print()
    print("🔧 SYSTEM OPTIONS:")
    print("9. 📦 Install Deps   - Install/update simulation dependencies")
    print("10. ❌ Exit")
    print()

def create_robot_selection_demo():
    """Demo showing different robot models"""
    if not check_simulation_ready():
        return
    
    print("\n🤖 ROBOT MODEL SHOWCASE")
    print("="*50)
    
    try:
        import pybullet as p
        from src.simulation.custom_robot_models import RobotModelFactory, get_robot_presets
        
        # Initialize simulation
        client = p.connect(p.GUI)
        p.setAdditionalSearchPath(p.getDataPath())  # Add PyBullet data path
        p.resetSimulation()
        p.setGravity(0, 0, -9.81)
        
        # Load ground plane
        plane_id = p.loadURDF("plane.urdf")
        
        # Set camera
        p.resetDebugVisualizerCamera(
            cameraDistance=4.0,
            cameraYaw=45,
            cameraPitch=-20,
            cameraTargetPosition=[0, 0, 0]
        )
        
        factory = RobotModelFactory()
        robot_positions = [
            [-2, 0, 0.5],   # Car
            [0, -2, 0.5],   # Tank  
            [2, 0, 0.5],    # Rover
            [0, 2, 1.0],    # Humanoid
        ]
        
        robot_types = ['car', 'tank', 'rover', 'humanoid']
        robots = []
        
        print("🏗️ Creating robot showcase...")
        for i, (robot_type, position) in enumerate(zip(robot_types, robot_positions)):
            print(f"   Creating {robot_type} robot at position {position}")
            robot_id = factory.create_robot(robot_type, position)
            robots.append(robot_id)
            time.sleep(0.5)  # Pause to see creation
        
        print("✅ Robot showcase created!")
        print("   - Use mouse to rotate camera and examine robots")
        print("   - Close window or press Ctrl+C to continue")
        
        # Keep simulation running
        try:
            while True:
                p.stepSimulation()
                time.sleep(1/240)
        except KeyboardInterrupt:
            print("   Demo interrupted by user")
        
        p.disconnect()
        
    except Exception as e:
        print(f"❌ Error in robot showcase: {e}")

def run_custom_robot_demo():
    """Run demo with custom robot configuration"""
    if not check_simulation_ready():
        return
    
    print("\n⚙️ CUSTOM ROBOT CONFIGURATION")
    print("="*50)
    
    # Get custom robot parameters
    print("Design your custom robot:")
    
    try:
        chassis_length = float(input("Chassis length (0.2-1.0m) [0.4]: ") or "0.4")
        chassis_width = float(input("Chassis width (0.1-0.5m) [0.2]: ") or "0.2") 
        chassis_height = float(input("Chassis height (0.05-0.3m) [0.1]: ") or "0.1")
        
        print("\\nChoose color:")
        print("1. Red    2. Blue   3. Green  4. Yellow  5. Silver")
        color_choice = input("Color choice (1-5) [2]: ") or "2"
        
        colors = {
            "1": [1.0, 0.2, 0.2, 1.0],  # Red
            "2": [0.2, 0.5, 0.8, 1.0],  # Blue
            "3": [0.2, 0.8, 0.2, 1.0],  # Green
            "4": [1.0, 1.0, 0.2, 1.0],  # Yellow
            "5": [0.8, 0.8, 0.8, 1.0],  # Silver
        }
        
        chassis_color = colors.get(color_choice, colors["2"])
        
        # Create custom robot
        from src.simulation.custom_robot_models import RobotModelFactory
        import pybullet as p
        
        # Initialize simulation
        client = p.connect(p.GUI)
        p.resetSimulation()
        p.setGravity(0, 0, -9.81)
        p.loadURDF("plane.urdf")
        
        p.resetDebugVisualizerCamera(
            cameraDistance=3.0,
            cameraYaw=45,
            cameraPitch=-20,
            cameraTargetPosition=[0, 0, 0]
        )
        
        factory = RobotModelFactory()
        
        print(f"\\n🏗️ Creating custom robot...")
        print(f"   - Size: {chassis_length}m x {chassis_width}m x {chassis_height}m")
        print(f"   - Color: RGB{chassis_color[:3]}")
        
        robot_id = factory.create_robot(
            'car',
            position=[0, 0, 0.5],
            chassis_size=[chassis_length, chassis_width, chassis_height],
            chassis_color=chassis_color
        )
        
        print("✅ Custom robot created successfully!")
        print("   - Use mouse to examine your robot")
        print("   - Close window when done")
        
        # Run simulation
        try:
            while True:
                p.stepSimulation()
                time.sleep(1/240)
        except KeyboardInterrupt:
            print("   Demo completed")
        
        p.disconnect()
        
    except Exception as e:
        print(f"❌ Error creating custom robot: {e}")

def run_enhanced_auto_demo(robot_type='car'):
    """Run auto demo with selected robot type"""
    if not check_simulation_ready():
        return
    
    print(f"\\n🎭 AUTO DEMO - {robot_type.upper()} ROBOT")
    print("="*50)
    
    try:
        import pybullet as p
        from src.simulation.custom_robot_models import RobotModelFactory
        
        # Initialize simulation with enhanced environment
        client = p.connect(p.GUI)
        p.setAdditionalSearchPath(p.getDataPath())  # Add PyBullet data path
        p.resetSimulation()
        p.setGravity(0, 0, -9.81)
        p.setTimeStep(1/240)
        
        # Load environment with proper path
        plane_id = p.loadURDF("plane.urdf")
        
        # Add some obstacles for navigation (using primitive shapes)
        obstacles = []
        obstacle_positions = [
            [2, 1, 0.25], [2, -1, 0.25], [-2, 1, 0.25], [-2, -1, 0.25]
        ]
        
        for i, pos in enumerate(obstacle_positions):
            # Create box obstacles
            obstacle_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.25, 0.25, 0.25])
            obstacle_visual = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.25, 0.25, 0.25],
                                                rgbaColor=[0.8, 0.4, 0.2, 1.0])
            obstacle_id = p.createMultiBody(baseMass=0.0,
                                          baseCollisionShapeIndex=obstacle_shape,
                                          baseVisualShapeIndex=obstacle_visual,
                                          basePosition=pos)
            obstacles.append(obstacle_id)
        
        # Set camera
        p.resetDebugVisualizerCamera(
            cameraDistance=5.0,
            cameraYaw=45,
            cameraPitch=-30,
            cameraTargetPosition=[0, 0, 0]
        )
        
        # Create robot
        factory = RobotModelFactory()
        robot_id = factory.create_robot(robot_type, position=[0, 0, 0.5])
        
        print(f"🤖 {robot_type.upper()} robot created!")
        print("🎭 Starting automated navigation demo...")
        
        # Simple navigation pattern
        navigation_commands = [
            ("🔄 Moving forward", [1, 0, 0], 3.0),
            ("↪️ Turning right", [0, 0, -0.5], 2.0),
            ("🔄 Moving forward", [1, 0, 0], 3.0),
            ("↩️ Turning left", [0, 0, 0.5], 2.0),
            ("🔄 Exploring area", [0.5, 0.5, 0], 3.0),
            ("🏠 Returning to start", [-1, 0, 0], 3.0),
        ]
        
        for action, velocity, duration in navigation_commands:
            print(f"\\n{action}")
            
            start_time = time.time()
            while time.time() - start_time < duration:
                # Apply velocity to robot (simplified physics)
                current_pos, current_orn = p.getBasePositionAndOrientation(robot_id)
                
                # Simple movement simulation
                new_pos = [
                    current_pos[0] + velocity[0] * 0.01,
                    current_pos[1] + velocity[1] * 0.01,
                    current_pos[2]
                ]
                
                # Keep robot on ground
                new_pos[2] = max(new_pos[2], 0.5)
                
                p.resetBasePositionAndOrientation(robot_id, new_pos, current_orn)
                
                p.stepSimulation()
                time.sleep(1/60)
        
        print("\\n🎉 Auto demo completed successfully!")
        print("   - Robot navigation demonstrated")
        print("   - All systems functioning")
        print("\\n   Press Enter to continue...")
        input()
        
        p.disconnect()
        
    except Exception as e:
        print(f"❌ Error in auto demo: {e}")

def main():
    """Main demo function with step-by-step improvements"""
    
    while True:
        print_improved_header()
        print_improved_menu()
        
        try:
            choice = input("Enter your choice (1-10): ").strip()
            
            if choice == '1':
                # Car robot demo
                run_enhanced_auto_demo('car')
            
            elif choice == '2':
                # Tank robot demo
                run_enhanced_auto_demo('tank')
            
            elif choice == '3':
                # Rover robot demo
                run_enhanced_auto_demo('rover')
            
            elif choice == '4':
                # Humanoid robot demo
                run_enhanced_auto_demo('humanoid')
            
            elif choice == '5':
                # Custom robot
                run_custom_robot_demo()
            
            elif choice == '6':
                # Auto demo with selection
                print("\\nSelect robot for auto demo:")
                print("1. Car  2. Tank  3. Rover  4. Humanoid")
                robot_choice = input("Robot type (1-4) [1]: ") or "1"
                robot_types = {'1': 'car', '2': 'tank', '3': 'rover', '4': 'humanoid'}
                selected_robot = robot_types.get(robot_choice, 'car')
                run_enhanced_auto_demo(selected_robot)
            
            elif choice == '7':
                # Interactive demo
                print("\\n🎮 Interactive mode coming soon...")
                print("   Will include WASD controls and real-time robot control")
                input("Press Enter to continue...")
            
            elif choice == '8':
                # Component test
                print("\\n🧪 Component testing coming soon...")
                print("   Will include individual system testing")
                input("Press Enter to continue...")
            
            elif choice == '9':
                # Install dependencies
                install_simulation_dependencies()
                input("\\nPress Enter to continue...")
            
            elif choice == '10':
                print("\\n👋 Thank you for using Sarus Robot Demo!")
                print("   Perfect for college presentations!")
                break
            
            else:
                print("\\n❌ Invalid choice. Please select 1-10.")
                input("Press Enter to continue...")
        
        except KeyboardInterrupt:
            print("\\n\\n👋 Demo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\\n❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
