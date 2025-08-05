"""
Display controller for Sarus robot

Manages LED matrix display, OLED screen, or other visual output devices
for showing robot facial expressions, status indicators, and information.
"""

import asyncio
import logging
import time
from typing import List, Tuple, Optional
from enum import Enum
import math

# Display libraries
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

# GPIO for LED control
try:
    import RPi.GPIO as GPIO
    RPI_GPIO_AVAILABLE = True
except ImportError:
    RPI_GPIO_AVAILABLE = False

try:
    from gpiozero import LED, PWMOutputDevice
    GPIOZERO_AVAILABLE = True
except ImportError:
    GPIOZERO_AVAILABLE = False

from ..config.settings import SYSTEM_CONFIG
from ..utils.logger import get_logger

class DisplayState(Enum):
    """Robot display states"""
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"
    HAPPY = "happy"
    ERROR = "error"
    SHUTDOWN = "shutdown"

class DisplayController:
    """
    Controls visual display elements including LED matrix, status LEDs,
    and facial expressions for robot communication
    """
    
    def __init__(self):
        self.logger = get_logger(__name__)
        
        # Configuration
        self.hardware_enabled = SYSTEM_CONFIG.get('hardware_enabled', False)
        self.display_type = SYSTEM_CONFIG.get('display_type', 'led_matrix')
        self.display_width = SYSTEM_CONFIG.get('display_width', 8)
        self.display_height = SYSTEM_CONFIG.get('display_height', 8)
        self.brightness = SYSTEM_CONFIG.get('display_brightness', 128)
        self.gpio_pins = SYSTEM_CONFIG.get('gpio_pins', {})
        
        # Display state
        self.current_state = DisplayState.IDLE
        self.animation_active = False
        self.animation_task = None
        
        # Hardware components
        self.led_matrix = None
        self.status_leds = {}
        
        # Animation patterns
        self.current_frame = 0
        self.animation_speed = 0.1  # seconds per frame
        
    async def initialize(self):
        """Initialize display systems"""
        self.logger.info("💡 Initializing display controller...")
        
        if not self.hardware_enabled:
            self.logger.info("Hardware disabled - display in simulation mode")
            return
        
        try:
            if self.display_type == 'led_matrix':
                await self._setup_led_matrix()
            elif self.display_type == 'oled':
                await self._setup_oled()
            
            await self._setup_status_leds()
            await self._test_display()
            
            self.logger.info("✅ Display controller initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize display: {e}")
            self.hardware_enabled = False  # Fallback to simulation
    
    async def _setup_led_matrix(self):
        """Setup LED matrix display"""
        self.logger.info("Setting up LED matrix display")
        
        # This would initialize LED matrix driver
        # For now, we'll simulate the display
        if self.hardware_enabled:
            # Initialize matrix driver pins
            data_pin = self.gpio_pins.get('led_matrix_data', 10)
            clock_pin = self.gpio_pins.get('led_matrix_clock', 11)
            latch_pin = self.gpio_pins.get('led_matrix_latch', 9)
            
            self.logger.info(f"LED matrix pins: data={data_pin}, clock={clock_pin}, latch={latch_pin}")
    
    async def _setup_oled(self):
        """Setup OLED display"""
        self.logger.info("OLED display setup placeholder")
        # OLED initialization would go here
    
    async def _setup_status_leds(self):
        """Setup status indicator LEDs"""
        if not GPIOZERO_AVAILABLE:
            return
        
        led_pins = {
            'red': self.gpio_pins.get('status_led_red', 16),
            'green': self.gpio_pins.get('status_led_green', 26),
            'blue': self.gpio_pins.get('status_led_blue', 6)
        }
        
        for color, pin in led_pins.items():
            try:
                self.status_leds[color] = PWMOutputDevice(pin)
                self.logger.info(f"Status LED {color} initialized on pin {pin}")
            except Exception as e:
                self.logger.warning(f"Failed to initialize {color} LED: {e}")
    
    async def _test_display(self):
        """Test display functionality"""
        self.logger.info("🧪 Testing display...")
        
        # Test status LEDs
        for color in ['red', 'green', 'blue']:
            await self._set_status_led(color, 0.5)
            await asyncio.sleep(0.2)
            await self._set_status_led(color, 0.0)
        
        # Test display pattern
        await self._show_test_pattern()
        
        self.logger.info("✅ Display test completed")
    
    async def _show_test_pattern(self):
        """Show test pattern on display"""
        if self.display_type == 'led_matrix':
            # Create simple test pattern
            pattern = self._create_smile_pattern()
            await self._display_pattern(pattern, duration=1.0)
    
    async def show_startup_animation(self):
        """Show startup animation"""
        self.logger.info("🎭 Showing startup animation")
        
        if not self.hardware_enabled:
            await asyncio.sleep(2.0)  # Simulate animation time
            return
        
        # Startup sequence
        await self._set_status_color('blue', 1.0)
        
        # Show boot sequence on display
        patterns = [
            self._create_dot_pattern(),
            self._create_line_pattern(),
            self._create_smile_pattern()
        ]
        
        for pattern in patterns:
            await self._display_pattern(pattern, duration=0.5)
        
        await self._set_status_color('green', 0.5)
        self.current_state = DisplayState.IDLE
    
    async def show_idle_face(self):
        """Show idle facial expression"""
        if self.current_state == DisplayState.IDLE:
            return
        
        self.current_state = DisplayState.IDLE
        await self._stop_animation()
        
        if self.hardware_enabled:
            pattern = self._create_idle_pattern()
            await self._display_pattern(pattern)
            await self._set_status_color('green', 0.3)
        
        self.logger.debug("😐 Showing idle face")
    
    async def show_listening_animation(self):
        """Show listening animation with visual feedback"""
        self.current_state = DisplayState.LISTENING
        
        if self.hardware_enabled:
            await self._set_status_color('blue', 0.8)
            await self._start_animation(self._listening_animation)
        
        self.logger.debug("👂 Showing listening animation")
    
    async def show_thinking_animation(self):
        """Show thinking/processing animation"""
        self.current_state = DisplayState.THINKING
        
        if self.hardware_enabled:
            await self._set_status_color('yellow', 0.6)
            await self._start_animation(self._thinking_animation)
        
        self.logger.debug("🤔 Showing thinking animation")
    
    async def show_speaking_animation(self):
        """Show speaking animation with mouth movement"""
        self.current_state = DisplayState.SPEAKING
        
        if self.hardware_enabled:
            await self._set_status_color('green', 0.8)
            await self._start_animation(self._speaking_animation)
        
        self.logger.debug("🗣️ Showing speaking animation")
    
    async def show_happy_animation(self):
        """Show happy expression"""
        self.current_state = DisplayState.HAPPY
        
        if self.hardware_enabled:
            await self._set_status_color('green', 1.0)
            pattern = self._create_happy_pattern()
            await self._display_pattern(pattern, duration=2.0)
        
        self.logger.debug("😊 Showing happy animation")
    
    async def show_error_animation(self):
        """Show error indication"""
        self.current_state = DisplayState.ERROR
        
        if self.hardware_enabled:
            await self._set_status_color('red', 1.0)
            
            # Blink error pattern
            for _ in range(3):
                pattern = self._create_error_pattern()
                await self._display_pattern(pattern, duration=0.3)
                await self._clear_display()
                await asyncio.sleep(0.3)
        
        self.logger.debug("❌ Showing error animation")
    
    async def show_shutdown_animation(self):
        """Show shutdown animation"""
        self.current_state = DisplayState.SHUTDOWN
        
        if self.hardware_enabled:
            # Fade out sequence
            patterns = [
                self._create_smile_pattern(),
                self._create_dot_pattern(),
                self._create_empty_pattern()
            ]
            
            for pattern in patterns:
                await self._display_pattern(pattern, duration=0.5)
            
            # Turn off all LEDs
            await self._set_status_color('off')
        
        self.logger.debug("🔌 Showing shutdown animation")
    
    async def _start_animation(self, animation_func):
        """Start continuous animation"""
        await self._stop_animation()
        
        self.animation_active = True
        self.animation_task = asyncio.create_task(self._animation_loop(animation_func))
    
    async def _stop_animation(self):
        """Stop current animation"""
        self.animation_active = False
        
        if self.animation_task:
            self.animation_task.cancel()
            try:
                await self.animation_task
            except asyncio.CancelledError:
                pass
    
    async def _animation_loop(self, animation_func):
        """Animation loop for continuous animations"""
        self.current_frame = 0
        
        while self.animation_active:
            try:
                pattern = animation_func()
                await self._display_pattern(pattern)
                
                self.current_frame = (self.current_frame + 1) % 8  # Reset after 8 frames
                await asyncio.sleep(self.animation_speed)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Animation error: {e}")
                break
    
    def _listening_animation(self) -> List[List[int]]:
        """Generate listening animation frame"""
        # Pulsing ears effect
        intensity = int(128 + 100 * math.sin(self.current_frame * 0.5))
        
        pattern = self._create_empty_pattern()
        
        # Add "ears" that pulse
        if self.current_frame % 4 < 2:
            pattern[1][1] = intensity
            pattern[1][6] = intensity
            pattern[2][0] = intensity
            pattern[2][7] = intensity
        
        # Eyes
        pattern[3][2] = 255
        pattern[3][5] = 255
        
        return pattern
    
    def _thinking_animation(self) -> List[List[int]]:
        """Generate thinking animation frame"""
        pattern = self._create_empty_pattern()
        
        # Eyes looking around
        eye_positions = [(2, 1), (2, 2), (2, 1), (1, 1)]
        eye_pos = eye_positions[self.current_frame % len(eye_positions)]
        
        pattern[eye_pos[0]][eye_pos[1]] = 255  # Left eye
        pattern[eye_pos[0]][eye_pos[1] + 4] = 255  # Right eye
        
        # Thinking dots
        if self.current_frame % 6 < 3:
            pattern[6][6] = 128
        if self.current_frame % 6 < 2:
            pattern[6][7] = 128
        if self.current_frame % 6 < 1:
            pattern[7][7] = 128
        
        return pattern
    
    def _speaking_animation(self) -> List[List[int]]:
        """Generate speaking animation frame"""
        pattern = self._create_smile_pattern()
        
        # Animated mouth
        mouth_frames = [
            [(5, 3), (5, 4)],  # Small mouth
            [(5, 2), (5, 3), (5, 4), (5, 5)],  # Open mouth
            [(4, 2), (4, 3), (4, 4), (4, 5), (5, 2), (5, 5)],  # Wide mouth
            [(5, 3), (5, 4)]  # Back to small
        ]
        
        mouth_frame = mouth_frames[self.current_frame % len(mouth_frames)]
        
        # Clear mouth area first
        for row in range(4, 7):
            for col in range(2, 6):
                pattern[row][col] = 0
        
        # Draw animated mouth
        for row, col in mouth_frame:
            if 0 <= row < len(pattern) and 0 <= col < len(pattern[0]):
                pattern[row][col] = 255
        
        return pattern
    
    def _create_empty_pattern(self) -> List[List[int]]:
        """Create empty display pattern"""
        return [[0 for _ in range(self.display_width)] for _ in range(self.display_height)]
    
    def _create_dot_pattern(self) -> List[List[int]]:
        """Create single dot pattern"""
        pattern = self._create_empty_pattern()
        center = self.display_width // 2
        pattern[center][center] = 255
        return pattern
    
    def _create_line_pattern(self) -> List[List[int]]:
        """Create horizontal line pattern"""
        pattern = self._create_empty_pattern()
        row = self.display_height // 2
        for col in range(self.display_width):
            pattern[row][col] = 128
        return pattern
    
    def _create_smile_pattern(self) -> List[List[int]]:
        """Create smile face pattern"""
        pattern = self._create_empty_pattern()
        
        # Eyes
        pattern[2][2] = 255
        pattern[2][5] = 255
        
        # Smile
        pattern[5][2] = 255
        pattern[5][5] = 255
        pattern[6][3] = 255
        pattern[6][4] = 255
        
        return pattern
    
    def _create_happy_pattern(self) -> List[List[int]]:
        """Create happy face pattern"""
        pattern = self._create_empty_pattern()
        
        # Happy eyes (^_^)
        pattern[2][1] = 255
        pattern[1][2] = 255
        pattern[2][3] = 255
        
        pattern[2][4] = 255
        pattern[1][5] = 255
        pattern[2][6] = 255
        
        # Big smile
        pattern[5][1] = 255
        pattern[5][6] = 255
        pattern[6][2] = 255
        pattern[6][5] = 255
        pattern[7][3] = 255
        pattern[7][4] = 255
        
        return pattern
    
    def _create_idle_pattern(self) -> List[List[int]]:
        """Create neutral idle pattern"""
        pattern = self._create_empty_pattern()
        
        # Simple eyes
        pattern[3][2] = 128
        pattern[3][5] = 128
        
        # Neutral mouth
        pattern[5][3] = 64
        pattern[5][4] = 64
        
        return pattern
    
    def _create_error_pattern(self) -> List[List[int]]:
        """Create error/X pattern"""
        pattern = self._create_empty_pattern()
        
        # X pattern
        for i in range(self.display_width):
            pattern[i][i] = 255
            pattern[i][self.display_width - 1 - i] = 255
        
        return pattern
    
    async def _display_pattern(self, pattern: List[List[int]], duration: Optional[float] = None):
        """Display pattern on LED matrix"""
        if not self.hardware_enabled:
            return
        
        # This would send the pattern to the actual LED matrix
        # For now, just log it in debug mode
        if SYSTEM_CONFIG.get('debug_mode', False):
            self.logger.debug(f"Display pattern: {len(pattern)}x{len(pattern[0]) if pattern else 0}")
        
        if duration:
            await asyncio.sleep(duration)
    
    async def _clear_display(self):
        """Clear the display"""
        pattern = self._create_empty_pattern()
        await self._display_pattern(pattern)
    
    async def _set_status_led(self, color: str, intensity: float):
        """Set status LED intensity"""
        if color in self.status_leds:
            self.status_leds[color].value = max(0.0, min(1.0, intensity))
    
    async def _set_status_color(self, color: str, intensity: float = 1.0):
        """Set status LED to specific color"""
        # Turn off all LEDs first
        for led_color in ['red', 'green', 'blue']:
            await self._set_status_led(led_color, 0.0)
        
        # Set requested color
        if color == 'red':
            await self._set_status_led('red', intensity)
        elif color == 'green':
            await self._set_status_led('green', intensity)
        elif color == 'blue':
            await self._set_status_led('blue', intensity)
        elif color == 'yellow':
            await self._set_status_led('red', intensity)
            await self._set_status_led('green', intensity)
        elif color == 'purple':
            await self._set_status_led('red', intensity)
            await self._set_status_led('blue', intensity)
        elif color == 'cyan':
            await self._set_status_led('green', intensity)
            await self._set_status_led('blue', intensity)
        elif color == 'white':
            await self._set_status_led('red', intensity)
            await self._set_status_led('green', intensity)
            await self._set_status_led('blue', intensity)
        # 'off' or any other color keeps all LEDs off
    
    def get_status(self) -> dict:
        """Get current display status"""
        return {
            'current_state': self.current_state.value,
            'animation_active': self.animation_active,
            'hardware_enabled': self.hardware_enabled,
            'display_type': self.display_type,
            'brightness': self.brightness
        }
    
    def cleanup(self):
        """Clean up display resources"""
        if self.animation_active:
            asyncio.create_task(self._stop_animation())
        
        # Turn off all LEDs
        if self.hardware_enabled:
            asyncio.create_task(self._set_status_color('off'))
            asyncio.create_task(self._clear_display())
        
        self.logger.info("🧹 Display controller cleanup complete")
