#!/usr/bin/env python3
"""
Raspberry Pi Hardware Validation Script for Sarus Robot

This script validates that all required hardware components are properly
connected and functioning on the Raspberry Pi.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class RaspberryPiValidator:
    """Hardware validation for Raspberry Pi setup"""
    
    def __init__(self):
        self.results = {}
        
    async def validate_system(self):
        """Run all validation tests"""
        print("🤖 Sarus Robot - Raspberry Pi Hardware Validation")
        print("=" * 50)
        
        # Check if running on Raspberry Pi
        await self.check_raspberry_pi()
        
        # System checks
        await self.check_python_environment()
        await self.check_gpio_access()
        
        # Hardware checks
        await self.check_camera()
        await self.check_audio()
        await self.check_gpio_pins()
        await self.check_i2c()
        
        # Software checks
        await self.check_dependencies()
        
        # Display results
        self.display_results()
        
    async def check_raspberry_pi(self):
        """Check if running on Raspberry Pi"""
        try:
            with open('/proc/device-tree/model', 'r') as f:
                model = f.read().strip('\x00')
                if 'Raspberry Pi' in model:
                    self.results['raspberry_pi'] = {'status': 'PASS', 'info': model}
                    print(f"✅ Running on: {model}")
                else:
                    self.results['raspberry_pi'] = {'status': 'FAIL', 'info': 'Not a Raspberry Pi'}
                    print(f"❌ Not running on Raspberry Pi: {model}")
        except Exception as e:
            self.results['raspberry_pi'] = {'status': 'FAIL', 'info': str(e)}
            print(f"❌ Could not detect Raspberry Pi: {e}")
    
    async def check_python_environment(self):
        """Check Python environment"""
        try:
            import sys
            version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            if sys.version_info >= (3, 8):
                self.results['python'] = {'status': 'PASS', 'info': f"Python {version}"}
                print(f"✅ Python version: {version}")
            else:
                self.results['python'] = {'status': 'WARN', 'info': f"Python {version} (3.8+ recommended)"}
                print(f"⚠️ Python version: {version} (3.8+ recommended)")
        except Exception as e:
            self.results['python'] = {'status': 'FAIL', 'info': str(e)}
            print(f"❌ Python check failed: {e}")
    
    async def check_gpio_access(self):
        """Check GPIO access permissions"""
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.cleanup()
            self.results['gpio_access'] = {'status': 'PASS', 'info': 'GPIO access available'}
            print("✅ GPIO access: Available")
        except ImportError:
            self.results['gpio_access'] = {'status': 'FAIL', 'info': 'RPi.GPIO not installed'}
            print("❌ GPIO access: RPi.GPIO not installed")
        except Exception as e:
            self.results['gpio_access'] = {'status': 'FAIL', 'info': str(e)}
            print(f"❌ GPIO access: {e}")
    
    async def check_camera(self):
        """Check camera availability"""
        try:
            # Try libcamera first (newer Pi OS)
            import subprocess
            result = subprocess.run(['libcamera-hello', '--help'], 
                                  capture_output=True, timeout=5)
            if result.returncode == 0:
                self.results['camera'] = {'status': 'PASS', 'info': 'libcamera available'}
                print("✅ Camera: libcamera available")
                return
        except:
            pass
        
        try:
            # Try legacy camera
            result = subprocess.run(['vcgencmd', 'get_camera'], 
                                  capture_output=True, text=True, timeout=5)
            if 'detected=1' in result.stdout:
                self.results['camera'] = {'status': 'PASS', 'info': 'Legacy camera detected'}
                print("✅ Camera: Legacy camera detected")
            else:
                self.results['camera'] = {'status': 'FAIL', 'info': 'No camera detected'}
                print("❌ Camera: No camera detected")
        except Exception as e:
            self.results['camera'] = {'status': 'WARN', 'info': f'Could not check camera: {e}'}
            print(f"⚠️ Camera: Could not check camera: {e}")
    
    async def check_audio(self):
        """Check audio devices"""
        try:
            import subprocess
            
            # Check audio output devices
            result = subprocess.run(['aplay', '-l'], capture_output=True, text=True)
            if result.returncode == 0 and 'card' in result.stdout:
                self.results['audio_output'] = {'status': 'PASS', 'info': 'Audio output available'}
                print("✅ Audio Output: Available")
            else:
                self.results['audio_output'] = {'status': 'FAIL', 'info': 'No audio output'}
                print("❌ Audio Output: No devices found")
            
            # Check audio input devices
            result = subprocess.run(['arecord', '-l'], capture_output=True, text=True)
            if result.returncode == 0 and 'card' in result.stdout:
                self.results['audio_input'] = {'status': 'PASS', 'info': 'Audio input available'}
                print("✅ Audio Input: Available")
            else:
                self.results['audio_input'] = {'status': 'WARN', 'info': 'No audio input'}
                print("⚠️ Audio Input: No devices found")
                
        except Exception as e:
            self.results['audio'] = {'status': 'FAIL', 'info': str(e)}
            print(f"❌ Audio check failed: {e}")
    
    async def check_gpio_pins(self):
        """Check specific GPIO pins for robot hardware"""
        try:
            import gpiozero
            from gpiozero import LED
            
            # Test pins (using safe pins that won't interfere)
            test_pins = [18, 19, 20, 21, 23, 24]
            working_pins = []
            
            for pin in test_pins:
                try:
                    led = LED(pin)
                    led.close()
                    working_pins.append(pin)
                except Exception:
                    pass
            
            if len(working_pins) >= 4:
                self.results['gpio_pins'] = {'status': 'PASS', 'info': f'{len(working_pins)} pins available'}
                print(f"✅ GPIO Pins: {len(working_pins)} pins available for robot hardware")
            else:
                self.results['gpio_pins'] = {'status': 'WARN', 'info': f'Only {len(working_pins)} pins available'}
                print(f"⚠️ GPIO Pins: Only {len(working_pins)} pins available")
                
        except ImportError:
            self.results['gpio_pins'] = {'status': 'FAIL', 'info': 'gpiozero not installed'}
            print("❌ GPIO Pins: gpiozero not installed")
        except Exception as e:
            self.results['gpio_pins'] = {'status': 'FAIL', 'info': str(e)}
            print(f"❌ GPIO Pins check failed: {e}")
    
    async def check_i2c(self):
        """Check I2C interface"""
        try:
            import subprocess
            result = subprocess.run(['i2cdetect', '-y', '1'], capture_output=True, text=True)
            if result.returncode == 0:
                self.results['i2c'] = {'status': 'PASS', 'info': 'I2C interface available'}
                print("✅ I2C Interface: Available")
            else:
                self.results['i2c'] = {'status': 'FAIL', 'info': 'I2C interface not available'}
                print("❌ I2C Interface: Not available")
        except Exception as e:
            self.results['i2c'] = {'status': 'WARN', 'info': f'Could not check I2C: {e}'}
            print(f"⚠️ I2C Interface: Could not check: {e}")
    
    async def check_dependencies(self):
        """Check required Python dependencies"""
        dependencies = [
            'numpy', 'opencv-python', 'Pillow', 'pygame',
            'pyaudio', 'pyttsx3', 'RPi.GPIO', 'gpiozero',
            'google-generativeai', 'openai', 'httpx'
        ]
        
        missing = []
        for dep in dependencies:
            try:
                __import__(dep.replace('-', '_'))
            except ImportError:
                missing.append(dep)
        
        if not missing:
            self.results['dependencies'] = {'status': 'PASS', 'info': 'All dependencies available'}
            print("✅ Dependencies: All required packages installed")
        else:
            self.results['dependencies'] = {'status': 'WARN', 'info': f'Missing: {", ".join(missing)}'}
            print(f"⚠️ Dependencies: Missing {len(missing)} packages: {', '.join(missing)}")
    
    def display_results(self):
        """Display validation summary"""
        print("\n" + "=" * 50)
        print("🏁 Validation Summary")
        print("=" * 50)
        
        pass_count = sum(1 for r in self.results.values() if r['status'] == 'PASS')
        warn_count = sum(1 for r in self.results.values() if r['status'] == 'WARN')
        fail_count = sum(1 for r in self.results.values() if r['status'] == 'FAIL')
        
        print(f"✅ PASS: {pass_count}")
        print(f"⚠️ WARN: {warn_count}")
        print(f"❌ FAIL: {fail_count}")
        
        if fail_count == 0:
            print("\n🎉 Your Raspberry Pi is ready for Sarus robot!")
        elif fail_count <= 2:
            print("\n⚠️ Your Raspberry Pi needs some setup before running Sarus robot.")
            print("Check the failed items above and run setup_raspberry_pi.sh")
        else:
            print("\n❌ Your Raspberry Pi needs significant setup.")
            print("Please run setup_raspberry_pi.sh to install required components.")
        
        print("\nNext steps:")
        print("1. Run setup script: ./setup_raspberry_pi.sh")
        print("2. Wire hardware components")
        print("3. Test components: python test_components.py")
        print("4. Start robot: python main.py")

async def main():
    """Main validation function"""
    validator = RaspberryPiValidator()
    await validator.validate_system()

if __name__ == "__main__":
    asyncio.run(main())
