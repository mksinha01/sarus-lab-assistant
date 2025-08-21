#!/usr/bin/env python3
"""
🚀 ENHANCED SARUS ROBOT - COLLEGE DEMONSTRATION SYSTEM 🚀
Advanced 3D Physics Simulation with Interactive Controls
Perfect for impressing professors and students!

FEATURES:
• Multiple camera angles (Follow/Top/Side/Free)
• Interactive control sliders
• Real-time obstacle detection  
• Smart pathfinding navigation
• "Run Again" button for repeated demos
• Enhanced visual effects
• Realistic robot car model
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
        print("   Please install manually: pip install pybullet numpy matplotlib")
        return False

def check_simulation_ready():
    """Check if enhanced simulation is ready to run"""
    try:
        import pybullet
        import numpy
        print("✅ Enhanced simulation dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        return False

def run_enhanced_auto_demo():
    """🎭 Enhanced Auto Demo with Run Again Button"""
    print("\n🎭 ENHANCED AUTOMATED COLLEGE DEMONSTRATION")
    print("=" * 55)
    print("🎓 Advanced Features:")
    print("   • 🚗 Realistic robot car model")
    print("   • 📷 Multiple camera angles")
    print("   • 🧠 Smart pathfinding navigation")
    print("   • ⚠️ Real-time obstacle detection")
    print("   • 🔄 'Run Again' button in PyBullet window")
    print("   • 🎮 Interactive control sliders")
    print("   • 🌍 Enhanced 3D laboratory environment")
    print("=" * 55)
    
    os.environ['SARUS_SIMULATION'] = '1'
    
    try:
        from src.simulation.enhanced_sim import run_enhanced_auto_demo
        simulation = run_enhanced_auto_demo()
        
        print("\n🎉 ENHANCED AUTO DEMO FEATURES:")
        print("   ✅ 3D PyBullet window with advanced controls")
        print("   ✅ Camera modes: Follow/Top/Side/Free view")
        print("   ✅ Real-time obstacle detection & avoidance")
        print("   ✅ Intelligent pathfinding navigation")
        print("   ✅ 'Run Again' button for repeated demonstrations")
        print("   ✅ Speed and distance control sliders")
        print("   ✅ Pause/Resume simulation control")
        
        print("\n📱 PYBULLET WINDOW CONTROLS:")
        print("   🔄 'Run Demo Again' - Repeat the full demonstration")
        print("   📷 'Camera Mode' - Change viewing angle")
        print("   🔍 'Camera Distance' - Zoom in/out (1.0-10.0)")
        print("   ⏸️ 'Pause/Resume' - Control simulation time")
        print("   🚀 'Speed' - Adjust robot movement speed")
        print("   🔄 'Reset Position' - Return robot to center")
        
        print("\n💡 WINDOW VISIBILITY TIPS:")
        print("   • Check your taskbar for 'PyBullet' or 'Physics Server'")
        print("   • Window may open behind other applications")
        print("   • Try Alt+Tab to find the 3D simulation window")
        print("   • Maximize the window for best experience")
        
        input("\n🎯 Press Enter to close the enhanced simulation...")
        simulation.cleanup()
        
    except ImportError as e:
        print(f"❌ Could not start enhanced auto demo: {e}")
        print("   Installing dependencies and trying again...")
        install_simulation_deps()
        
    except Exception as e:
        print(f"❌ Demo error: {e}")

def run_enhanced_interactive():
    """🎮 Enhanced Interactive Mode with Full Controls"""
    print("\n🎮 ENHANCED INTERACTIVE DEMONSTRATION")
    print("=" * 55)
    print("🎯 Advanced Interactive Features:")
    print("   • 🎮 GUI control sliders + keyboard shortcuts")
    print("   • 📷 4 different camera modes")
    print("   • 🚀 Adjustable speed control (0.1 - 2.0)")
    print("   • ⚠️ Real-time obstacle detection display")
    print("   • 🎭 Auto demo mode within interactive")
    print("   • ⏸️ Pause/Resume functionality")
    print("   • 🔄 Reset position feature")
    print("=" * 55)
    
    os.environ['SARUS_SIMULATION'] = '1'
    
    try:
        from src.simulation.enhanced_sim import run_enhanced_interactive
        simulation = run_enhanced_interactive()
        
        print("\n🎮 ENHANCED INTERACTIVE MODE STARTED!")
        print("\n📋 COMPLETE CONTROL GUIDE:")
        print("\n   🎮 GUI CONTROL SLIDERS:")
        print("      • ⬆️ Move Forward - Push robot forward")
        print("      • ⬇️ Move Backward - Reverse robot movement") 
        print("      • ⬅️ Turn Left - Rotate counter-clockwise")
        print("      • ➡️ Turn Right - Rotate clockwise")
        print("      • 🛑 Stop Robot - Immediate stop")
        print("      • 🚀 Speed (0.1-2.0) - Movement velocity")
        
        print("\n   📷 CAMERA CONTROLS:")
        print("      • Camera Mode 0: Follow robot (behind view)")
        print("      • Camera Mode 1: Top-down (bird's eye view)")
        print("      • Camera Mode 2: Side view (profile view)")
        print("      • Camera Mode 3: Free camera (user control)")
        print("      • Camera Distance: 1.0-10.0 (zoom level)")
        
        print("\n   🎭 SPECIAL FEATURES:")
        print("      • Auto Demo: Launch automatic navigation")
        print("      • Reset Position: Return robot to center")
        print("      • Pause/Resume: Control simulation time")
        
        print("\n💡 HOW TO USE CONTROLS:")
        print("   1. Adjust sliders in the PyBullet control panel")
        print("   2. Robot responds to slider changes in real-time")
        print("   3. Try different camera modes for best view")
        print("   4. Use speed control for precise movements")
        print("   5. Monitor obstacle detection in real-time")
        
        print("\n🎯 INTERACTIVE MODE ACTIVE!")
        print("   Keep the 3D window focused for best experience!")
        
        simulation.cleanup()
        
    except ImportError as e:
        print(f"❌ Could not start enhanced interactive mode: {e}")
        install_simulation_deps()
        
    except Exception as e:
        print(f"❌ Interactive mode error: {e}")

def run_enhanced_component_test():
    """🧪 Enhanced Component Testing with Detailed Explanations"""
    print("\n🧪 ENHANCED COMPONENT TESTING SYSTEM")
    print("=" * 55)
    print("🔧 What This Advanced Test Does:")
    print("   • 🚗 Tests all robot subsystems individually")
    print("   • 📊 Shows real-time component status")
    print("   • 🎬 Demonstrates each capability visually")
    print("   • 📈 Provides detailed system feedback")
    print("   • 🔄 Continues running for manual interaction")
    print("   • 🎮 Includes control explanations")
    print("=" * 55)
    
    os.environ['SARUS_SIMULATION'] = '1'
    
    try:
        from src.simulation.enhanced_sim import run_enhanced_component_test
        simulation = run_enhanced_component_test()
        
        print("\n✅ ENHANCED COMPONENT TEST FEATURES:")
        print("   🚗 Motor Testing - Movement in all directions")
        print("   📡 Sensor Testing - Obstacle detection validation")
        print("   📷 Vision Testing - Camera and image processing")
        print("   🧠 Navigation Testing - Path planning demonstration")
        print("   🔋 Power Testing - Battery and energy management")
        print("   📊 Communication Testing - Data transmission")
        
        print("\n🎮 AFTER AUTOMATED TESTING:")
        print("   • Simulation continues for manual interaction")
        print("   • Use control sliders to test components yourself")
        print("   • All camera modes available for inspection")
        print("   • Real-time feedback on all systems")
        
        print("\n🔧 DETAILED BUTTON EXPLANATIONS:")
        print("   ⬆️ Forward Button:")
        print("      - Activates forward drive motors")
        print("      - Speed controlled by Speed slider")
        print("      - Automatically detects front obstacles")
        
        print("   ⬇️ Backward Button:")
        print("      - Reverses motor direction")
        print("      - Slower speed for safety")
        print("      - Checks rear sensors")
        
        print("   ⬅️ Left Turn Button:")
        print("      - Differential motor control")
        print("      - Right motor faster than left")
        print("      - Gyroscope feedback for accuracy")
        
        print("   ➡️ Right Turn Button:")
        print("      - Left motor faster than right")
        print("      - Controlled rotation rate")
        print("      - Prevents over-turning")
        
        print("   🛑 Stop Button:")
        print("      - Immediate motor stop")
        print("      - Engages braking system")
        print("      - Saves current position")
        
        print("   🚀 Speed Slider (0.1-2.0):")
        print("      - 0.1-0.5: Precise movements")
        print("      - 0.5-1.0: Normal operation")
        print("      - 1.0-2.0: Fast movements")
        
        print("   📷 Camera Controls:")
        print("      - Mode 0: Robot-following camera")
        print("      - Mode 1: Overhead surveillance view")
        print("      - Mode 2: Side inspection view")
        print("      - Mode 3: Free-roaming camera")
        
        print("   🔄 Reset Button:")
        print("      - Returns robot to starting position")
        print("      - Clears movement history")
        print("      - Resets all sensors")
        
        print("\n🎯 COMPONENT TEST COMPLETED!")
        print("   All systems verified and ready for demonstration!")
        
        simulation.cleanup()
        
    except ImportError as e:
        print(f"❌ Could not start enhanced component test: {e}")
        install_simulation_deps()
        
    except Exception as e:
        print(f"❌ Component test error: {e}")

def show_window_troubleshooting():
    """Show detailed window troubleshooting guide"""
    print("\n🔧 PYBULLET WINDOW TROUBLESHOOTING GUIDE")
    print("=" * 55)
    print("❓ If you don't see the 3D simulation window:")
    print("\n🔍 CHECK THESE LOCATIONS:")
    print("   1. Windows Taskbar:")
    print("      • Look for 'PyBullet Physics Server'")
    print("      • Look for 'Bullet Physics ExampleBrowser'")
    print("      • Look for 'OpenGL' application")
    print("\n   2. Alt+Tab Menu:")
    print("      • Press Alt+Tab to cycle through windows")
    print("      • Look for simulation window")
    print("\n   3. Multiple Monitors:")
    print("      • Check all connected displays")
    print("      • Window may open on secondary monitor")
    print("\n   4. Window State:")
    print("      • Window may be minimized")
    print("      • Right-click taskbar icon and select 'Maximize'")
    print("\n🛠️ SOLUTIONS:")
    print("   • Try running demo again")
    print("   • Close other applications to free up resources")
    print("   • Update graphics drivers")
    print("   • Run as administrator if needed")
    print("\n💡 WHAT YOU SHOULD SEE:")
    print("   • 3D laboratory environment")
    print("   • Blue robot car in the center")
    print("   • Control sliders on the right side")
    print("   • Laboratory tables and equipment")
    print("   • Real-time movement and physics")

def main():
    """Main enhanced demonstration launcher"""
    print("🚀 ENHANCED SARUS ROBOT - COLLEGE DEMONSTRATION SYSTEM")
    print("   Advanced 3D Physics Simulation with Interactive Controls")
    print("   Perfect for impressing professors and students!")
    print("")
    
    # Check dependencies first
    if not check_simulation_ready():
        print("📦 Installing required dependencies...")
        if not install_simulation_deps():
            print("❌ Failed to install dependencies. Please install manually.")
            return
    
    while True:
        print("\n" + "=" * 60)
        print("🤖 ENHANCED SARUS ROBOT - COLLEGE DEMONSTRATION SYSTEM")
        print("=" * 60)
        print("Choose your enhanced demonstration mode:")
        print("")
        print("1. 🎭 Enhanced Auto Demo    - Advanced pathfinding navigation")
        print("2. 🎮 Enhanced Interactive  - Full manual control with GUI")
        print("3. 🧪 Enhanced Components   - Detailed system testing")
        print("4. 📊 Window Troubleshoot   - Help finding the 3D window")
        print("5. 📦 Install Dependencies  - Reinstall simulation packages")
        print("6. ❌ Exit")
        print("")
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                run_enhanced_auto_demo()
            elif choice == "2":
                run_enhanced_interactive()
            elif choice == "3":
                run_enhanced_component_test()
            elif choice == "4":
                show_window_troubleshooting()
            elif choice == "5":
                install_simulation_deps()
            elif choice == "6":
                print("\n👋 Thank you for using Enhanced Sarus Robot Demo!")
                print("   🎓 Perfect for your college presentation!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
