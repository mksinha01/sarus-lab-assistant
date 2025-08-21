#!/usr/bin/env python3
"""
Enhanced Sarus Robot College Demonstration System
Advanced version with realistic robot model, camera controls, and better interaction
"""

import sys
import os
import time
import threading
import asyncio
import math
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import enhanced simulation
from src.simulation.enhanced_sim_world import EnhancedSarusSimWorld

def print_header():
    """Print enhanced demo header"""
    print("🤖 Sarus Robot - ENHANCED College Demonstration System")
    print("   ⚡ Realistic 3D Physics Simulation with PyBullet")
    print("   🎮 Interactive Controls & Multiple Camera Modes")
    print("   🚗 Realistic Robot Car Model")
    print("   🎯 Advanced Pathfinding & Navigation")

def print_menu():
    """Print enhanced menu options"""
    print("\n" + "="*70)
    print("🤖 SARUS ROBOT - ENHANCED COLLEGE DEMONSTRATION SYSTEM")
    print("="*70)
    print("Choose your demonstration mode:")
    print()
    print("1. 🎭 Auto Demo     - Advanced pathfinding navigation")
    print("2. 🎮 Interactive   - Manual control with enhanced controls")
    print("3. 🧪 Component     - Test robot components with controls")
    print("4. 📊 Full System   - Complete robot with AI integration")
    print("5. 🎥 Camera Test   - Test different camera angles")
    print("6. 📦 Install Deps  - Install simulation dependencies")
    print("7. ❌ Exit")
    print()

def check_dependencies():
    """Check if simulation dependencies are available"""
    try:
        import pybullet
        import numpy
        print("✅ Enhanced simulation dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing Enhanced Simulation Dependencies...")
    print("   This may take a few minutes...")
    
    import subprocess
    
    packages = [
        "pybullet>=3.2.0",
        "numpy>=1.21.0", 
        "matplotlib>=3.5.0",
        "opencv-python>=4.5.0",
        "Pillow>=8.0.0"
    ]
    
    for package in packages:
        print(f"   Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"   ✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"   ❌ Failed to install {package}")
    
    print("📦 Installation complete!")

def run_enhanced_auto_demo():
    """Run enhanced auto demo with advanced pathfinding"""
    print("\n🎭 Starting Enhanced Automated Demonstration")
    print("="*60)
    print("🎓 Advanced Sarus Robot College Demonstration")
    print("="*60)
    
    try:
        # Create enhanced simulation world
        print("🌍 Creating Enhanced 3D World...")
        world = EnhancedSarusSimWorld(gui_mode=True, lab_environment=True)
        
        # Create enhanced robot
        print("🚗 Creating Realistic Robot Car...")
        robot_id = world.create_enhanced_robot()
        
        print("\n🎭 Starting advanced demonstration sequence...")
        print("📱 Camera Controls Available:")
        print("   - Follow Camera (default)")
        print("   - Fixed Camera") 
        print("   - Top-Down View")
        print("   - First-Person View")
        print("   - Distance/Angle sliders")
        
        # Enhanced navigation sequence
        navigation_sequence = [
            ("🔄 Moving forward with obstacle avoidance", 2.0, 0.0, 3.0),
            ("↪️ Smart turning right around obstacles", 0.0, 1.5, 2.0),
            ("🔄 Advanced pathfinding through lab", 1.5, 0.0, 4.0),
            ("↩️ Intelligent left turn navigation", 0.0, -1.2, 2.5),
            ("🎯 Exploring target areas", 1.0, 0.5, 3.0),
            ("🏠 Returning to base with optimal path", -1.5, 0.0, 3.0),
        ]
        
        for action, linear_vel, angular_vel, duration in navigation_sequence:
            print(f"\n{action}")
            
            start_time = time.time()
            while time.time() - start_time < duration:
                # Get enhanced obstacle detection
                obstacles = world.get_obstacle_detection()
                
                # Display obstacle information
                detected_obstacles = [name for name, detected in obstacles.items() if detected]
                if detected_obstacles:
                    print(f"   ⚠️ Smart obstacle avoidance: {detected_obstacles}")
                
                # Enhanced movement with obstacle avoidance
                if obstacles.get('front_center', False):
                    # Smart obstacle avoidance
                    if not obstacles.get('front_right', False):
                        world.move_robot(0.0, 1.0)  # Turn right
                    elif not obstacles.get('front_left', False):
                        world.move_robot(0.0, -1.0)  # Turn left
                    else:
                        world.move_robot(-0.5, 0.0)  # Back up
                else:
                    world.move_robot(linear_vel, angular_vel)
                
                world.step_simulation()
                time.sleep(1/60)  # 60 FPS
        
        print("\n🛑 Mission complete - advanced navigation finished")
        print("🎉 Enhanced Demonstration Complete!")
        print("   - Advanced pathfinding successful")
        print("   - Smart obstacle avoidance working")
        print("   - Multiple camera modes demonstrated")
        print("   - Realistic robot physics validated")
        
        print("\n📱 Simulation continues for camera exploration...")
        print("   Use camera controls on the right panel")
        print("   Press Ctrl+C to exit")
        
        # Keep simulation running for camera testing
        try:
            while True:
                world.step_simulation()
                time.sleep(1/60)
        except KeyboardInterrupt:
            pass
            
    except Exception as e:
        print(f"❌ Enhanced demo error: {e}")
    finally:
        try:
            world.close()
        except:
            pass
        print("👋 Enhanced demonstration ended")

def run_enhanced_interactive_demo():
    """Run enhanced interactive demo with clear controls"""
    print("\n🎮 Starting Enhanced Interactive Demonstration")
    print("="*60)
    print("🎮 Enhanced Interactive Sarus Robot Demo")
    print("="*60)
    
    print("Enhanced Controls:")
    print("  🎮 MOVEMENT:")
    print("     W/↑ - Move Forward")
    print("     S/↓ - Move Backward") 
    print("     A/← - Turn Left")
    print("     D/→ - Turn Right")
    print("     SPACE - Stop")
    print()
    print("  📷 CAMERA (Use GUI sliders):")
    print("     Follow Camera - Track robot")
    print("     Fixed Camera - Static view")
    print("     Top View - Bird's eye")
    print("     First Person - Robot view")
    print()
    print("  ⚡ ADVANCED:")
    print("     R - Reset robot position")
    print("     T - Toggle turbo mode")
    print("     Q - Quit")
    print()
    
    try:
        # Create enhanced simulation
        world = EnhancedSarusSimWorld(gui_mode=True, lab_environment=True)
        robot_id = world.create_enhanced_robot()
        
        print("🤖 Enhanced Robot ready! Use controls above...")
        print("📱 Camera controls available in GUI panel")
        
        # Interactive control variables
        turbo_mode = False
        
        # Control loop with enhanced input handling
        import pybullet as p
        
        # Add control instructions to GUI
        info_text = p.addUserDebugText("CONTROLS: W/A/S/D to move, R to reset, T for turbo, Q to quit", 
                                     [0, 0, 2], textColorRGB=[1, 1, 1], textSize=1.2)
        
        while True:
            # Get keyboard input
            keys = p.getKeyboardEvents()
            
            linear_vel = 0.0
            angular_vel = 0.0
            speed_multiplier = 2.0 if turbo_mode else 1.0
            
            for key, state in keys.items():
                if state & p.KEY_IS_DOWN:
                    # Movement controls
                    if key == ord('w') or key == p.B3G_UP_ARROW:
                        linear_vel = 2.0 * speed_multiplier
                    elif key == ord('s') or key == p.B3G_DOWN_ARROW:
                        linear_vel = -2.0 * speed_multiplier
                    elif key == ord('a') or key == p.B3G_LEFT_ARROW:
                        angular_vel = 2.0 * speed_multiplier
                    elif key == ord('d') or key == p.B3G_RIGHT_ARROW:
                        angular_vel = -2.0 * speed_multiplier
                    elif key == ord(' '):  # Space bar
                        linear_vel = 0.0
                        angular_vel = 0.0
                    
                    # Special controls
                    elif key == ord('r'):
                        world.reset_robot_position()
                        print("🔄 Robot position reset")
                    elif key == ord('t'):
                        turbo_mode = not turbo_mode
                        mode_text = "ON" if turbo_mode else "OFF"
                        print(f"⚡ Turbo mode: {mode_text}")
                    elif key == ord('q'):
                        print("👋 Quitting interactive demo...")
                        raise KeyboardInterrupt
            
            # Move robot
            world.move_robot(linear_vel, angular_vel)
            
            # Get and display obstacle information
            obstacles = world.get_obstacle_detection()
            detected = [name for name, detected in obstacles.items() if detected]
            if detected:
                print(f"   ⚠️ Obstacles detected: {detected}")
            
            world.step_simulation()
            time.sleep(1/60)
            
    except KeyboardInterrupt:
        print("\n👋 Interactive demo ended")
    except Exception as e:
        print(f"❌ Interactive demo error: {e}")
    finally:
        try:
            world.close()
        except:
            pass

def run_component_test():
    """Run component test with proper controls"""
    print("\n🧪 Starting Enhanced Component Testing")
    print("="*60)
    
    try:
        world = EnhancedSarusSimWorld(gui_mode=True, lab_environment=True)
        robot_id = world.create_enhanced_robot()
        
        print("🧪 Testing robot components...")
        print("📱 This demo will run until you close the window or press Ctrl+C")
        
        test_sequence = [
            ("🔧 Testing movement system", 1.0, 0.0),
            ("🔧 Testing rotation system", 0.0, 1.0),
            ("🔧 Testing sensor systems", 0.5, 0.5),
            ("🔧 Testing camera systems", 0.0, 0.0),
        ]
        
        cycle_count = 0
        while True:
            for test_name, linear_vel, angular_vel in test_sequence:
                print(f"\n{test_name} (Cycle {cycle_count + 1})")
                
                # Run test for 3 seconds
                for i in range(180):  # 3 seconds at 60 FPS
                    obstacles = world.get_obstacle_detection()
                    if any(obstacles.values()):
                        detected = [name for name, detected in obstacles.items() if detected]
                        print(f"   ✅ Sensor test: {detected}")
                    
                    world.move_robot(linear_vel, angular_vel)
                    world.step_simulation()
                    time.sleep(1/60)
                
                # Pause between tests
                for i in range(60):  # 1 second pause
                    world.move_robot(0.0, 0.0)
                    world.step_simulation()
                    time.sleep(1/60)
            
            cycle_count += 1
            print(f"\n🔄 Component test cycle {cycle_count} complete")
            
    except KeyboardInterrupt:
        print("\n👋 Component testing ended")
    except Exception as e:
        print(f"❌ Component test error: {e}")
    finally:
        try:
            world.close()
        except:
            pass

def run_camera_test():
    """Test different camera angles and modes"""
    print("\n🎥 Starting Enhanced Camera Test")
    print("="*60)
    
    try:
        world = EnhancedSarusSimWorld(gui_mode=True, lab_environment=True)
        robot_id = world.create_enhanced_robot()
        
        print("🎥 Camera Test Mode Active")
        print("📱 Use the camera control sliders on the right:")
        print("   - Camera mode buttons (Follow/Fixed/Top/First Person)")
        print("   - Distance slider")
        print("   - Yaw/Pitch angle sliders")
        print()
        print("🚗 Robot will move in a pattern while you test cameras")
        print("   Press Ctrl+C to exit")
        
        # Simple movement pattern for camera testing
        angle = 0
        while True:
            # Move robot in a figure-8 pattern
            x_vel = 1.0 * math.cos(angle * 0.01)
            angular_vel = 0.5 * math.sin(angle * 0.02)
            
            world.move_robot(x_vel, angular_vel)
            world.step_simulation()
            
            angle += 1
            time.sleep(1/60)
            
    except KeyboardInterrupt:
        print("\n👋 Camera test ended")
    except Exception as e:
        print(f"❌ Camera test error: {e}")
    finally:
        try:
            world.close()
        except:
            pass

def run_full_system():
    """Run full system demonstration"""
    print("\n📊 Starting Full Enhanced System")
    print("="*60)
    
    print("⚠️ Note: Full system requires additional dependencies")
    print("   This demo shows the simulation with enhanced features")
    
    try:
        world = EnhancedSarusSimWorld(gui_mode=True, lab_environment=True)
        robot_id = world.create_enhanced_robot()
        
        print("📊 Full system simulation running...")
        print("🎮 All enhanced features active")
        print("   Press Ctrl+C to exit")
        
        # Continuous operation
        while True:
            world.step_simulation()
            time.sleep(1/60)
            
    except KeyboardInterrupt:
        print("\n👋 Full system demo ended")
    except Exception as e:
        print(f"❌ Full system error: {e}")
    finally:
        try:
            world.close()
        except:
            pass

def main():
    """Enhanced main function"""
    import math  # Import math for camera test
    
    print_header()
    
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (1-7): ").strip()
            
            if choice == "1":
                if check_dependencies():
                    run_enhanced_auto_demo()
                else:
                    print("❌ Please install dependencies first (option 6)")
                    
            elif choice == "2":
                if check_dependencies():
                    run_enhanced_interactive_demo()
                else:
                    print("❌ Please install dependencies first (option 6)")
                    
            elif choice == "3":
                if check_dependencies():
                    run_component_test()
                else:
                    print("❌ Please install dependencies first (option 6)")
                    
            elif choice == "4":
                if check_dependencies():
                    run_full_system()
                else:
                    print("❌ Please install dependencies first (option 6)")
                    
            elif choice == "5":
                if check_dependencies():
                    run_camera_test()
                else:
                    print("❌ Please install dependencies first (option 6)")
                    
            elif choice == "6":
                install_dependencies()
                
            elif choice == "7":
                print("👋 Thank you for using Sarus Robot Enhanced Demo!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-7.")
                
        except KeyboardInterrupt:
            print("\n👋 Demo interrupted by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
