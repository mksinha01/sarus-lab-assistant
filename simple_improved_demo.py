#!/usr/bin/env python3
"""
🚀 SIMPLE IMPROVED SARUS ROBOT DEMO
Step-by-step robot model customization demo
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_dependencies():
    """Check simulation dependencies"""
    try:
        import pybullet
        import numpy
        print("✅ Dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def show_robot_models():
    """Demo showing different robot models"""
    if not check_dependencies():
        return
    
    print("🤖 ROBOT MODEL SHOWCASE")
    print("=" * 40)
    
    try:
        import pybullet as p
        import pybullet_data
        from src.simulation.custom_robot_models import RobotModelFactory
        
        # Connect to PyBullet
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
            cameraDistance=4.0,
            cameraYaw=45,
            cameraPitch=-20,
            cameraTargetPosition=[0, 0, 0]
        )
        
        # Create robot factory
        factory = RobotModelFactory()
        
        print("🏗️ Creating car robot...")
        car_robot = factory.create_robot('car', position=[0, 0, 0.5])
        
        print("✅ Robot created! You can:")
        print("   - Use mouse to rotate camera")
        print("   - Scroll to zoom in/out")
        print("   - Right-click and drag to pan")
        print("   - Close window when done")
        
        # Simple animation loop
        import time
        step_count = 0
        
        while True:
            try:
                p.stepSimulation()
                
                # Simple robot movement animation
                if step_count % 240 == 0:  # Every 4 seconds
                    pos, orn = p.getBasePositionAndOrientation(car_robot)
                    new_pos = [pos[0] + 0.1, pos[1], pos[2]]
                    p.resetBasePositionAndOrientation(car_robot, new_pos, orn)
                
                step_count += 1
                time.sleep(1/240)
                
            except KeyboardInterrupt:
                break
        
        p.disconnect()
        print("Demo completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def show_robot_types():
    """Show different robot types available"""
    print("🤖 AVAILABLE ROBOT TYPES:")
    print("=" * 40)
    
    robot_info = {
        'car': {
            'name': '🚗 Car Robot',
            'description': 'Wheeled robot, perfect for navigation demos',
            'best_for': 'College presentations, obstacle avoidance'
        },
        'tank': {
            'name': '🛡️ Tank Robot', 
            'description': 'Heavy-duty tracked robot',
            'best_for': 'Rough terrain, military simulations'
        },
        'rover': {
            'name': '🚀 Rover Robot',
            'description': 'Mars rover style with 6 wheels',
            'best_for': 'Space simulations, exploration'
        },
        'humanoid': {
            'name': '🤖 Humanoid Robot',
            'description': 'Bipedal human-like robot', 
            'best_for': 'AI research, human-robot interaction'
        }
    }
    
    for robot_type, info in robot_info.items():
        print(f"{info['name']}")
        print(f"   Description: {info['description']}")
        print(f"   Best for: {info['best_for']}")
        print()

def create_custom_robot():
    """Interactive custom robot creation"""
    if not check_dependencies():
        return
    
    print("⚙️ CUSTOM ROBOT DESIGNER")
    print("=" * 40)
    
    try:
        # Get user preferences
        print("Design your robot:")
        size = input("Robot size (small/medium/large) [medium]: ").lower() or "medium"
        color = input("Robot color (red/blue/green/yellow) [blue]: ").lower() or "blue"
        
        # Map choices to parameters
        size_map = {
            'small': [0.25, 0.15, 0.08],
            'medium': [0.4, 0.2, 0.1], 
            'large': [0.6, 0.3, 0.15]
        }
        
        color_map = {
            'red': [1.0, 0.2, 0.2, 1.0],
            'blue': [0.2, 0.5, 0.8, 1.0],
            'green': [0.2, 0.8, 0.2, 1.0],
            'yellow': [1.0, 1.0, 0.2, 1.0]
        }
        
        chassis_size = size_map.get(size, size_map['medium'])
        chassis_color = color_map.get(color, color_map['blue'])
        
        print(f"\\n🏗️ Creating {size} {color} robot...")
        
        # Create simulation
        import pybullet as p
        import pybullet_data
        from src.simulation.custom_robot_models import RobotModelFactory
        
        client = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.resetSimulation()
        p.setGravity(0, 0, -9.81)
        
        # Ground
        ground_shape = p.createCollisionShape(p.GEOM_PLANE)
        ground_id = p.createMultiBody(0, ground_shape)
        
        # Camera
        p.resetDebugVisualizerCamera(3.0, 45, -20, [0, 0, 0])
        
        # Create custom robot
        factory = RobotModelFactory()
        robot_id = factory.create_robot(
            'car',
            position=[0, 0, 0.5],
            chassis_size=chassis_size,
            chassis_color=chassis_color
        )
        
        print("✅ Custom robot created!")
        print("   Examine your robot and close window when done")
        
        # Keep running
        import time
        try:
            while True:
                p.stepSimulation()
                time.sleep(1/240)
        except KeyboardInterrupt:
            pass
        
        p.disconnect()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main demo menu"""
    print("🚀 SARUS ROBOT - STEP BY STEP IMPROVEMENT")
    print("=" * 50)
    
    while True:
        print("\\nChoose an option:")
        print("1. 📋 Show available robot types")
        print("2. 🤖 Demo robot model showcase") 
        print("3. ⚙️ Create custom robot")
        print("4. ❌ Exit")
        
        choice = input("\\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            show_robot_types()
        elif choice == '2':
            show_robot_models()
        elif choice == '3':
            create_custom_robot()
        elif choice == '4':
            print("\\n👋 Thank you! Your robot demo is ready for college presentation!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
