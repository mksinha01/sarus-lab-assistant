"""
🌡️ ENVIRONMENTAL SENSOR MANAGER - Jarvis Monitoring Feature
Temperature, humidity, and environmental condition monitoring

Continuously monitors lab environmental conditions for safety
and optimal working conditions.
"""

import asyncio
import logging
import time
import json
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path

@dataclass
class EnvironmentalReading:
    """Environmental sensor reading data"""
    temperature: float  # Celsius
    humidity: float     # Percentage
    pressure: Optional[float] = None  # hPa
    air_quality: Optional[float] = None  # AQI
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class EnvironmentalThresholds:
    """Environmental safety thresholds"""
    temp_min: float = 15.0   # Minimum safe temperature
    temp_max: float = 35.0   # Maximum safe temperature
    temp_warning: float = 30.0  # Warning temperature
    humidity_min: float = 30.0  # Minimum humidity
    humidity_max: float = 70.0  # Maximum humidity
    humidity_warning: float = 65.0  # Warning humidity

class EnvironmentalSensorManager:
    """
    🌡️ Environmental Monitoring System
    
    Features:
    - DHT22 temperature and humidity monitoring
    - Real-time environmental data logging
    - Safety threshold monitoring and alerts
    - Environmental trend analysis
    """
    
    def __init__(self, config, alert_callback: Optional[Callable] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.alert_callback = alert_callback

        # Monitoring configuration
        self.thresholds = EnvironmentalThresholds()
        self.monitoring_interval = 10.0  # seconds
        self.is_monitoring = False

        # Data storage
        self.current_reading: Optional[EnvironmentalReading] = None
        self.readings_history: List[EnvironmentalReading] = []
        self.max_history = 1000  # Keep last 1000 readings

        # Alert state
        self.alert_cooldown = 300  # 5 minutes between same type alerts
        self.last_alerts: Dict[str, float] = {}

        # Hardware simulation
        self.simulation_mode = getattr(config, 'simulation_mode', getattr(config, 'SIMULATION_MODE', True))

        # Data logging
        # Resolve logs dir from config dataclass (LOGS_DIR) or attribute
        logs_dir = getattr(config, 'LOGS_DIR', getattr(config, 'log_dir', Path(__file__).parent.parent.parent.parent / 'logs'))
        self.log_file = Path(logs_dir) / "environmental" / "sensor_data.jsonl"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        self.logger.info("Environmental Sensor Manager initialized")
    
    async def start_monitoring(self):
        """Start environmental monitoring"""
        self.is_monitoring = True
        self.logger.info("Starting environmental monitoring")
        
        # Initialize sensors
        await self._initialize_sensors()
        
        # Start monitoring loop
        asyncio.create_task(self._monitoring_loop())
        
        # Start data logging task
        asyncio.create_task(self._logging_loop())
    
    async def stop_monitoring(self):
        """Stop environmental monitoring"""
        self.is_monitoring = False
        self.logger.info("Environmental monitoring stopped")
    
    async def _initialize_sensors(self):
        """Initialize environmental sensors"""
        if self.simulation_mode:
            self.logger.info("Environmental sensors initialized (simulation mode)")
        else:
            try:
                # Initialize DHT22 sensor
                # This would initialize actual hardware sensors
                self.logger.info("DHT22 sensor initialized")
            except Exception as e:
                self.logger.error(f"Failed to initialize sensors: {e}")
                self.simulation_mode = True
    
    async def _monitoring_loop(self):
        """Main environmental monitoring loop"""
        while self.is_monitoring:
            try:
                # Read sensors
                reading = await self._read_sensors()
                
                if reading:
                    self.current_reading = reading
                    self.readings_history.append(reading)
                    
                    # Maintain history size
                    if len(self.readings_history) > self.max_history:
                        self.readings_history.pop(0)
                    
                    # Check thresholds and trigger alerts
                    await self._check_thresholds(reading)
                
                await asyncio.sleep(self.monitoring_interval)
                
            except Exception as e:
                self.logger.error(f"Error in environmental monitoring loop: {e}")
                await asyncio.sleep(self.monitoring_interval)
    
    async def _read_sensors(self) -> Optional[EnvironmentalReading]:
        """Read all environmental sensors"""
        try:
            if self.simulation_mode:
                return self._simulate_reading()
            else:
                return await self._read_hardware_sensors()
        except Exception as e:
            self.logger.error(f"Error reading sensors: {e}")
            return None
    
    def _simulate_reading(self) -> EnvironmentalReading:
        """Simulate environmental sensor readings"""
        import random
        
        # Base values with some variation
        base_temp = 22.0
        base_humidity = 45.0
        
        # Add realistic variation
        temp_noise = random.uniform(-2.0, 2.0)
        humidity_noise = random.uniform(-5.0, 5.0)
        
        # Occasionally simulate extreme conditions for testing
        if random.random() < 0.01:  # 1% chance
            if random.random() < 0.5:
                base_temp += random.uniform(10, 15)  # Hot condition
                self.logger.warning("SIMULATION: High temperature condition")
            else:
                base_humidity += random.uniform(20, 30)  # High humidity
                self.logger.warning("SIMULATION: High humidity condition")
        
        temperature = base_temp + temp_noise
        humidity = max(0, min(100, base_humidity + humidity_noise))
        
        return EnvironmentalReading(
            temperature=temperature,
            humidity=humidity,
            pressure=1013.25 + random.uniform(-5, 5),  # Standard pressure ± 5 hPa
            air_quality=random.uniform(50, 150)  # AQI simulation
        )
    
    async def _read_hardware_sensors(self) -> Optional[EnvironmentalReading]:
        """Read actual hardware sensors"""
        try:
            # Read DHT22 sensor
            # This would interface with actual Adafruit CircuitPython DHT22
            
            # For now, return simulated values
            # In real implementation:
            # import adafruit_dht
            # dht = adafruit_dht.DHT22(board.D4)
            # temperature = dht.temperature
            # humidity = dht.humidity
            
            temperature = 22.5
            humidity = 45.0
            
            return EnvironmentalReading(
                temperature=temperature,
                humidity=humidity
            )
            
        except Exception as e:
            self.logger.error(f"Hardware sensor read error: {e}")
            return None
    
    async def _check_thresholds(self, reading: EnvironmentalReading):
        """Check environmental thresholds and trigger alerts"""
        current_time = time.time()
        
        # Temperature checks
        if reading.temperature > self.thresholds.temp_max:
            await self._trigger_alert(
                "temperature_critical",
                f"Critical temperature: {reading.temperature:.1f}°C (max: {self.thresholds.temp_max}°C)",
                "critical",
                reading,
                current_time
            )
        elif reading.temperature > self.thresholds.temp_warning:
            await self._trigger_alert(
                "temperature_warning",
                f"High temperature warning: {reading.temperature:.1f}°C",
                "warning",
                reading,
                current_time
            )
        elif reading.temperature < self.thresholds.temp_min:
            await self._trigger_alert(
                "temperature_low",
                f"Low temperature: {reading.temperature:.1f}°C (min: {self.thresholds.temp_min}°C)",
                "warning",
                reading,
                current_time
            )
        
        # Humidity checks
        if reading.humidity > self.thresholds.humidity_max:
            await self._trigger_alert(
                "humidity_critical",
                f"Critical humidity: {reading.humidity:.1f}% (max: {self.thresholds.humidity_max}%)",
                "critical",
                reading,
                current_time
            )
        elif reading.humidity > self.thresholds.humidity_warning:
            await self._trigger_alert(
                "humidity_warning",
                f"High humidity warning: {reading.humidity:.1f}%",
                "warning",
                reading,
                current_time
            )
        elif reading.humidity < self.thresholds.humidity_min:
            await self._trigger_alert(
                "humidity_low",
                f"Low humidity: {reading.humidity:.1f}% (min: {self.thresholds.humidity_min}%)",
                "warning",
                reading,
                current_time
            )
    
    async def _trigger_alert(self, alert_type: str, message: str, severity: str, 
                           reading: EnvironmentalReading, current_time: float):
        """Trigger environmental alert with cooldown"""
        # Check cooldown
        if alert_type in self.last_alerts:
            if current_time - self.last_alerts[alert_type] < self.alert_cooldown:
                return  # Still in cooldown
        
        self.last_alerts[alert_type] = current_time
        
        # Log alert
        if severity == "critical":
            self.logger.critical(message)
        else:
            self.logger.warning(message)
        
        # Call alert callback
        if self.alert_callback:
            await self.alert_callback({
                'type': 'environmental_alert',
                'alert_type': alert_type,
                'severity': severity,
                'message': message,
                'reading': asdict(reading),
                'timestamp': reading.timestamp
            })
    
    async def _logging_loop(self):
        """Data logging loop"""
        while self.is_monitoring:
            try:
                if self.current_reading:
                    await self._log_reading(self.current_reading)
                
                await asyncio.sleep(60)  # Log every minute
                
            except Exception as e:
                self.logger.error(f"Error in logging loop: {e}")
                await asyncio.sleep(60)
    
    async def _log_reading(self, reading: EnvironmentalReading):
        """Log environmental reading to file"""
        try:
            ts = reading.timestamp or datetime.now()
            log_entry = {
                'timestamp': ts.isoformat(),
                'temperature': reading.temperature,
                'humidity': reading.humidity,
                'pressure': reading.pressure,
                'air_quality': reading.air_quality
            }
            
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            self.logger.error(f"Error logging reading: {e}")
    
    def get_current_reading(self) -> Optional[EnvironmentalReading]:
        """Get current environmental reading"""
        return self.current_reading
    
    def get_recent_readings(self, hours: int = 24) -> List[EnvironmentalReading]:
        """Get recent environmental readings"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        result: List[EnvironmentalReading] = []
        for r in self.readings_history:
            ts = r.timestamp or datetime.now()
            if ts >= cutoff_time:
                result.append(r)
        return result
    
    def get_average_conditions(self, hours: int = 1) -> Optional[Dict[str, float]]:
        """Get average environmental conditions over time period"""
        recent_readings = self.get_recent_readings(hours)
        
        if not recent_readings:
            return None
        
        total_temp = sum(r.temperature for r in recent_readings)
        total_humidity = sum(r.humidity for r in recent_readings)
        count = len(recent_readings)
        
        return {
            'temperature': total_temp / count,
            'humidity': total_humidity / count,
            'count': count
        }
    
    def is_environment_safe(self) -> bool:
        """Check if current environment is within safe parameters"""
        if not self.current_reading:
            return False
        
        reading = self.current_reading
        
        temp_safe = (self.thresholds.temp_min <= reading.temperature <= self.thresholds.temp_max)
        humidity_safe = (self.thresholds.humidity_min <= reading.humidity <= self.thresholds.humidity_max)
        
        return temp_safe and humidity_safe
    
    def get_status_report(self) -> str:
        """Get human-readable environmental status report"""
        if not self.current_reading:
            return "Environmental monitoring active, no readings yet."
        
    reading = self.current_reading
    ts = reading.timestamp or datetime.now()
    time_ago = (datetime.now() - ts).total_seconds()
        
        # Safety status
        if self.is_environment_safe():
            safety_status = "✅ SAFE"
        else:
            safety_status = "⚠️ WARNING"
        
        return (
            f"{safety_status} - Temp: {reading.temperature:.1f}°C, "
            f"Humidity: {reading.humidity:.1f}% "
            f"(Updated {time_ago:.0f}s ago)"
        )
    
    def set_thresholds(self, **kwargs):
        """Update environmental thresholds"""
        for key, value in kwargs.items():
            if hasattr(self.thresholds, key):
                setattr(self.thresholds, key, value)
                self.logger.info(f"Updated threshold {key} to {value}")
    
    def get_thresholds(self) -> EnvironmentalThresholds:
        """Get current environmental thresholds"""
        return self.thresholds
