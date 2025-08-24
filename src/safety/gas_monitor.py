"""
🛡️ GAS MONITOR - Jarvis Safety Feature
Gas leak detection and monitoring system for lab safety

Monitors gas levels using MQ sensors and triggers alerts
when dangerous levels are detected.
"""

import asyncio
import logging
import time
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from datetime import datetime

@dataclass
class GasReading:
    """Gas sensor reading data"""
    sensor_type: str
    value: float
    ppm: float
    timestamp: datetime
    is_dangerous: bool
    threshold_exceeded: bool

class GasMonitor:
    """
    🔍 Gas Detection and Monitoring System
    
    Features:
    - MQ-2 (combustible gases, smoke)
    - MQ-5 (natural gas, LPG)
    - MQ-7 (carbon monoxide)
    - Real-time monitoring and alerts
    """
    
    def __init__(self, config, alert_callback: Optional[Callable] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.alert_callback = alert_callback

        # Gas sensor thresholds (PPM)
        self.thresholds: Dict[str, float] = {
            'mq2': 300,  # Smoke/combustible gases
            'mq5': 200,  # Natural gas
            'mq7': 50,   # Carbon monoxide
            'general': 400  # General gas threshold
        }

        # Monitoring state
        self.is_monitoring: bool = False
        self.last_readings: Dict[str, GasReading] = {}
        self.alert_active: bool = False
        self.baseline_values: Dict[str, float] = {}

        # Hardware simulation for development (support both SIMULATION_MODE and simulation_mode)
        self.simulation_mode: bool = getattr(config, 'simulation_mode', getattr(config, 'SIMULATION_MODE', True))

        self.logger.info("Gas Monitor initialized")
    
    async def start_monitoring(self):
        """Start continuous gas monitoring"""
        self.is_monitoring = True
        self.logger.info("Starting gas monitoring system")
        
        # Calibrate sensors on startup
        await self.calibrate_sensors()
        
        # Start monitoring loop
        asyncio.create_task(self._monitoring_loop())
    
    async def stop_monitoring(self):
        """Stop gas monitoring"""
        self.is_monitoring = False
        self.logger.info("Gas monitoring stopped")
    
    async def calibrate_sensors(self):
        """Calibrate gas sensors to baseline values"""
        self.logger.info("Calibrating gas sensors...")
        
        # Take baseline readings
        for sensor in ['mq2', 'mq5', 'mq7']:
            readings = []
            for _ in range(10):
                value = await self._read_sensor(sensor)
                readings.append(value)
                await asyncio.sleep(0.1)
            
            self.baseline_values[sensor] = sum(readings) / len(readings)
            self.logger.info(f"Sensor {sensor} baseline: {self.baseline_values[sensor]:.2f}")
        
        self.logger.info("Gas sensor calibration complete")
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Read all gas sensors
                readings = await self._read_all_sensors()
                
                # Check for dangerous levels
                for sensor, reading in readings.items():
                    self.last_readings[sensor] = reading
                    
                    if reading.is_dangerous:
                        await self._trigger_gas_alert(reading)
                
                # Log readings periodically
                await self._log_readings(readings)
                
                await asyncio.sleep(1.0)  # Monitor every second
                
            except Exception as e:
                self.logger.error(f"Error in gas monitoring loop: {e}")
                await asyncio.sleep(5.0)
    
    async def _read_all_sensors(self) -> Dict[str, GasReading]:
        """Read all gas sensors"""
        readings = {}
        
        for sensor in ['mq2', 'mq5', 'mq7']:
            value = await self._read_sensor(sensor)
            ppm = self._convert_to_ppm(sensor, value)
            
            threshold = self.thresholds.get(sensor, self.thresholds['general'])
            is_dangerous = ppm > threshold
            threshold_exceeded = ppm > (threshold * 0.8)  # Warning at 80%
            
            readings[sensor] = GasReading(
                sensor_type=sensor,
                value=value,
                ppm=ppm,
                timestamp=datetime.now(),
                is_dangerous=is_dangerous,
                threshold_exceeded=threshold_exceeded
            )
        
        return readings
    
    async def _read_sensor(self, sensor: str) -> float:
        """Read individual gas sensor"""
        if self.simulation_mode:
            # Simulate gas sensor readings
            import random
            base_value = 100.0
            noise = random.uniform(-10, 10)
            
            # Occasionally simulate a gas leak for testing
            if random.random() < 0.001:  # 0.1% chance
                leak_value = random.uniform(400, 800)
                self.logger.warning(f"SIMULATION: Gas leak detected on {sensor}")
                return leak_value
            
            return base_value + noise
        else:
            # Read from actual MQ sensor via ADC
            try:
                # This would interface with actual MCP3008 ADC
                # For now, return simulated value
                return 150.0
            except Exception as e:
                self.logger.error(f"Error reading {sensor}: {e}")
                return 0.0
    
    def _convert_to_ppm(self, sensor: str, raw_value: float) -> float:
        """Convert raw sensor value to PPM"""
        # Simplified conversion - would need proper calibration
        # for real deployment with specific MQ sensor curves
        
        baseline = self.baseline_values.get(sensor, 100.0)
        ratio = raw_value / baseline
        
        # Simple linear approximation (real sensors need logarithmic curves)
        if sensor == 'mq2':  # Smoke/combustible
            ppm = (ratio - 1.0) * 200
        elif sensor == 'mq5':  # Natural gas
            ppm = (ratio - 1.0) * 150
        elif sensor == 'mq7':  # Carbon monoxide
            ppm = (ratio - 1.0) * 100
        else:
            ppm = (ratio - 1.0) * 100
        
        return max(0, ppm)  # Ensure positive values
    
    async def _trigger_gas_alert(self, reading: GasReading):
        """Trigger gas leak alert"""
        if not self.alert_active:
            self.alert_active = True
            
            alert_message = (
                f"🚨 GAS LEAK DETECTED! 🚨\n"
                f"Sensor: {reading.sensor_type.upper()}\n"
                f"Level: {reading.ppm:.1f} PPM\n"
                f"Threshold: {self.thresholds.get(reading.sensor_type, 400)} PPM\n"
                f"Time: {reading.timestamp.strftime('%H:%M:%S')}"
            )
            
            self.logger.critical(alert_message)
            
            # Call alert callback if provided
            if self.alert_callback:
                await self.alert_callback({
                    'type': 'gas_leak',
                    'severity': 'critical',
                    'sensor': reading.sensor_type,
                    'ppm': reading.ppm,
                    'message': alert_message,
                    'timestamp': reading.timestamp
                })
            
            # Keep alert active for minimum duration
            await asyncio.sleep(10)
            self.alert_active = False
    
    async def _log_readings(self, readings: Dict[str, GasReading]):
        """Log gas readings to environmental log"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'gas_readings': {}
        }
        
        for sensor, reading in readings.items():
            log_data['gas_readings'][sensor] = {
                'value': reading.value,
                'ppm': reading.ppm,
                'is_dangerous': reading.is_dangerous,
                'threshold_exceeded': reading.threshold_exceeded
            }
        
        # This would write to environmental log file
        # Environmental logger handles the actual file writing
    
    def get_current_readings(self) -> Dict[str, GasReading]:
        """Get current gas sensor readings"""
        return self.last_readings.copy()
    
    def is_safe(self) -> bool:
        """Check if current gas levels are safe"""
        if not self.last_readings:
            return True
        
        return not any(reading.is_dangerous for reading in self.last_readings.values())
    
    def get_status_report(self) -> str:
        """Get human-readable status report"""
        if not self.last_readings:
            return "Gas monitoring system active, no readings yet."
        
        safe_sensors = []
        warning_sensors = []
        danger_sensors = []
        
        for sensor, reading in self.last_readings.items():
            if reading.is_dangerous:
                danger_sensors.append(f"{sensor.upper()}: {reading.ppm:.1f} PPM")
            elif reading.threshold_exceeded:
                warning_sensors.append(f"{sensor.upper()}: {reading.ppm:.1f} PPM")
            else:
                safe_sensors.append(f"{sensor.upper()}: {reading.ppm:.1f} PPM")
        
        if danger_sensors:
            return f"🚨 DANGER: Gas leak detected! {', '.join(danger_sensors)}"
        elif warning_sensors:
            return f"⚠️ WARNING: Elevated gas levels: {', '.join(warning_sensors)}"
        else:
            return f"✅ All gas levels normal: {', '.join(safe_sensors)}"
