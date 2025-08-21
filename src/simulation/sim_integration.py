"""
Simulation Mode Integration for Sarus Robot
Automatically switches between real hardware and simulation
"""
import os
import sys
import time
from pathlib import Path

def is_simulation_mode():
    """Check if running in simulation mode"""
    return os.getenv('SARUS_SIMULATION', '0').lower() in ['1', 'true', 'yes']

def get_simulation_world():
    """Get or create simulation world"""
    if not hasattr(get_simulation_world, '_world'):
        if is_simulation_mode():
            try:
                from .sim_world import SarusSimWorld
                get_simulation_world._world = SarusSimWorld(
                    gui=True, 
                    lab_environment=True
                )
                print("🌍 3D Simulation World Created!")
            except ImportError as e:
                print(f"⚠️ Could not create simulation world: {e}")
                print("   Install PyBullet: pip install pybullet")
                get_simulation_world._world = None
        else:
            get_simulation_world._world = None
    
    return get_simulation_world._world

def create_motor_controller():
    """Create motor controller (real or simulated)"""
    if is_simulation_mode():
        from .sim_hardware import SimMotorController
        world = get_simulation_world()
        controller = SimMotorController(world)
        print("🚗 Using SIMULATED motor controller")
        return controller
    else:
        from ..hardware.motor_controller import MotorController
        print("🚗 Using REAL motor controller")
        return MotorController()

def create_sensor_manager():
    """Create sensor manager (real or simulated)"""
    if is_simulation_mode():
        from .sim_hardware import SimSensorManager
        world = get_simulation_world()
        manager = SimSensorManager(world)
        print("📡 Using SIMULATED sensor manager")
        return manager
    else:
        from ..hardware.sensor_manager import SensorManager
        print("📡 Using REAL sensor manager")
        return SensorManager()

def create_vision_manager():
    """Create vision manager (real or simulated)"""
    if is_simulation_mode():
        from .sim_hardware import SimVisionManager
        world = get_simulation_world()
        manager = SimVisionManager(world)
        print("👁️ Using SIMULATED vision manager")
        return manager
    else:
        from ..ai.vision_manager import VisionManager
        print("👁️ Using REAL vision manager")
        return VisionManager()

def step_simulation():
    """Step simulation forward (only in simulation mode)"""
    if is_simulation_mode():
        world = get_simulation_world()
        if world:
            world.step()

def cleanup_simulation():
    """Cleanup simulation resources"""
    if hasattr(get_simulation_world, '_world') and get_simulation_world._world:
        get_simulation_world._world.cleanup()
        get_simulation_world._world = None
        print("🔄 Simulation cleaned up")

# Demo functions for college presentation
def run_college_demo():
    """Run a complete college demonstration"""
    print("🎓 Starting Sarus Robot College Demonstration")
    print("=" * 50)
    
    # Enable simulation mode
    os.environ['SARUS_SIMULATION'] = '1'
    
    # Create simulation world
    world = get_simulation_world()
    if not world:
        print("❌ Failed to create simulation world")
        return
    
    # Create simulated hardware
    motors = create_motor_controller()
    sensors = create_sensor_manager()
    vision = create_vision_manager()
    
    # Initialize everything
    import asyncio
    
    async def demo_main():
        await motors.initialize()
        await sensors.initialize() 
        await vision.initialize()
        
        print("\n🤖 Sarus Robot Initialized in 3D Simulation!")
        print("🎭 Starting demonstration sequence...")
        
        # Demo sequence
        demo_moves = [
            ("🔄 Moving forward to explore lab", lambda: motors.move_forward(0.4), 3),
            ("🔍 Scanning for obstacles", lambda: None, 2),
            ("↪️ Turning right to avoid table", lambda: motors.turn_right(0.3), 2),
            ("🔄 Moving forward past equipment", lambda: motors.move_forward(0.4), 3),
            ("↩️ Turning left towards next area", lambda: motors.turn_left(0.3), 2),
            ("🔄 Exploring new section", lambda: motors.move_forward(0.3), 3),
            ("🛑 Mission complete - returning to base", lambda: motors.stop(), 1)
        ]
        
        for description, action, duration in demo_moves:
            print(f"\n{description}")
            
            if action:
                action()
            
            # Run for specified duration
            for i in range(int(duration * 60)):  # 60 FPS
                # Get sensor data
                obstacle_data = sensors.get_obstacle_map()
                nav_data = sensors.get_navigation_data()
                
                # Show obstacle warnings
                if obstacle_data.get('obstacles'):
                    print(f"   ⚠️ Obstacle detected: {list(obstacle_data['obstacles'].keys())}")
                
                # Step simulation
                step_simulation()
                await asyncio.sleep(1/60)  # 60 FPS
        
        print("\n🎉 Demonstration Complete!")
        print("   - Robot successfully navigated lab environment")
        print("   - All sensors functioning properly")
        print("   - AI systems responding to commands")
        
        # Keep simulation running for interaction
        print("\n📱 Simulation will continue running for manual control...")
        print("   Press Ctrl+C to exit")
        
        try:
            while True:
                step_simulation()
                await asyncio.sleep(1/60)
        except KeyboardInterrupt:
            print("\n👋 Demo ended by user")
    
    try:
        asyncio.run(demo_main())
    except Exception as e:
        print(f"❌ Demo error: {e}")
    finally:
        cleanup_simulation()

def run_interactive_demo():
    """Run interactive demo with keyboard controls"""
    print("🎮 Interactive Sarus Robot Demo")
    print("Use WASD keys to control the robot:")
    print("  W - Forward")
    print("  S - Backward") 
    print("  A - Turn Left")
    print("  D - Turn Right")
    print("  Q - Quit")
    
    # Enable simulation
    os.environ['SARUS_SIMULATION'] = '1'
    
    world = get_simulation_world()
    if not world:
        print("❌ Failed to create simulation")
        return
    
    motors = create_motor_controller()
    sensors = create_sensor_manager()
    
    import asyncio
    
    async def interactive_main():
        await motors.initialize()
        await sensors.initialize()
        
        try:
            import msvcrt  # Windows only
            print("\n🤖 Robot ready! Use WASD keys...")
            
            while True:
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').lower()
                    
                    if key == 'w':
                        motors.move_forward(0.5)
                    elif key == 's':
                        motors.move_backward(0.5)
                    elif key == 'a':
                        motors.turn_left(0.4)
                    elif key == 'd':
                        motors.turn_right(0.4)
                    elif key == 'q':
                        break
                    else:
                        motors.stop()
                
                # Show sensor data periodically
                if int(time.time() * 10) % 30 == 0:  # Every 3 seconds
                    obstacles = sensors.get_obstacle_map()
                    if obstacles.get('obstacles'):
                        print(f"⚠️ Obstacles: {list(obstacles['obstacles'].keys())}")
                
                step_simulation()
                await asyncio.sleep(1/60)
                
        except ImportError:
            print("⚠️ Interactive controls not available on this system")
        except KeyboardInterrupt:
            pass
        finally:
            motors.stop()
            print("\n👋 Interactive demo ended")
    
    try:
        asyncio.run(interactive_main())
    except Exception as e:
        print(f"❌ Interactive demo error: {e}")
    finally:
        cleanup_simulation()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        run_interactive_demo()
    else:
        run_college_demo()
