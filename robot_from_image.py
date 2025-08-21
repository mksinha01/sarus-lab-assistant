#!/usr/bin/env python3
"""
🤖 ROBOT FROM IMAGE DEMO
Create robot model based on your uploaded image
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def show_image_info():
    """Show information about the uploaded image"""
    print("📸 IMAGE ANALYSIS")
    print("=" * 40)
    print("Image found: Gemini_Generated_Image_68y4uv68y4uv68y4.png")
    print("Location: ./image/ folder")
    print()
    print("🔍 Based on typical robot designs, I can create:")
    print("   🚗 Car-style robot (wheeled, autonomous vehicle)")
    print("   🛡️ Tank-style robot (tracked, heavy-duty)")
    print("   🚀 Rover-style robot (6-wheels, exploration)")
    print("   🤖 Humanoid robot (bipedal, service robot)")
    print("   ⚙️ Custom design (based on your specifications)")

def create_image_based_robot():
    """Create robot based on the uploaded image"""
    print("🤖 CREATING ROBOT FROM YOUR IMAGE")
    print("=" * 50)
    
    # Ask user what type of robot they want based on their image
    print("What type of robot does your image show?")
    print("1. 🚗 Car/Vehicle robot (4 wheels, autonomous)")
    print("2. 🛡️ Tank robot (tracks, heavy-duty)")
    print("3. 🚀 Rover robot (6 wheels, space/exploration)")
    print("4. 🤖 Humanoid robot (legs, human-like)")
    print("5. ⚙️ Custom robot (I'll help you design)")
    
    choice = input("\\nEnter choice (1-5) [1]: ").strip() or "1"
    
    try:
        import pybullet as p
        import pybullet_data
        import numpy as np
        from src.simulation.image_based_robot import ImageBasedRobotModel, get_robot_specs_templates
        
        # Initialize simulation
        client = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.resetSimulation()
        p.setGravity(0, 0, -9.81)
        
        # Create ground
        ground_shape = p.createCollisionShape(p.GEOM_PLANE)
        ground_id = p.createMultiBody(0, ground_shape)
        
        # Set camera
        p.resetDebugVisualizerCamera(3.0, 45, -20, [0, 0, 0])
        
        # Get robot specifications
        templates = get_robot_specs_templates()
        
        if choice == "1":
            robot_specs = templates['modern_car_robot']
            print("🚗 Creating car-style robot based on your image...")
        elif choice == "2":
            robot_specs = templates['tank_robot'] 
            print("🛡️ Creating tank-style robot based on your image...")
        elif choice == "3":
            # Rover specification
            robot_specs = {
                'type': 'rover',
                'body': {
                    'shape': 'box',
                    'size': [0.6, 0.4, 0.12],
                    'color': [0.8, 0.8, 0.8, 1.0],  # Silver
                    'position': [0, 0, 0.5]
                },
                'movement': {
                    'type': 'wheels',
                    'count': 6,
                    'radius': 0.1,
                    'width': 0.06,
                    'color': [0.3, 0.3, 0.3, 1.0]
                },
                'sensors': {
                    'camera': True,
                    'positions': [[0.35, 0, 0.15]],
                    'color': [0.0, 0.5, 1.0, 1.0]
                },
                'features': {
                    'antenna': True,
                    'arms': False
                }
            }
            print("🚀 Creating rover-style robot based on your image...")
        elif choice == "4":
            robot_specs = templates['humanoid_robot']
            print("🤖 Creating humanoid robot based on your image...")
        else:
            # Custom robot
            print("⚙️ Creating custom robot...")
            robot_specs = get_custom_robot_specs()
        
        # Create robot
        robot_model = ImageBasedRobotModel()
        robot_id = robot_model.create_robot_from_specs(robot_specs)
        
        print("\\n✅ Robot created successfully!")
        print("🎮 Use mouse to examine your robot:")
        print("   - Drag to rotate camera")
        print("   - Scroll to zoom")
        print("   - Right-drag to pan")
        print("\\n   Close window when finished")
        
        # Animation loop
        import time
        step = 0
        
        while True:
            try:
                p.stepSimulation()
                
                # Gentle robot movement for demonstration
                if step % 300 == 0:  # Every 5 seconds
                    pos, orn = p.getBasePositionAndOrientation(robot_id)
                    # Small circular movement
                    angle = step * 0.01
                    new_pos = [
                        pos[0] + 0.1 * np.cos(angle),
                        pos[1] + 0.1 * np.sin(angle),
                        pos[2]
                    ]
                    p.resetBasePositionAndOrientation(robot_id, new_pos, orn)
                
                step += 1
                time.sleep(1/240)
                
            except KeyboardInterrupt:
                break
        
        p.disconnect()
        
    except Exception as e:
        print(f"❌ Error creating robot: {e}")
        print("   Make sure dependencies are installed: python quick_setup.py")

def get_custom_robot_specs():
    """Get custom robot specifications from user"""
    print("\\n⚙️ CUSTOM ROBOT DESIGNER")
    print("Let's design your robot step by step:")
    
    # Body shape
    print("\\n1. Body shape:")
    print("   a) Box (rectangular)")
    print("   b) Cylinder (round)")
    print("   c) Rounded (capsule)")
    body_shape = input("Choose (a/b/c) [a]: ").lower() or "a"
    shape_map = {'a': 'box', 'b': 'cylinder', 'c': 'rounded'}
    
    # Body size
    print("\\n2. Robot size:")
    print("   a) Small (compact)")
    print("   b) Medium (standard)")
    print("   c) Large (heavy-duty)")
    size_choice = input("Choose (a/b/c) [b]: ").lower() or "b"
    size_map = {
        'a': [0.25, 0.15, 0.08],
        'b': [0.4, 0.25, 0.12],
        'c': [0.6, 0.35, 0.18]
    }
    
    # Color
    print("\\n3. Robot color:")
    print("   a) Blue    b) Red     c) Green")
    print("   d) Silver  e) Black   f) Yellow")
    color_choice = input("Choose (a-f) [a]: ").lower() or "a"
    color_map = {
        'a': [0.2, 0.5, 0.8, 1.0],  # Blue
        'b': [0.8, 0.2, 0.2, 1.0],  # Red
        'c': [0.2, 0.8, 0.2, 1.0],  # Green
        'd': [0.8, 0.8, 0.8, 1.0],  # Silver
        'e': [0.2, 0.2, 0.2, 1.0],  # Black
        'f': [1.0, 1.0, 0.2, 1.0]   # Yellow
    }
    
    # Movement type
    print("\\n4. Movement system:")
    print("   a) Wheels (4-wheel drive)")
    print("   b) Tracks (tank-style)")
    print("   c) Legs (walking robot)")
    movement_choice = input("Choose (a/b/c) [a]: ").lower() or "a"
    movement_map = {'a': 'wheels', 'b': 'tracks', 'c': 'legs'}
    
    # Features
    print("\\n5. Special features:")
    has_antenna = input("Add antenna? (y/n) [y]: ").lower() != "n"
    has_arms = input("Add robotic arms? (y/n) [n]: ").lower() == "y"
    
    return {
        'type': 'custom',
        'body': {
            'shape': shape_map[body_shape],
            'size': size_map[size_choice],
            'color': color_map[color_choice],
            'position': [0, 0, 0.5]
        },
        'movement': {
            'type': movement_map[movement_choice],
            'count': 4 if movement_choice == 'a' else 2,
            'radius': 0.08,
            'width': 0.04,
            'color': [0.1, 0.1, 0.1, 1.0]
        },
        'sensors': {
            'camera': True,
            'positions': [[0.25, 0, 0.05]],
            'color': [1.0, 1.0, 0.0, 1.0]
        },
        'features': {
            'antenna': has_antenna,
            'arms': has_arms
        }
    }

def main():
    """Main function"""
    print("🤖 ROBOT FROM IMAGE - STEP BY STEP")
    print("=" * 50)
    
    while True:
        print("\\nWhat would you like to do?")
        print("1. 📸 Show image information")
        print("2. 🤖 Create robot from image")
        print("3. ❌ Exit")
        
        choice = input("\\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            show_image_info()
        elif choice == "2":
            create_image_based_robot()
        elif choice == "3":
            print("\\n👋 Thank you! Your custom robot is ready!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
