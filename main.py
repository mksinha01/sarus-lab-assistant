"""
Sarus - Autonomous AI-Powered Lab Assistant Robot

Main entry point for the Sarus robot system.
This module initializes and coordinates all subsystems including:
- Voice interaction (STT/TTS)
- AI processing (LLaMA, vision models)
- Hardware control (motors, sensors)
- Navigation and exploration
- Logging and reporting
"""
import numpy as np
import asyncio
import logging
import signal
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.robot import SarusRobot
from src.config.settings import SYSTEM_CONFIG
from src.utils.logger import setup_logging

# Global robot instance
robot = None

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    #!/usr/bin/env python3
"""
🤖 SARUS - AI Lab Assistant Robot (Jarvis + Sarus Integration)
Main entry point for the autonomous lab assistant robot

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

from src.core.robot import SarusRobot
from src.config.settings import Config
from src.utils.logging import setup_logging

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print("\n🛑 Shutdown signal received. Stopping Sarus...")
    sys.exit(0)

async def main():
    """Main entry point for Sarus robot"""
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    print("🚀 SARUS AI LAB ASSISTANT ROBOT")
    print("=" * 50)
    print("🔬 Jarvis + Sarus Integration")
    print("🤖 Autonomous Lab Assistant with AI")
    print("🛡️ Safety, Security & Environmental Monitoring")
    print("=" * 50)
    
    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Initialize configuration
        config = Config()
        logger.info("Configuration loaded successfully")
        
        # Initialize Sarus robot
        print("🔧 Initializing Sarus robot systems...")
        robot = SarusRobot(config)
        
        # Start robot systems
        await robot.initialize()
        logger.info("Sarus robot initialized successfully")
        
        print("✅ Sarus is ready!")
        print("🎤 Say 'Hey Sarus' to start voice interaction")
        print("🎮 Use Xbox controller for manual control")
        print("🌐 Web dashboard available at http://localhost:5000")
        print("📊 Monitoring environmental conditions...")
        
        # Start main robot loop
        await robot.run()
        
    except KeyboardInterrupt:
        print("
👋 Sarus shutdown requested by user")
        
    except Exception as e:
        logger.error(f"Critical error in main: {e}")
        print(f"❌ Critical error: {e}")
        
    finally:
        # Cleanup
        if 'robot' in locals():
            await robot.shutdown()
        print("🛑 Sarus shutdown complete")

if __name__ == "__main__":
    try:
        # Run the main async loop
        asyncio.run(main())
    except KeyboardInterrupt:
        print("
👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
    if robot:
        robot.shutdown()
    sys.exit(0)

async def main():
    """Main entry point for Sarus robot"""
    global robot
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("🔬 Starting Sarus - Autonomous AI-Powered Lab Assistant Robot")
        
        # Initialize robot
        robot = SarusRobot()
        await robot.initialize()
        
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start main robot loop
        await robot.run()
        
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        if robot:
            robot.shutdown()
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSarus shutdown complete.")
    except Exception as e:
        print(f"Failed to start Sarus: {e}")
        sys.exit(1)
