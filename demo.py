#!/usr/bin/env python3
"""
🚀 SARUS ROBOT - ENHANCED COLLEGE DEMONSTRATION SYSTEM 🚀
Advanced 3D Physics Simulation with Interactive Controls
Perfect for impressing professors and students!
"""
import os
import sys
import time
import threading
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def install_simulation_deps():
    """Install required simulation dependencies"""
    print("📦 Installing simulation dependencies...")
    
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
        
        print("✅ Simulation dependencies installed!")
        return True
        
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        print("   Please install manually: pip install pybullet numpy matplotlib")
        return False

def check_simulation_ready():
    """Check if simulation is ready to run"""
    try:
        import pybullet
        import numpy
        print("✅ Simulation dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def show_demo_menu():
    """Show demonstration menu"""
    print("\n" + "="*60)
    print("🤖 SARUS ROBOT - COLLEGE DEMONSTRATION SYSTEM")
    print("="*60)
    print("Choose your demonstration mode:")
    print()
    print("1. 🎭 Auto Demo    - Automated navigation demonstration")
    print("2. 🎮 Interactive  - Manual control with WASD keys")
    print("3. 🧪 Component    - Test individual robot components")
    print("4. 📊 Full System  - Complete robot with AI integration")
    print("5. 📦 Install Deps - Install simulation dependencies")
    print("6. ❌ Exit")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return int(choice)
            else:
                print("❌ Invalid choice. Please enter 1-6.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return 6

def run_auto_demo():
    """Run automated demonstration"""
    print("\n🎭 Starting Automated College Demonstration")
    print("=" * 50)
    
    # Enable simulation mode
    os.environ['SARUS_SIMULATION'] = '1'
    
    try:
        from src.simulation.sim_integration import run_college_demo
        run_college_demo()
    except ImportError as e:
        print(f"❌ Could not start demo: {e}")
        print("   Make sure simulation dependencies are installed")

def run_interactive_demo():
    """Run interactive demonstration"""
    print("\n🎮 Starting Interactive Demonstration")
    print("=" * 50)
    
    os.environ['SARUS_SIMULATION'] = '1'
    
    try:
        from src.simulation.sim_integration import run_interactive_demo
        run_interactive_demo()
    except ImportError as e:
        print(f"❌ Could not start interactive demo: {e}")

def run_component_test():
    """Run component testing demonstration"""
    print("\n🧪 Testing Robot Components")
    print("=" * 50)
    
    os.environ['SARUS_SIMULATION'] = '1'
    
    try:
        from src.simulation.sim_integration import (
            create_motor_controller, 
            create_sensor_manager, 
            create_vision_manager,
            step_simulation
        )
        import asyncio
        
        async def test_components():
            print("Initializing simulated components...")
            
            # Create components
            motors = create_motor_controller()
            sensors = create_sensor_manager()
            vision = create_vision_manager()
            
            # Initialize
            await motors.initialize()
            await sensors.initialize()
            await vision.initialize()
            
            print("\n🔄 Testing motor movements...")
            movements = [
                ("Forward", lambda: motors.move_forward(0.5)),
                ("Backward", lambda: motors.move_backward(0.5)),
                ("Turn Left", lambda: motors.turn_left(0.4)),
                ("Turn Right", lambda: motors.turn_right(0.4)),
                ("Stop", lambda: motors.stop())
            ]
            
            for name, action in movements:
                print(f"   {name}...")
                action()
                
                # Run simulation for 1 second
                for _ in range(60):
                    step_simulation()
                    await asyncio.sleep(1/60)
            
            print("\n📡 Testing sensors...")
            obstacle_data = sensors.get_obstacle_map()
            nav_data = sensors.get_navigation_data()
            battery = sensors.get_battery_level()
            
            print(f"   Battery Level: {battery:.1f}%")
            print(f"   Position: ({nav_data['position']['x']:.2f}, {nav_data['position']['y']:.2f})")
            print(f"   Obstacles Detected: {len(obstacle_data.get('obstacles', {}))}")
            
            print("\n👁️ Testing vision...")
            scene_analysis = await vision.analyze_scene()
            print(f"   Objects Detected: {len(scene_analysis['objects_detected'])}")
            print(f"   Scene: {scene_analysis['scene_description']}")
            
            print("\n✅ All component tests completed!")
            
        asyncio.run(test_components())
        
    except Exception as e:
        print(f"❌ Component test error: {e}")

def run_full_system():
    """Run full robot system demonstration"""
    print("\n📊 Starting Full Robot System")
    print("=" * 50)
    
    os.environ['SARUS_SIMULATION'] = '1'
    
    try:
        # Import and run the main robot
        from src.core.robot import SarusRobot
        import asyncio
        
        async def run_full_robot():
            print("🤖 Initializing Sarus Robot in simulation mode...")
            
            robot = SarusRobot()
            await robot.initialize()
            
            print("✅ Robot initialized successfully!")
            print("🎭 Robot will demonstrate autonomous behavior...")
            
            # Let robot run for demo
            robot.is_running = True
            
            try:
                await robot.run()
            except KeyboardInterrupt:
                print("\n🛑 Demo stopped by user")
            finally:
                robot.shutdown()
        
        asyncio.run(run_full_robot())
        
    except Exception as e:
        print(f"❌ Full system error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main demonstration launcher"""
    print("🤖 Sarus Robot College Demonstration System")
    print("   Developed for autonomous lab assistant demonstration")
    print("   3D Physics Simulation with PyBullet")
    
    while True:
        choice = show_demo_menu()
        
        if choice == 1:
            if check_simulation_ready():
                run_auto_demo()
            else:
                print("❌ Simulation not ready. Install dependencies first (option 5)")
                
        elif choice == 2:
            if check_simulation_ready():
                run_interactive_demo()
            else:
                print("❌ Simulation not ready. Install dependencies first (option 5)")
                
        elif choice == 3:
            if check_simulation_ready():
                run_component_test()
            else:
                print("❌ Simulation not ready. Install dependencies first (option 5)")
                
        elif choice == 4:
            if check_simulation_ready():
                run_full_system()
            else:
                print("❌ Simulation not ready. Install dependencies first (option 5)")
                
        elif choice == 5:
            install_simulation_deps()
            
        elif choice == 6:
            print("\n👋 Thank you for viewing the Sarus Robot demonstration!")
            print("   🌟 Star the project: https://github.com/mksinha01/sarus-lab-assistant")
            break
        
        print("\n" + "="*60)
        input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demonstration ended. Thank you!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("   Check that all dependencies are installed")
        print("   Run with: python demo.py")
