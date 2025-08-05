#!/usr/bin/env python3
"""
Quick start script for Sarus robot

This script provides a simple way to start Sarus with different configurations
and test modes for development and deployment.
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.robot import SarusRobot
from src.config.settings import SYSTEM_CONFIG, update_config, get_config
from src.utils.logger import setup_logging

async def main():
    parser = argparse.ArgumentParser(description='Sarus Robot Quick Start')
    parser.add_argument('--profile', choices=['development', 'raspberry_pi_4', 'jetson_nano'], 
                       default='development', help='Hardware profile to use')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--no-hardware', action='store_true', help='Disable hardware (simulation only)')
    parser.add_argument('--test-mode', action='store_true', help='Run in test mode with limited functionality')
    
    args = parser.parse_args()
    
    # Update configuration based on arguments
    config_updates = {}
    
    if args.debug:
        config_updates['debug_mode'] = True
        config_updates['log_level'] = 'DEBUG'
    
    if args.no_hardware:
        config_updates['hardware_enabled'] = False
    
    if args.test_mode:
        config_updates['hardware_enabled'] = False
        config_updates['exploration_duration'] = 60  # Short test missions
    
    # Apply profile configuration
    profile_config = get_config(args.profile)
    config_updates.update(profile_config)
    
    # Update system configuration
    update_config(config_updates)
    
    # Setup logging
    setup_logging()
    
    print(f"""
🔬 Starting Sarus Robot
Profile: {args.profile}
Hardware: {'Enabled' if SYSTEM_CONFIG.get('hardware_enabled') else 'Simulation'}
Debug: {'On' if args.debug else 'Off'}
""")
    
    try:
        # Initialize and run robot
        robot = SarusRobot()
        await robot.initialize()
        
        if args.test_mode:
            print("🧪 Running in test mode - limited functionality")
            await run_test_sequence(robot)
        else:
            print("🚀 Starting main robot operation")
            await robot.run()
    
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
    finally:
        if 'robot' in locals():
            robot.shutdown()

async def run_test_sequence(robot):
    """Run a test sequence for validation"""
    print("Running system tests...")
    
    # Test voice interface
    if robot.voice_interface:
        await robot.voice_interface.test_voice_system()
    
    # Test vision system
    if robot.vision_manager:
        scene = await robot.vision_manager.analyze_scene()
        print(f"Vision test: {scene}")
    
    # Test navigation
    if robot.navigation_manager:
        status = robot.navigation_manager.get_navigation_status()
        print(f"Navigation test: {status}")
    
    # Brief exploration
    print("Starting 30-second test exploration...")
    await robot.navigation_manager.continue_exploration({
        'start_time': asyncio.get_event_loop().time(),
        'max_duration': 30.0
    })
    
    print("✅ Test sequence completed")

if __name__ == "__main__":
    asyncio.run(main())
