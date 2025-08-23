"""
🚗 MOTOR CONTROLLER - Sarus Mobility Feature
DC motor control and movement coordination for robot locomotion

Handles DC motor control for robot movement including forward/backward
motion, turning, and speed control using L298N motor driver with safety features.
Integrates with Sarus navigation and emergency stop systems.
"""

import asyncio
import logging
import time
from typing import Tuple, Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# GPIO control libraries
try:
    import RPi.GPIO as GPIO
    RPI_GPIO_AVAILABLE = True
except ImportError:
    RPI_GPIO_AVAILABLE = False

try:
    from gpiozero import PWMOutputDevice, DigitalOutputDevice
    GPIOZERO_AVAILABLE = True
except ImportError:
    GPIOZERO_AVAILABLE = False

class MotorDirection(Enum):
    """Motor rotation directions"""
    FORWARD = "forward"
    BACKWARD = "backward"
    STOP = "stop"

@dataclass
class MotorCommand:
    """Motor control command"""
    left_speed: float   # -1.0 to 1.0
    right_speed: float  # -1.0 to 1.0
    duration: Optional[float] = None  # seconds, None for continuous
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class MotorController:
    """
    🚗 Enhanced Motor Control System for Sarus Robot
    
    Features:
    - Dual motor control (left/right wheels)
    - Speed control and direction management
    - Emergency stop capability
    - Movement coordination and safety
    - Integration with navigation system
    """
    
    def __init__(self, config=None):
        self.logger = logging.getLogger(__name__)
        self.config = config
        
        # Hardware configuration
        self.hardware_enabled = getattr(config, 'hardware_enabled', False) if config else False
        self.simulation_mode = getattr(config, 'simulation_mode', True) if config else True
        
        # Motor parameters
        self.max_speed = getattr(config, 'max_speed', 0.8) if config else 0.8
        self.turn_speed = getattr(config, 'turn_speed', 0.6) if config else 0.6
        
        # Motor control objects
        self.left_motor_forward = None
        self.left_motor_backward = None
        self.left_motor_enable = None
        self.right_motor_forward = None
        self.right_motor_backward = None
        self.right_motor_enable = None
        
        # Current state
        self.current_left_speed = 0.0
        self.current_right_speed = 0.0
        self.current_direction = MotorDirection.STOP
        self.is_moving = False
        
        # Safety
        self.emergency_stop_active = False
        self.max_continuous_time = SYSTEM_CONFIG.get('max_continuous_movement_time', 30)
        self.movement_start_time = None
        
    async def initialize(self):
        """Initialize motor control system"""
        self.logger.info("🚗 Initializing motor controller...")
        
        if not self.hardware_enabled:
            self.logger.info("Hardware disabled - motor control in simulation mode")
            return
        
        try:
            await self._setup_gpio()
            await self._test_motors()
            
            self.logger.info("✅ Motor controller initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize motor controller: {e}")
            self.hardware_enabled = False  # Fallback to simulation
    
    async def _setup_gpio(self):
        """Setup GPIO pins for motor control"""
        if not (RPI_GPIO_AVAILABLE or GPIOZERO_AVAILABLE):
            raise RuntimeError("No GPIO library available")
        
        # Pin assignments
        pin_config = {
            'left_forward': self.gpio_pins.get('motor_left_forward', 18),
            'left_backward': self.gpio_pins.get('motor_left_backward', 19),
            'left_enable': self.gpio_pins.get('motor_left_enable', 12),
            'right_forward': self.gpio_pins.get('motor_right_forward', 20),
            'right_backward': self.gpio_pins.get('motor_right_backward', 21),
            'right_enable': self.gpio_pins.get('motor_right_enable', 13),
        }
        
        if GPIOZERO_AVAILABLE:
            # Use gpiozero for cleaner PWM control
            self.left_motor_forward = DigitalOutputDevice(pin_config['left_forward'])
            self.left_motor_backward = DigitalOutputDevice(pin_config['left_backward'])
            self.left_motor_enable = PWMOutputDevice(pin_config['left_enable'])
            
            self.right_motor_forward = DigitalOutputDevice(pin_config['right_forward'])
            self.right_motor_backward = DigitalOutputDevice(pin_config['right_backward'])
            self.right_motor_enable = PWMOutputDevice(pin_config['right_enable'])
            
        elif RPI_GPIO_AVAILABLE:
            # Fallback to RPi.GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            # Setup pins
            for pin in pin_config.values():
                GPIO.setup(pin, GPIO.OUT)
            
            # Create PWM instances for speed control
            self.left_motor_enable = GPIO.PWM(pin_config['left_enable'], 1000)  # 1kHz
            self.right_motor_enable = GPIO.PWM(pin_config['right_enable'], 1000)
            
            self.left_motor_enable.start(0)
            self.right_motor_enable.start(0)
        
        self.logger.info(f"GPIO pins configured: {pin_config}")
    
    async def _test_motors(self):
        """Test motor functionality"""
        if not self.hardware_enabled:
            return
        
        self.logger.info("🧪 Testing motors...")
        
        # Brief forward movement test
        await self.move_forward(0.3, duration=0.5)
        await asyncio.sleep(0.5)
        
        # Brief turn test
        await self.turn_left(0.3, duration=0.5)
        await asyncio.sleep(0.5)
        
        await self.stop()
        
        self.logger.info("✅ Motor test completed")
    
    async def move_forward(self, speed: float = None, duration: Optional[float] = None):
        """
        Move robot forward
        
        Args:
            speed: Motor speed (0.0 to 1.0), uses max_speed if None
            duration: Movement duration in seconds, infinite if None
        """
        if speed is None:
            speed = self.max_speed
        
        speed = max(0.0, min(1.0, speed))  # Clamp to valid range
        
        self.logger.info(f"🚀 Moving forward at speed {speed}")
        
        if self.emergency_stop_active:
            self.logger.warning("Emergency stop active - movement blocked")
            return
        
        await self._set_motor_direction(MotorDirection.FORWARD)
        await self._set_motor_speeds(speed, speed)
        
        self.current_direction = MotorDirection.FORWARD
        self.is_moving = True
        self.movement_start_time = time.time()
        
        if duration:
            await asyncio.sleep(duration)
            await self.stop()
    
    async def move_backward(self, speed: float = None, duration: Optional[float] = None):
        """
        Move robot backward
        
        Args:
            speed: Motor speed (0.0 to 1.0), uses max_speed if None
            duration: Movement duration in seconds, infinite if None
        """
        if speed is None:
            speed = self.max_speed
        
        speed = max(0.0, min(1.0, speed))
        
        self.logger.info(f"🔙 Moving backward at speed {speed}")
        
        if self.emergency_stop_active:
            self.logger.warning("Emergency stop active - movement blocked")
            return
        
        await self._set_motor_direction(MotorDirection.BACKWARD)
        await self._set_motor_speeds(speed, speed)
        
        self.current_direction = MotorDirection.BACKWARD
        self.is_moving = True
        self.movement_start_time = time.time()
        
        if duration:
            await asyncio.sleep(duration)
            await self.stop()
    
    async def turn_left(self, speed: float = None, duration: Optional[float] = None):
        """
        Turn robot left
        
        Args:
            speed: Turn speed (0.0 to 1.0), uses turn_speed if None
            duration: Turn duration in seconds, infinite if None
        """
        if speed is None:
            speed = self.turn_speed
        
        speed = max(0.0, min(1.0, speed))
        
        self.logger.info(f"↰ Turning left at speed {speed}")
        
        if self.emergency_stop_active:
            self.logger.warning("Emergency stop active - movement blocked")
            return
        
        # Left motor backward, right motor forward for left turn
        await self._set_individual_motor_direction(
            left_direction=MotorDirection.BACKWARD,
            right_direction=MotorDirection.FORWARD
        )
        await self._set_motor_speeds(speed, speed)
        
        self.is_moving = True
        self.movement_start_time = time.time()
        
        if duration:
            await asyncio.sleep(duration)
            await self.stop()
    
    async def turn_right(self, speed: float = None, duration: Optional[float] = None):
        """
        Turn robot right
        
        Args:
            speed: Turn speed (0.0 to 1.0), uses turn_speed if None
            duration: Turn duration in seconds, infinite if None
        """
        if speed is None:
            speed = self.turn_speed
        
        speed = max(0.0, min(1.0, speed))
        
        self.logger.info(f"↱ Turning right at speed {speed}")
        
        if self.emergency_stop_active:
            self.logger.warning("Emergency stop active - movement blocked")
            return
        
        # Left motor forward, right motor backward for right turn
        await self._set_individual_motor_direction(
            left_direction=MotorDirection.FORWARD,
            right_direction=MotorDirection.BACKWARD
        )
        await self._set_motor_speeds(speed, speed)
        
        self.is_moving = True
        self.movement_start_time = time.time()
        
        if duration:
            await asyncio.sleep(duration)
            await self.stop()
    
    async def stop(self):
        """Stop all motor movement"""
        self.logger.info("🛑 Stopping motors")
        
        await self._set_motor_speeds(0.0, 0.0)
        await self._set_motor_direction(MotorDirection.STOP)
        
        self.current_direction = MotorDirection.STOP
        self.is_moving = False
        self.movement_start_time = None
        self.current_left_speed = 0.0
        self.current_right_speed = 0.0
    
    async def emergency_stop(self):
        """Emergency stop - immediately halt all movement"""
        self.logger.warning("🚨 EMERGENCY STOP ACTIVATED")
        
        self.emergency_stop_active = True
        await self.stop()
        
        # Additional safety delay
        await asyncio.sleep(0.1)
    
    def clear_emergency_stop(self):
        """Clear emergency stop condition"""
        self.emergency_stop_active = False
        self.logger.info("✅ Emergency stop cleared")
    
    async def _set_motor_direction(self, direction: MotorDirection):
        """Set direction for both motors"""
        await self._set_individual_motor_direction(direction, direction)
    
    async def _set_individual_motor_direction(
        self, 
        left_direction: MotorDirection, 
        right_direction: MotorDirection
    ):
        """Set direction for individual motors"""
        if not self.hardware_enabled:
            return
        
        # Left motor direction
        if GPIOZERO_AVAILABLE:
            if left_direction == MotorDirection.FORWARD:
                self.left_motor_forward.on()
                self.left_motor_backward.off()
            elif left_direction == MotorDirection.BACKWARD:
                self.left_motor_forward.off()
                self.left_motor_backward.on()
            else:  # STOP
                self.left_motor_forward.off()
                self.left_motor_backward.off()
            
            # Right motor direction
            if right_direction == MotorDirection.FORWARD:
                self.right_motor_forward.on()
                self.right_motor_backward.off()
            elif right_direction == MotorDirection.BACKWARD:
                self.right_motor_forward.off()
                self.right_motor_backward.on()
            else:  # STOP
                self.right_motor_forward.off()
                self.right_motor_backward.off()
        
        elif RPI_GPIO_AVAILABLE:
            # Left motor
            left_forward_pin = self.gpio_pins.get('motor_left_forward', 18)
            left_backward_pin = self.gpio_pins.get('motor_left_backward', 19)
            
            if left_direction == MotorDirection.FORWARD:
                GPIO.output(left_forward_pin, GPIO.HIGH)
                GPIO.output(left_backward_pin, GPIO.LOW)
            elif left_direction == MotorDirection.BACKWARD:
                GPIO.output(left_forward_pin, GPIO.LOW)
                GPIO.output(left_backward_pin, GPIO.HIGH)
            else:  # STOP
                GPIO.output(left_forward_pin, GPIO.LOW)
                GPIO.output(left_backward_pin, GPIO.LOW)
            
            # Right motor
            right_forward_pin = self.gpio_pins.get('motor_right_forward', 20)
            right_backward_pin = self.gpio_pins.get('motor_right_backward', 21)
            
            if right_direction == MotorDirection.FORWARD:
                GPIO.output(right_forward_pin, GPIO.HIGH)
                GPIO.output(right_backward_pin, GPIO.LOW)
            elif right_direction == MotorDirection.BACKWARD:
                GPIO.output(right_forward_pin, GPIO.LOW)
                GPIO.output(right_backward_pin, GPIO.HIGH)
            else:  # STOP
                GPIO.output(right_forward_pin, GPIO.LOW)
                GPIO.output(right_backward_pin, GPIO.LOW)
    
    async def _set_motor_speeds(self, left_speed: float, right_speed: float):
        """Set PWM speed for motors"""
        left_speed = max(0.0, min(1.0, left_speed))
        right_speed = max(0.0, min(1.0, right_speed))
        
        self.current_left_speed = left_speed
        self.current_right_speed = right_speed
        
        if not self.hardware_enabled:
            return
        
        if GPIOZERO_AVAILABLE:
            self.left_motor_enable.value = left_speed
            self.right_motor_enable.value = right_speed
        
        elif RPI_GPIO_AVAILABLE:
            self.left_motor_enable.ChangeDutyCycle(left_speed * 100)
            self.right_motor_enable.ChangeDutyCycle(right_speed * 100)
    
    async def differential_drive(self, left_speed: float, right_speed: float):
        """
        Direct control of individual motor speeds for differential drive
        
        Args:
            left_speed: Left motor speed (-1.0 to 1.0, negative for reverse)
            right_speed: Right motor speed (-1.0 to 1.0, negative for reverse)
        """
        if self.emergency_stop_active:
            self.logger.warning("Emergency stop active - movement blocked")
            return
        
        # Clamp speeds
        left_speed = max(-1.0, min(1.0, left_speed))
        right_speed = max(-1.0, min(1.0, right_speed))
        
        # Set directions based on speed signs
        left_direction = MotorDirection.FORWARD if left_speed >= 0 else MotorDirection.BACKWARD
        right_direction = MotorDirection.FORWARD if right_speed >= 0 else MotorDirection.BACKWARD
        
        await self._set_individual_motor_direction(left_direction, right_direction)
        await self._set_motor_speeds(abs(left_speed), abs(right_speed))
        
        self.is_moving = abs(left_speed) > 0.01 or abs(right_speed) > 0.01
        
        if self.is_moving and not self.movement_start_time:
            self.movement_start_time = time.time()
        elif not self.is_moving:
            self.movement_start_time = None
    
    def get_status(self) -> dict:
        """Get current motor status"""
        return {
            'is_moving': self.is_moving,
            'direction': self.current_direction.value,
            'left_speed': self.current_left_speed,
            'right_speed': self.current_right_speed,
            'emergency_stop': self.emergency_stop_active,
            'hardware_enabled': self.hardware_enabled,
            'movement_duration': (
                time.time() - self.movement_start_time 
                if self.movement_start_time else 0
            )
        }
    
    async def check_safety_limits(self):
        """Check and enforce safety limits"""
        if (self.is_moving and 
            self.movement_start_time and 
            time.time() - self.movement_start_time > self.max_continuous_time):
            
            self.logger.warning(
                f"Maximum continuous movement time ({self.max_continuous_time}s) exceeded"
            )
            await self.emergency_stop()
    
    def stop_all_motors(self):
        """Synchronous emergency stop for shutdown"""
        if not self.hardware_enabled:
            return
        
        try:
            if GPIOZERO_AVAILABLE:
                if self.left_motor_enable:
                    self.left_motor_enable.value = 0
                if self.right_motor_enable:
                    self.right_motor_enable.value = 0
                if self.left_motor_forward:
                    self.left_motor_forward.off()
                if self.left_motor_backward:
                    self.left_motor_backward.off()
                if self.right_motor_forward:
                    self.right_motor_forward.off()
                if self.right_motor_backward:
                    self.right_motor_backward.off()
            
            elif RPI_GPIO_AVAILABLE:
                GPIO.cleanup()
            
            self.logger.info("🛑 All motors stopped for shutdown")
            
        except Exception as e:
            self.logger.error(f"Error stopping motors: {e}")
    
    def cleanup(self):
        """Clean up motor controller resources"""
        self.stop_all_motors()
        
        if GPIOZERO_AVAILABLE:
            # gpiozero handles cleanup automatically
            pass
        elif RPI_GPIO_AVAILABLE:
            GPIO.cleanup()
        
        self.logger.info("🧹 Motor controller cleanup complete")
