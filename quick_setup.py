#!/usr/bin/env python3
"""
Quick Setup and Test Script for Improved Sarus Robot Demo
"""

import sys
import subprocess
from pathlib import Path

def install_simulation_deps():
    """Install simulation dependencies"""
    print("📦 Installing simulation dependencies...")
    
    packages = [
        "pybullet>=3.2.5",
        "numpy>=1.21.0", 
        "matplotlib>=3.5.0"
    ]
    
    for package in packages:
        print(f"   Installing {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"   ✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️ Could not install {package}: {e}")
    
    print("✅ Dependencies installation complete!")

def test_simulation():
    """Test if simulation works"""
    print("🧪 Testing simulation...")
    
    try:
        import pybullet as p
        import numpy as np
        
        # Quick test
        client = p.connect(p.DIRECT)  # Headless mode for testing
        p.resetSimulation()
        p.setGravity(0, 0, -9.81)
        
        # Test robot creation
        from src.simulation.custom_robot_models import RobotModelFactory
        factory = RobotModelFactory()
        
        print("   ✅ PyBullet working")
        print("   ✅ Custom robot models working")
        
        p.disconnect()
        print("✅ Simulation test passed!")
        return True
        
    except Exception as e:
        print(f"   ❌ Simulation test failed: {e}")
        return False

def main():
    print("🚀 SARUS ROBOT - QUICK SETUP")
    print("=" * 40)
    
    # Install dependencies
    install_simulation_deps()
    
    print()
    
    # Test simulation
    if test_simulation():
        print()
        print("🎉 Setup complete! Your robot demo is ready!")
        print()
        print("To run the demo:")
        print(f"   python improved_demo.py")
        print()
        print("Available robot types:")
        print("   🚗 Car Robot (recommended for college demo)")
        print("   🛡️ Tank Robot (heavy-duty)")
        print("   🚀 Rover Robot (Mars rover style)")
        print("   🤖 Humanoid Robot (bipedal)")
        print("   ⚙️ Custom Robot (design your own)")
    else:
        print()
        print("❌ Setup incomplete. Please check errors above.")

if __name__ == "__main__":
    main()
