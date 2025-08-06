"""
State manager for Sarus robot

Manages robot state, current commands, and system status
for coordination between different subsystems.
"""

import time
import threading
from typing import Dict, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, asdict

from ..config.settings import SYSTEM_CONFIG
from ..utils.logger import get_logger

class SystemState(Enum):
    """Overall system states"""
    INITIALIZING = "initializing"
    IDLE = "idle"
    ACTIVE = "active"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    SHUTDOWN = "shutdown"

@dataclass
class RobotStatus:
    """Current robot status information"""
    system_state: SystemState
    battery_level: Optional[float] = None
    temperature: Optional[float] = None
    location: str = "unknown"
    uptime: float = 0.0
    last_command: Optional[str] = None
    last_response: Optional[str] = None
    current_action: Optional[str] = None
    is_moving: bool = False
    obstacles_detected: bool = False
    timestamp: float = 0.0

class StateManager:
    """
    Manages robot state and provides thread-safe access to current status
    """
    
    def __init__(self):
        self.logger = get_logger(__name__)
        
        # Thread safety
        self._lock = threading.RLock()
        
        # System information
        self.start_time = time.time()
        self.robot_name = SYSTEM_CONFIG.get('robot_name', 'Sarus')
        
        # Current state
        self._status = RobotStatus(
            system_state=SystemState.INITIALIZING,
            timestamp=time.time()
        )
        
        # Command/response tracking
        self._current_command: Optional[str] = None
        self._current_response: Optional[str] = None
        self._current_action: Optional[Dict[str, Any]] = None
        
        # Mission tracking
        self._current_mission_id: Optional[str] = None
        self._mission_data: Dict[str, Any] = {}
        
        # Performance metrics
        self._command_count = 0
        self._error_count = 0
        self._last_activity_time = time.time()
        
    def set_system_state(self, state: SystemState):
        """Update system state"""
        with self._lock:
            old_state = self._status.system_state
            self._status.system_state = state
            self._status.timestamp = time.time()
            
            if old_state != state:
                self.logger.info(f"🔄 System state changed: {old_state.value} → {state.value}")
    
    def get_system_state(self) -> SystemState:
        """Get current system state"""
        with self._lock:
            return self._status.system_state
    
    def set_current_command(self, command: str):
        """Set current command being processed"""
        with self._lock:
            self._current_command = command
            self._status.last_command = command
            self._command_count += 1
            self._last_activity_time = time.time()
            
            self.logger.debug(f"📝 Current command set: {command}")
    
    def get_current_command(self) -> Optional[str]:
        """Get current command"""
        with self._lock:
            return self._current_command
    
    def clear_current_command(self):
        """Clear current command"""
        with self._lock:
            self._current_command = None
    
    def set_current_response(self, response: str):
        """Set current response being generated"""
        with self._lock:
            self._current_response = response
            self._status.last_response = response
            
            self.logger.debug(f"💬 Current response set: {response}")
    
    def get_current_response(self) -> Optional[str]:
        """Get current response"""
        with self._lock:
            return self._current_response
    
    def clear_current_response(self):
        """Clear current response"""
        with self._lock:
            self._current_response = None
    
    def set_current_action(self, action: Dict[str, Any]):
        """Set current action being executed"""
        with self._lock:
            self._current_action = action
            action_type = action.get('type', 'unknown')
            self._status.current_action = action_type
            
            self.logger.debug(f"🎯 Current action set: {action_type}")
    
    def get_current_action(self) -> Optional[Dict[str, Any]]:
        """Get current action"""
        with self._lock:
            return self._current_action
    
    def clear_current_action(self):
        """Clear current action"""
        with self._lock:
            self._current_action = None
            self._status.current_action = None
    
    def update_sensor_data(self, sensor_data: Dict[str, Any]):
        """Update robot status with sensor data"""
        with self._lock:
            # Update battery level
            if 'battery_level' in sensor_data:
                self._status.battery_level = sensor_data['battery_level']
            
            # Update temperature
            if 'temperature' in sensor_data:
                self._status.temperature = sensor_data['temperature']
            
            # Update movement status
            if 'is_moving' in sensor_data:
                self._status.is_moving = sensor_data['is_moving']
            
            # Update obstacle detection
            if 'obstacles_detected' in sensor_data:
                self._status.obstacles_detected = sensor_data['obstacles_detected']
            
            self._status.timestamp = time.time()
    
    def update_location(self, location: str):
        """Update robot location"""
        with self._lock:
            self._status.location = location
            self._status.timestamp = time.time()
            
            self.logger.debug(f"📍 Location updated: {location}")
    
    def set_mission(self, mission_id: str, mission_data: Dict[str, Any]):
        """Set current mission"""
        with self._lock:
            self._current_mission_id = mission_id
            self._mission_data = mission_data.copy()
            
            self.logger.info(f"🗺️ Mission set: {mission_id}")
    
    def get_current_mission(self) -> Optional[Tuple[str, Dict[str, Any]]]:
        """Get current mission ID and data"""
        with self._lock:
            if self._current_mission_id:
                return self._current_mission_id, self._mission_data.copy()
            return None
    
    def clear_mission(self):
        """Clear current mission"""
        with self._lock:
            self._current_mission_id = None
            self._mission_data.clear()
    
    def increment_error_count(self):
        """Increment error counter"""
        with self._lock:
            self._error_count += 1
    
    def get_status(self) -> RobotStatus:
        """Get complete robot status"""
        with self._lock:
            # Update uptime
            self._status.uptime = time.time() - self.start_time
            self._status.timestamp = time.time()
            
            return RobotStatus(**asdict(self._status))
    
    def get_status_dict(self) -> Dict[str, Any]:
        """Get status as dictionary"""
        status = self.get_status()
        status_dict = asdict(status)
        
        # Add additional metrics
        with self._lock:
            status_dict.update({
                'robot_name': self.robot_name,
                'command_count': self._command_count,
                'error_count': self._error_count,
                'last_activity_time': self._last_activity_time,
                'current_mission_id': self._current_mission_id,
                'idle_time': time.time() - self._last_activity_time
            })
        
        return status_dict
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance and activity metrics"""
        with self._lock:
            uptime = time.time() - self.start_time
            
            return {
                'uptime_seconds': uptime,
                'uptime_hours': uptime / 3600,
                'commands_processed': self._command_count,
                'errors_encountered': self._error_count,
                'error_rate': self._error_count / max(1, self._command_count),
                'commands_per_hour': self._command_count / max(0.001, uptime / 3600),
                'last_activity_seconds_ago': time.time() - self._last_activity_time,
                'current_state': self._status.system_state.value
            }
    
    def is_busy(self) -> bool:
        """Check if robot is currently busy with a task"""
        with self._lock:
            return (self._current_command is not None or 
                   self._current_action is not None or
                   self._status.is_moving)
    
    def is_ready_for_command(self) -> bool:
        """Check if robot is ready to accept new commands"""
        with self._lock:
            return (self._status.system_state in [SystemState.IDLE, SystemState.ACTIVE] and
                   not self.is_busy() and
                   not self._status.obstacles_detected)
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get system health indicators"""
        with self._lock:
            health = {
                'overall_status': 'healthy',
                'warnings': [],
                'errors': []
            }
            
            # Check battery level
            if self._status.battery_level is not None:
                if self._status.battery_level < 20:
                    health['warnings'].append(f"Low battery: {self._status.battery_level}%")
                elif self._status.battery_level < 10:
                    health['errors'].append(f"Critical battery: {self._status.battery_level}%")
            
            # Check temperature
            if self._status.temperature is not None:
                if self._status.temperature > 70:
                    health['warnings'].append(f"High temperature: {self._status.temperature}°C")
                elif self._status.temperature > 80:
                    health['errors'].append(f"Critical temperature: {self._status.temperature}°C")
            
            # Check error rate
            if self._command_count > 10:  # Only check after some activity
                error_rate = self._error_count / self._command_count
                if error_rate > 0.1:
                    health['warnings'].append(f"High error rate: {error_rate:.1%}")
                elif error_rate > 0.2:
                    health['errors'].append(f"Critical error rate: {error_rate:.1%}")
            
            # Check system state
            if self._status.system_state == SystemState.ERROR:
                health['errors'].append("System in error state")
            
            # Overall status
            if health['errors']:
                health['overall_status'] = 'critical'
            elif health['warnings']:
                health['overall_status'] = 'warning'
            
            return health
    
    def reset_metrics(self):
        """Reset performance metrics"""
        with self._lock:
            self._command_count = 0
            self._error_count = 0
            self.start_time = time.time()
            
            self.logger.info("📊 Performance metrics reset")
    
    def export_status(self) -> str:
        """Export current status as formatted string"""
        status_dict = self.get_status_dict()
        health = self.get_health_status()
        
        lines = [
            f"=== {self.robot_name} Status Report ===",
            f"State: {status_dict['system_state']}",
            f"Uptime: {status_dict['uptime']:.1f}s",
            f"Location: {status_dict['location']}",
            ""
        ]
        
        if status_dict['battery_level'] is not None:
            lines.append(f"Battery: {status_dict['battery_level']:.1f}%")
        
        if status_dict['temperature'] is not None:
            lines.append(f"Temperature: {status_dict['temperature']:.1f}°C")
        
        lines.extend([
            f"Commands processed: {status_dict['command_count']}",
            f"Errors: {status_dict['error_count']}",
            f"Health: {health['overall_status']}",
            ""
        ])
        
        if status_dict['last_command']:
            lines.append(f"Last command: {status_dict['last_command']}")
        
        if status_dict['current_action']:
            lines.append(f"Current action: {status_dict['current_action']}")
        
        return "\n".join(lines)
