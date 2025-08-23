#!/usr/bin/env python3
"""
🤖 SARUS - AI Lab Assistant Robot (Jarvis + Sarus Integration)
Main entry point for the autonomous lab assistant robot

Features:
- Voice interaction with Gemini AI
- Environmental monitoring (temperature, humidity, gas detection)
- Computer vision and face recognition
- Autonomous navigation and movement
- Safety protocols and emergency response

Author: Inventor Usman & Contributors
Version: 2.0.0
License: MIT
"""

import sys
import asyncio
import signal
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import Sarus components
# Use simplified robot for development/testing
from src.core.simple_robot import SarusRobot
from src.config.settings import Config
from src.utils.logging import setup_logging

# Global robot instance for signal handling
robot = None

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print("\n🛑 Shutdown signal received. Stopping Sarus...")
    if robot and hasattr(robot, 'shutdown'):
        # Set running flag to False to stop loops gracefully
        robot.is_running = False
    sys.exit(0)

async def main():
    """Main entry point for Sarus robot"""
    global robot
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("🚀 SARUS AI LAB ASSISTANT ROBOT")
    print("=" * 50)
    print("🔬 Jarvis + Sarus Integration")
    print("🤖 Autonomous Lab Assistant with AI")
    print("🛡️ Safety, Security & Environmental Monitoring")
    print("🎤 Voice Interaction & Natural Language")
    print("🚗 Autonomous Navigation & Movement")
    print("=" * 50)
    
    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Initialize configuration
        print("⚙️ Loading configuration...")
        config = Config()
        logger.info("Configuration loaded successfully")
        
        # Initialize Sarus robot
        print("🔧 Initializing Sarus robot systems...")
        robot = SarusRobot(config)
        
        # Start robot systems
        print("🚀 Starting Sarus subsystems...")
        await robot.initialize()
        logger.info("Sarus robot initialized successfully")
        
        print("✅ Sarus is ready!")
        print("🎤 Say 'Hey Sarus' to start voice interaction")
        print("🎮 Use Xbox controller for manual control")
        print("🌐 Web dashboard available at http://localhost:5000")
        print("📊 Monitoring environmental conditions...")
        print("🛡️ Safety systems active")
        print("\n💬 Example commands:")
        print("  - 'Hey Sarus, what's the temperature?'")
        print("  - 'Hey Sarus, move forward'")
        print("  - 'Hey Sarus, what do you see?'")
        print("  - 'Hey Sarus, patrol the lab'")
        print("\n� Starting main robot loop...\n")
        
        # Start main robot loop
        await robot.run()
        
    except KeyboardInterrupt:
        print("\n👋 Sarus shutdown requested by user")
        
    except Exception as e:
        logger.error(f"Critical error in main: {e}")
        print(f"❌ Critical error: {e}")
        
    finally:
        # Cleanup
        if robot and hasattr(robot, 'shutdown'):
            print("🧹 Cleaning up Sarus systems...")
            await robot.shutdown()
        print("🛑 Sarus shutdown complete")

if __name__ == "__main__":
    try:
        # Run the main async loop
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye from Sarus!")
    except Exception as e:
        print(f"❌ Fatal error starting Sarus: {e}")
        sys.exit(1)
