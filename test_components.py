# Simple Test Scripts for Sarus Robot Components

"""
Simple test scripts for verifying that Sarus robot components can be imported
and initialized correctly. These tests don't require hardware.
"""

import asyncio
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
# Also add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

class ComponentTester:
    """Test runner for individual robot components."""
    
    def __init__(self):
        print("Sarus Robot Component Tester")
        print("=" * 40)
    
    async def test_sensors(self):
        """Test sensor manager initialization."""
        print("\n🔍 Testing Sensor Manager...")
        try:
            from hardware.sensor_manager import SensorManager
            
            sensor_manager = SensorManager()
            await sensor_manager.initialize()
            
            # Test basic methods
            obstacle_map = sensor_manager.get_obstacle_map()
            print(f"✅ Obstacle map: {obstacle_map}")
            
            nav_data = sensor_manager.get_navigation_data()
            print(f"✅ Navigation data available: {list(nav_data.keys())}")
            
            battery = sensor_manager.get_battery_level()
            if battery:
                print(f"✅ Battery level: {battery:.1f}%")
            
            sensor_manager.cleanup()
            print("✅ Sensor Manager test completed")
            
        except Exception as e:
            print(f"❌ Sensor Manager test failed: {e}")
    
    async def test_motors(self):
        """Test motor controller initialization."""
        print("\n🚗 Testing Motor Controller...")
        try:
            from hardware.motor_controller import MotorController
            
            motor_controller = MotorController()
            await motor_controller.initialize()
            
            print("✅ Motor controller initialized")
            
            # Test that methods exist (but don't actually move in test)
            if hasattr(motor_controller, 'move_forward'):
                print("✅ move_forward method available")
            if hasattr(motor_controller, 'turn_left'):
                print("✅ turn_left method available")
            if hasattr(motor_controller, 'stop'):
                print("✅ stop method available")
            
            motor_controller.cleanup()
            print("✅ Motor Controller test completed")
            
        except Exception as e:
            print(f"❌ Motor Controller test failed: {e}")
    
    async def test_display(self):
        """Test display controller initialization."""
        print("\n💡 Testing Display Controller...")
        try:
            from hardware.display_controller import DisplayController
            
            display_controller = DisplayController()
            await display_controller.initialize()
            
            print("✅ Display controller initialized")
            
            # Check available methods
            if hasattr(display_controller, 'show_status'):
                print("✅ show_status method available")
            if hasattr(display_controller, 'set_brightness'):
                print("✅ set_brightness method available")
            
            display_controller.cleanup()
            print("✅ Display Controller test completed")
            
        except Exception as e:
            print(f"❌ Display Controller test failed: {e}")
    
    async def test_speech(self):
        """Test speech manager initialization."""
        print("\n🎤 Testing Speech Manager...")
        try:
            from ai.speech_manager import SpeechManager
            
            speech_manager = SpeechManager()
            await speech_manager.initialize()
            
            print("✅ Speech manager initialized")
            
            # Check available methods
            if hasattr(speech_manager, 'speak'):
                print("✅ speak method available")
            if hasattr(speech_manager, 'listen'):
                print("✅ listen method available")
            
            speech_manager.cleanup()
            print("✅ Speech Manager test completed")
            
        except Exception as e:
            print(f"❌ Speech Manager test failed: {e}")
    
    async def test_vision(self):
        """Test vision manager initialization."""
        print("\n👁️ Testing Vision Manager...")
        try:
            from ai.vision_manager import VisionManager
            
            vision_manager = VisionManager()
            await vision_manager.initialize()
            
            print("✅ Vision manager initialized")
            
            # Check available methods
            if hasattr(vision_manager, 'capture_image'):
                print("✅ capture_image method available")
            if hasattr(vision_manager, 'analyze_scene'):
                print("✅ analyze_scene method available")
            
            vision_manager.cleanup()
            print("✅ Vision Manager test completed")
            
        except Exception as e:
            print(f"❌ Vision Manager test failed: {e}")
    
    async def test_llm(self):
        """Test LLM manager initialization."""
        print("\n🧠 Testing LLM Manager...")
        try:
            from ai.llm_manager import LLMManager
            
            llm_manager = LLMManager()
            await llm_manager.initialize()
            
            print("✅ LLM manager initialized")
            
            # Check available methods
            if hasattr(llm_manager, 'process_query'):
                print("✅ process_query method available")
            if hasattr(llm_manager, 'generate_text'):
                print("✅ generate_text method available")
            
            # Note: LLMManager may not have cleanup method
            print("✅ LLM Manager test completed")
            
        except Exception as e:
            print(f"❌ LLM Manager test failed: {e}")
    
    async def test_navigation(self):
        """Test navigation manager initialization."""
        print("\n🧭 Testing Navigation Manager...")
        try:
            from navigation.navigation_manager import NavigationManager
            from hardware.sensor_manager import SensorManager
            from hardware.motor_controller import MotorController
            from ai.vision_manager import VisionManager
            
            # Initialize dependencies
            sensor_manager = SensorManager()
            motor_controller = MotorController()
            vision_manager = VisionManager()
            
            await sensor_manager.initialize()
            await motor_controller.initialize()
            await vision_manager.initialize()
            
            nav_manager = NavigationManager(
                motor_controller,
                sensor_manager, 
                vision_manager
            )
            
            print("✅ Navigation manager initialized")
            
            # Check available methods
            if hasattr(nav_manager, 'start_exploration'):
                print("✅ start_exploration method available")
            if hasattr(nav_manager, 'navigate_to_target'):
                print("✅ navigate_to_target method available")
            
            # Cleanup
            sensor_manager.cleanup()
            motor_controller.cleanup()
            vision_manager.cleanup()
            
            print("✅ Navigation Manager test completed")
            
        except Exception as e:
            print(f"❌ Navigation Manager test failed: {e}")
    
    async def test_robot_integration(self):
        """Test full robot integration."""
        print("\n🤖 Testing Full Robot Integration...")
        try:
            from core.robot import SarusRobot
            
            robot = SarusRobot()
            await robot.initialize()
            
            print("✅ Sarus robot initialized successfully")
            print(f"✅ Robot state: {robot.state}")
            
            robot.shutdown()
            print("✅ Robot Integration test completed")
            
        except Exception as e:
            print(f"❌ Robot Integration test failed: {e}")

async def run_all_tests():
    """Run all component tests."""
    tester = ComponentTester()
    
    await tester.test_sensors()
    await tester.test_motors()
    await tester.test_display()
    await tester.test_speech()
    await tester.test_vision()
    await tester.test_llm()
    await tester.test_navigation()
    await tester.test_robot_integration()
    
    print("\n🎉 All tests completed!")

async def run_hardware_tests():
    """Run only hardware-related tests."""
    tester = ComponentTester()
    
    await tester.test_sensors()
    await tester.test_motors()
    await tester.test_display()
    
    print("\n🔧 Hardware tests completed!")

async def run_ai_tests():
    """Run only AI-related tests."""
    tester = ComponentTester()
    
    await tester.test_speech()
    await tester.test_vision()
    await tester.test_llm()
    
    print("\n🤖 AI tests completed!")

if __name__ == "__main__":
    print("Sarus Robot Component Test Suite")
    print("Choose test mode:")
    print("1. All tests")
    print("2. Hardware only")
    print("3. AI only")
    print("4. Individual component")
    print("5. Robot integration")
    
    choice = input("Enter choice (1-5): ").strip()
    
    if choice == "1":
        asyncio.run(run_all_tests())
    elif choice == "2":
        asyncio.run(run_hardware_tests())
    elif choice == "3":
        asyncio.run(run_ai_tests())
    elif choice == "4":
        print("\nIndividual tests:")
        print("a. Sensors")
        print("b. Motors") 
        print("c. Display")
        print("d. Speech")
        print("e. Vision")
        print("f. LLM")
        print("g. Navigation")
        
        test_choice = input("Enter test (a-g): ").strip().lower()
        tester = ComponentTester()
        
        if test_choice == "a":
            asyncio.run(tester.test_sensors())
        elif test_choice == "b":
            asyncio.run(tester.test_motors())
        elif test_choice == "c":
            asyncio.run(tester.test_display())
        elif test_choice == "d":
            asyncio.run(tester.test_speech())
        elif test_choice == "e":
            asyncio.run(tester.test_vision())
        elif test_choice == "f":
            asyncio.run(tester.test_llm())
        elif test_choice == "g":
            asyncio.run(tester.test_navigation())
        else:
            print("Invalid choice")
    elif choice == "5":
        tester = ComponentTester()
        asyncio.run(tester.test_robot_integration())
    else:
        print("Invalid choice")
