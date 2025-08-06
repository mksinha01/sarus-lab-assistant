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
    print("\nShutting down Sarus...")
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
