"""
Sensor manager for Sarus robot

Manages ultrasonic sensors, environmental sensors, and other input devices
for obstacle detection, navigation, and environmental monitoring.
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# GPIO libraries
try:
    import RPi.GPIO as GPIO
    RPI_GPIO_AVAILABLE = True
except ImportError:
    RPI_GPIO_AVAILABLE = False

try:
    from gpiozero import DistanceSensor, MCP3008
    GPIOZERO_AVAILABLE = True
except ImportError:
    GPIOZERO_AVAILABLE = False

import random  # For simulation

from ..config.settings import SYSTEM_CONFIG
from ..utils.logger import get_logger

class SensorType(Enum):
    """Types of sensors"""
    ULTRASONIC = "ultrasonic"
    INFRARED = "infrared"
    BUMPER = "bumper"
    GYROSCOPE = "gyroscope"
    ACCELEROMETER = "accelerometer"
    TEMPERATURE = "temperature"
    BATTERY = "battery"

@dataclass
class SensorReading:
    """Data structure for sensor readings"""
    sensor_id: str
    sensor_type: SensorType
    value: float
    unit: str
    timestamp: float
    valid: bool = True

class SensorManager:
    """
    Manages all robot sensors for navigation and environmental monitoring
    """
    
    def __init__(self):
        self.logger = get_logger(__name__)
        
        # Configuration
        self.hardware_enabled = SYSTEM_CONFIG.get('hardware_enabled', False)
        self.gpio_pins = SYSTEM_CONFIG.get('gpio_pins', {})
        self.obstacle_threshold = SYSTEM_CONFIG.get('obstacle_distance_threshold', 30)
        self.emergency_threshold = SYSTEM_CONFIG.get('emergency_stop_distance', 10)
        
        # Ultrasonic sensors
        self.ultrasonic_sensors = {}
        self.sensor_positions = {
            'front': 'ultrasonic_front',
            'left': 'ultrasonic_left',
            'right': 'ultrasonic_right'
        }
        
        # Environmental sensors
        self.battery_monitor = None
        self.temperature_sensor = None
        
        # Sensor data
        self.latest_readings: Dict[str, SensorReading] = {}
        self.reading_history: Dict[str, List[SensorReading]] = {}
        self.max_history_length = 100
        
        # Monitoring
        self.monitoring_active = False
        self.monitoring_task = None
        self.update_rate = SYSTEM_CONFIG.get('navigation_update_rate', 10)  # Hz
        
    async def initialize(self):
        """Initialize sensor systems"""
        self.logger.info("📡 Initializing sensor systems...")
        
        if not self.hardware_enabled:
            self.logger.info("Hardware disabled - sensors in simulation mode")
            return
        
        try:
            await self._setup_ultrasonic_sensors()
            await self._setup_environmental_sensors()
            await self._test_sensors()
            
            self.logger.info("✅ Sensor systems initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize sensors: {e}")
            self.hardware_enabled = False  # Fallback to simulation
    
    async def _setup_ultrasonic_sensors(self):
        """Setup ultrasonic distance sensors"""
        if not GPIOZERO_AVAILABLE:
            self.logger.warning("gpiozero not available - ultrasonic sensors disabled")
            return
        
        for position, sensor_key in self.sensor_positions.items():
            trigger_pin = self.gpio_pins.get(f'{sensor_key}_trigger')
            echo_pin = self.gpio_pins.get(f'{sensor_key}_echo')
            
            if trigger_pin and echo_pin:
                try:
                    sensor = DistanceSensor(
                        echo=echo_pin,
                        trigger=trigger_pin,
                        max_distance=4.0  # 4 meters maximum range
                    )
                    
                    self.ultrasonic_sensors[position] = sensor
                    self.logger.info(f"✅ Ultrasonic sensor '{position}' initialized (pins {trigger_pin}, {echo_pin})")
                    
                except Exception as e:
                    self.logger.error(f"Failed to initialize ultrasonic sensor '{position}': {e}")
            else:
                self.logger.warning(f"Missing pins for ultrasonic sensor '{position}'")
    
    async def _setup_environmental_sensors(self):
        """Setup environmental monitoring sensors"""
        # Battery monitoring would typically use ADC
        # Temperature sensor setup would go here
        # For now, these are simulated
        self.logger.info("Environmental sensors setup (simulated)")
    
    async def _test_sensors(self):
        """Test sensor functionality"""
        self.logger.info("🧪 Testing sensors...")
        
        # Test ultrasonic sensors
        for position, sensor in self.ultrasonic_sensors.items():
            try:
                distance = sensor.distance * 100  # Convert to cm
                self.logger.info(f"Ultrasonic {position}: {distance:.1f} cm")
            except Exception as e:
                self.logger.warning(f"Ultrasonic sensor {position} test failed: {e}")
        
        self.logger.info("✅ Sensor tests completed")
    
    async def start_monitoring(self):
        """Start continuous sensor monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
        
        self.logger.info("📊 Sensor monitoring started")
    
    async def stop_monitoring(self):
        """Stop sensor monitoring"""
        self.monitoring_active = False
        
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        
        self.logger.info("📊 Sensor monitoring stopped")
    
    async def _monitoring_loop(self):
        """Continuous sensor monitoring loop"""
        interval = 1.0 / self.update_rate
        
        while self.monitoring_active:
            try:
                # Read all sensors
                await self._read_all_sensors()
                
                # Check for emergency conditions
                await self._check_emergency_conditions()
                
                await asyncio.sleep(interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in sensor monitoring: {e}")
                await asyncio.sleep(1.0)  # Longer delay on error
    
    async def _read_all_sensors(self):
        """Read all available sensors"""
        current_time = time.time()
        
        # Read ultrasonic sensors
        for position, sensor in self.ultrasonic_sensors.items():
            try:
                distance_m = sensor.distance
                distance_cm = distance_m * 100
                
                reading = SensorReading(
                    sensor_id=f"ultrasonic_{position}",
                    sensor_type=SensorType.ULTRASONIC,
                    value=distance_cm,
                    unit="cm",
                    timestamp=current_time,
                    valid=distance_m < 4.0  # Valid if within max range
                )
                
                self._store_reading(reading)
                
            except Exception as e:
                self.logger.error(f"Error reading ultrasonic sensor {position}: {e}")
        
        # Read environmental sensors (simulated for now)
        if not self.hardware_enabled:
            await self._simulate_sensor_readings(current_time)
    
    async def _simulate_sensor_readings(self, timestamp: float):
        """Simulate sensor readings for development"""
        # Simulate ultrasonic sensors
        for position in ['front', 'left', 'right']:
            # Simulate random distances with some realistic patterns
            base_distance = 100 + random.uniform(-20, 20)  # cm
            if position == 'front':
                base_distance = 150 + random.uniform(-50, 50)  # Front typically sees further
            
            reading = SensorReading(
                sensor_id=f"ultrasonic_{position}",
                sensor_type=SensorType.ULTRASONIC,
                value=max(5, base_distance),  # Minimum 5cm
                unit="cm",
                timestamp=timestamp,
                valid=True
            )
            
            self._store_reading(reading)
        
        # Simulate battery level
        battery_level = 85 + random.uniform(-5, 5)  # Simulate ~85% battery
        battery_reading = SensorReading(
            sensor_id="battery_main",
            sensor_type=SensorType.BATTERY,
            value=max(0, min(100, battery_level)),
            unit="%",
            timestamp=timestamp,
            valid=True
        )
        
        self._store_reading(battery_reading)
        
        # Simulate temperature
        temperature = 25 + random.uniform(-3, 7)  # Room temperature variation
        temp_reading = SensorReading(
            sensor_id="temperature_cpu",
            sensor_type=SensorType.TEMPERATURE,
            value=temperature,
            unit="°C",
            timestamp=timestamp,
            valid=True
        )
        
        self._store_reading(temp_reading)
    
    def _store_reading(self, reading: SensorReading):
        """Store sensor reading in history and update latest"""
        sensor_id = reading.sensor_id
        
        # Update latest reading
        self.latest_readings[sensor_id] = reading
        
        # Add to history
        if sensor_id not in self.reading_history:
            self.reading_history[sensor_id] = []
        
        self.reading_history[sensor_id].append(reading)
        
        # Limit history length
        if len(self.reading_history[sensor_id]) > self.max_history_length:
            self.reading_history[sensor_id] = self.reading_history[sensor_id][-self.max_history_length:]
    
    async def _check_emergency_conditions(self):
        """Check for emergency conditions requiring immediate action"""
        # Check ultrasonic sensors for very close obstacles
        for position in ['front', 'left', 'right']:
            sensor_id = f"ultrasonic_{position}"
            reading = self.latest_readings.get(sensor_id)
            
            if reading and reading.valid and reading.value < self.emergency_threshold:
                self.logger.warning(
                    f"🚨 Emergency obstacle detected: {position} sensor shows {reading.value:.1f}cm"
                )
                # Emergency stop would be triggered by navigation manager
        
        # Check battery level
        battery_reading = self.latest_readings.get("battery_main")
        if battery_reading and battery_reading.valid:
            battery_threshold = SYSTEM_CONFIG.get('battery_low_threshold', 20)
            if battery_reading.value < battery_threshold:
                self.logger.warning(f"🔋 Low battery warning: {battery_reading.value:.1f}%")
        
        # Check temperature
        temp_reading = self.latest_readings.get("temperature_cpu")
        if temp_reading and temp_reading.valid:
            temp_threshold = SYSTEM_CONFIG.get('temperature_warning_threshold', 70)
            if temp_reading.value > temp_threshold:
                self.logger.warning(f"🌡️ High temperature warning: {temp_reading.value:.1f}°C")
    
    def get_distance_reading(self, position: str) -> Optional[float]:
        """
        Get latest distance reading from ultrasonic sensor
        
        Args:
            position: Sensor position ('front', 'left', 'right')
        
        Returns:
            Distance in centimeters or None if not available
        """
        sensor_id = f"ultrasonic_{position}"
        reading = self.latest_readings.get(sensor_id)
        
        if reading and reading.valid:
            return reading.value
        
        return None
    
    def get_obstacle_map(self) -> Dict[str, float]:
        """
        Get current obstacle distances in all directions
        
        Returns:
            Dictionary mapping direction to distance in cm
        """
        obstacle_map = {}
        
        for position in ['front', 'left', 'right']:
            distance = self.get_distance_reading(position)
            if distance is not None:
                obstacle_map[position] = distance
        
        return obstacle_map
    
    def is_path_clear(self, direction: str = 'front', min_distance: Optional[float] = None) -> bool:
        """
        Check if path is clear in specified direction
        
        Args:
            direction: Direction to check ('front', 'left', 'right')
            min_distance: Minimum clear distance required (uses obstacle_threshold if None)
        
        Returns:
            True if path is clear, False otherwise
        """
        if min_distance is None:
            min_distance = self.obstacle_threshold
        
        distance = self.get_distance_reading(direction)
        
        if distance is None:
            return False  # Assume blocked if sensor unavailable
        
        return distance >= min_distance
    
    def get_battery_level(self) -> Optional[float]:
        """Get current battery level percentage"""
        battery_reading = self.latest_readings.get("battery_main")
        
        if battery_reading and battery_reading.valid:
            return battery_reading.value
        
        return None
    
    def get_temperature(self) -> Optional[float]:
        """Get current temperature in Celsius"""
        temp_reading = self.latest_readings.get("temperature_cpu")
        
        if temp_reading and temp_reading.valid:
            return temp_reading.value
        
        return None
    
    def get_sensor_status(self) -> Dict[str, Dict]:
        """Get status of all sensors"""
        status = {
            'monitoring_active': self.monitoring_active,
            'hardware_enabled': self.hardware_enabled,
            'sensors': {}
        }
        
        for sensor_id, reading in self.latest_readings.items():
            status['sensors'][sensor_id] = {
                'type': reading.sensor_type.value,
                'value': reading.value,
                'unit': reading.unit,
                'valid': reading.valid,
                'age_seconds': time.time() - reading.timestamp
            }
        
        return status
    
    def get_navigation_data(self) -> Dict[str, any]:
        """Get sensor data relevant for navigation"""
        return {
            'obstacles': self.get_obstacle_map(),
            'paths_clear': {
                'front': self.is_path_clear('front'),
                'left': self.is_path_clear('left'),
                'right': self.is_path_clear('right')
            },
            'emergency_distances': {
                pos: dist < self.emergency_threshold 
                for pos, dist in self.get_obstacle_map().items()
            },
            'battery_level': self.get_battery_level(),
            'temperature': self.get_temperature(),
            'timestamp': time.time()
        }
    
    def cleanup(self):
        """Clean up sensor resources"""
        if self.monitoring_active:
            asyncio.create_task(self.stop_monitoring())
        
        # Cleanup GPIO if using RPi.GPIO
        if RPI_GPIO_AVAILABLE and self.hardware_enabled:
            try:
                GPIO.cleanup()
            except:
                pass
        
        self.logger.info("🧹 Sensor manager cleanup complete")
