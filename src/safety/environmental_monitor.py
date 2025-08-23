"""
Environmental Monitoring System for Sarus Robot

Monitors temperature, humidity, air quality and other environmental
parameters for safety and operational awareness. This implements
core Jarvis environmental monitoring capabilities.
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

# Sensor libraries for Raspberry Pi
try:
    import adafruit_dht
    import board
    DHT_AVAILABLE = True
except ImportError:
    DHT_AVAILABLE = False

try:
    import busio
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn
    ADS_AVAILABLE = True
except ImportError:
    ADS_AVAILABLE = False

from ..config.settings import Config
from ..utils.logger import get_logger

class AlertLevel(Enum):
    """Environmental alert levels"""
    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

@dataclass
class EnvironmentalReading:
    """Single environmental measurement"""
    timestamp: float
    temperature_c: Optional[float] = None
    humidity_percent: Optional[float] = None
    air_quality_index: Optional[int] = None
    atmospheric_pressure: Optional[float] = None
    light_level: Optional[float] = None
    noise_level: Optional[float] = None
    
class EnvironmentalMonitor:
    """
    Monitors environmental conditions for safety and optimization
    
    Key Features:
    - Temperature and humidity monitoring (DHT22)
    - Air quality assessment
    - Environmental alerts and thresholds
    - Historical data logging
    - Safety protocol integration
    """
    
    def __init__(self, config: Config):
        self.logger = get_logger(__name__)
        self.config = config
        
        # Hardware components
        self.dht_sensor = None
        self.ads_converter = None
        
        # Monitoring state
        self.is_monitoring = False
        self.current_readings = None
        self.alert_level = AlertLevel.NORMAL
        
        # Data storage
        self.readings_history: List[EnvironmentalReading] = []
        self.max_history = 1000  # Keep last 1000 readings
        
        # Alert thresholds
        self.temp_warning = 35.0  # °C
        self.temp_critical = 40.0  # °C
        self.humidity_warning = 80.0  # %
        self.humidity_critical = 90.0  # %
        
        # Monitoring intervals
        self.monitor_interval = 30.0  # seconds
        self.alert_check_interval = 5.0  # seconds
        
    async def initialize(self):
        """Initialize environmental monitoring hardware"""
        self.logger.info("🌡️ Initializing environmental monitoring...")
        
        try:
            # Initialize DHT22 temperature/humidity sensor
            if DHT_AVAILABLE and self.config.hardware_enabled:
                self._initialize_dht_sensor()
            
            # Initialize ADC for analog sensors
            if ADS_AVAILABLE and self.config.hardware_enabled:
                self._initialize_adc()
            
            self.logger.info("✅ Environmental monitoring initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize environmental monitoring: {e}")
            raise
    
    def _initialize_dht_sensor(self):
        """Initialize DHT22 temperature and humidity sensor"""
        try:
            pin = getattr(board, f"D{self.config.gpio_pins.get('dht22_pin', 4)}")
            self.dht_sensor = adafruit_dht.DHT22(pin)
            self.logger.info("✅ DHT22 sensor initialized")
        except Exception as e:
            self.logger.warning(f"Could not initialize DHT22: {e}")
            self.dht_sensor = None
    
    def _initialize_adc(self):
        """Initialize ADC for analog environmental sensors"""
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.ads_converter = ADS.ADS1115(i2c)
            self.logger.info("✅ ADS1115 ADC initialized")
        except Exception as e:
            self.logger.warning(f"Could not initialize ADC: {e}")
            self.ads_converter = None
    
    async def start_monitoring(self):
        """Start continuous environmental monitoring"""
        if self.is_monitoring:
            self.logger.warning("Environmental monitoring already running")
            return
        
        self.is_monitoring = True
        self.logger.info("🔄 Starting environmental monitoring loop")
        
        # Start monitoring tasks
        monitor_task = asyncio.create_task(self._monitoring_loop())
        alert_task = asyncio.create_task(self._alert_checking_loop())
        
        await asyncio.gather(monitor_task, alert_task)
    
    async def stop_monitoring(self):
        """Stop environmental monitoring"""
        self.is_monitoring = False
        self.logger.info("⏹️ Stopping environmental monitoring")
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                reading = await self._take_reading()
                if reading:
                    self.current_readings = reading
                    self._store_reading(reading)
                    self._log_reading(reading)
                
                await asyncio.sleep(self.monitor_interval)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)  # Brief pause before retry
    
    async def _alert_checking_loop(self):
        """Check for environmental alerts"""
        while self.is_monitoring:
            try:
                if self.current_readings:
                    new_alert_level = self._assess_alert_level(self.current_readings)
                    
                    if new_alert_level != self.alert_level:
                        await self._handle_alert_change(self.alert_level, new_alert_level)
                        self.alert_level = new_alert_level
                
                await asyncio.sleep(self.alert_check_interval)
                
            except Exception as e:
                self.logger.error(f"Error in alert checking: {e}")
                await asyncio.sleep(2)
    
    async def _take_reading(self) -> Optional[EnvironmentalReading]:
        """Take a complete environmental reading"""
        reading = EnvironmentalReading(timestamp=time.time())
        
        # Read temperature and humidity
        if self.dht_sensor:
            try:
                reading.temperature_c = self.dht_sensor.temperature
                reading.humidity_percent = self.dht_sensor.humidity
            except RuntimeError as e:
                # DHT sensors can be finicky
                self.logger.debug(f"DHT reading error: {e}")
        
        # Read analog sensors via ADC
        if self.ads_converter:
            try:
                # Air quality sensor (MQ-135 or similar)
                chan0 = AnalogIn(self.ads_converter, ADS.P0)
                reading.air_quality_index = int(chan0.value / 655.35)  # Convert to 0-100 scale
                
                # Light sensor
                chan1 = AnalogIn(self.ads_converter, ADS.P1)
                reading.light_level = chan1.voltage
                
            except Exception as e:
                self.logger.debug(f"ADC reading error: {e}")
        
        return reading if any([
            reading.temperature_c is not None,
            reading.humidity_percent is not None,
            reading.air_quality_index is not None
        ]) else None
    
    def _store_reading(self, reading: EnvironmentalReading):
        """Store reading in history"""
        self.readings_history.append(reading)
        
        # Trim history if too long
        if len(self.readings_history) > self.max_history:
            self.readings_history = self.readings_history[-self.max_history:]
    
    def _log_reading(self, reading: EnvironmentalReading):
        """Log reading to environmental log"""
        log_data = {
            'timestamp': reading.timestamp,
            'temperature_c': reading.temperature_c,
            'humidity_percent': reading.humidity_percent,
            'air_quality_index': reading.air_quality_index,
            'light_level': reading.light_level
        }
        
        # Use environmental logger
        env_logger = logging.getLogger('environmental')
        env_logger.info(f"ENV_READING: {log_data}")
    
    def _assess_alert_level(self, reading: EnvironmentalReading) -> AlertLevel:
        """Assess current environmental alert level"""
        if reading.temperature_c is not None:
            if reading.temperature_c >= self.temp_critical:
                return AlertLevel.EMERGENCY
            elif reading.temperature_c >= self.temp_warning:
                return AlertLevel.CRITICAL
        
        if reading.humidity_percent is not None:
            if reading.humidity_percent >= self.humidity_critical:
                return AlertLevel.CRITICAL
            elif reading.humidity_percent >= self.humidity_warning:
                return AlertLevel.WARNING
        
        if reading.air_quality_index is not None:
            if reading.air_quality_index >= 80:
                return AlertLevel.CRITICAL
            elif reading.air_quality_index >= 60:
                return AlertLevel.WARNING
        
        return AlertLevel.NORMAL
    
    async def _handle_alert_change(self, old_level: AlertLevel, new_level: AlertLevel):
        """Handle environmental alert level changes"""
        self.logger.warning(f"🚨 Environmental alert level changed: {old_level.value} → {new_level.value}")
        
        if new_level == AlertLevel.EMERGENCY:
            await self._handle_emergency_alert()
        elif new_level == AlertLevel.CRITICAL:
            await self._handle_critical_alert()
        elif new_level == AlertLevel.WARNING:
            await self._handle_warning_alert()
    
    async def _handle_emergency_alert(self):
        """Handle emergency environmental conditions"""
        self.logger.error("🚨 ENVIRONMENTAL EMERGENCY - Initiating safety protocols")
        
        # Log emergency
        emergency_logger = logging.getLogger('security')
        emergency_logger.critical(f"ENVIRONMENTAL_EMERGENCY: {self.current_readings}")
        
        # Could trigger robot shutdown, alert systems, etc.
        # This would integrate with the main safety manager
    
    async def _handle_critical_alert(self):
        """Handle critical environmental conditions"""
        self.logger.warning("⚠️ Critical environmental conditions detected")
        
        # Log critical condition
        security_logger = logging.getLogger('security')
        security_logger.warning(f"ENVIRONMENTAL_CRITICAL: {self.current_readings}")
    
    async def _handle_warning_alert(self):
        """Handle warning environmental conditions"""
        self.logger.info("⚡ Environmental warning conditions")
    
    def get_current_conditions(self) -> Dict[str, Any]:
        """Get current environmental conditions"""
        if not self.current_readings:
            return {"status": "no_data", "alert_level": self.alert_level.value}
        
        return {
            "timestamp": self.current_readings.timestamp,
            "temperature_c": self.current_readings.temperature_c,
            "humidity_percent": self.current_readings.humidity_percent,
            "air_quality_index": self.current_readings.air_quality_index,
            "light_level": self.current_readings.light_level,
            "alert_level": self.alert_level.value,
            "status": "active" if self.is_monitoring else "inactive"
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get environmental statistics"""
        if not self.readings_history:
            return {"status": "no_data"}
        
        temps = [r.temperature_c for r in self.readings_history if r.temperature_c is not None]
        humidity = [r.humidity_percent for r in self.readings_history if r.humidity_percent is not None]
        
        stats = {
            "total_readings": len(self.readings_history),
            "monitoring_duration_hours": (time.time() - self.readings_history[0].timestamp) / 3600,
        }
        
        if temps:
            stats.update({
                "temperature_min": min(temps),
                "temperature_max": max(temps),
                "temperature_avg": sum(temps) / len(temps)
            })
        
        if humidity:
            stats.update({
                "humidity_min": min(humidity),
                "humidity_max": max(humidity),
                "humidity_avg": sum(humidity) / len(humidity)
            })
        
        return stats
