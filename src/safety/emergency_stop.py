"""
🛑 EMERGENCY STOP - Critical Safety System
Emergency stop and safety shutdown procedures

Provides immediate emergency response capabilities for
critical safety situations.
"""

import asyncio
import logging
import time
from typing import Callable, Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class EmergencyType(Enum):
    """Types of emergency situations"""
    GAS_LEAK = "gas_leak"
    FIRE = "fire"
    INTRUDER = "intruder"
    HARDWARE_FAILURE = "hardware_failure"
    USER_EMERGENCY = "user_emergency"
    SYSTEM_CRITICAL = "system_critical"
    MANUAL_STOP = "manual_stop"

@dataclass
class EmergencyEvent:
    """Emergency event data"""
    event_type: EmergencyType
    severity: str  # 'low', 'medium', 'high', 'critical'
    message: str
    timestamp: datetime
    source: str
    data: Dict[str, Any]

class EmergencyStop:
    """
    🚨 Emergency Stop and Safety System
    
    Features:
    - Immediate system shutdown procedures
    - Emergency alert broadcasting
    - Safety protocol execution
    - Critical event logging
    """
    
    def __init__(self, config, robot_controller=None):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.robot_controller = robot_controller
        
        # Emergency state
        self.emergency_active = False
        self.emergency_level = 0  # 0=normal, 1=warning, 2=alert, 3=critical
        self.current_emergency: Optional[EmergencyEvent] = None
        
        # Emergency procedures
        self.emergency_procedures = {
            EmergencyType.GAS_LEAK: self._handle_gas_leak,
            EmergencyType.FIRE: self._handle_fire_emergency,
            EmergencyType.INTRUDER: self._handle_security_breach,
            EmergencyType.HARDWARE_FAILURE: self._handle_hardware_failure,
            EmergencyType.USER_EMERGENCY: self._handle_user_emergency,
            EmergencyType.SYSTEM_CRITICAL: self._handle_system_critical,
            EmergencyType.MANUAL_STOP: self._handle_manual_stop
        }
        
        # Callback functions
        self.alert_callbacks: List[Callable] = []
        self.shutdown_callbacks: List[Callable] = []
        
        # Emergency history
        self.emergency_history: List[EmergencyEvent] = []
        
        self.logger.info("Emergency Stop system initialized")
    
    def register_alert_callback(self, callback: Callable):
        """Register callback for emergency alerts"""
        self.alert_callbacks.append(callback)
    
    def register_shutdown_callback(self, callback: Callable):
        """Register callback for emergency shutdown"""
        self.shutdown_callbacks.append(callback)
    
    async def trigger_emergency(self, 
                              emergency_type: EmergencyType, 
                              message: str, 
                              severity: str = 'high',
                              source: str = 'system',
                              data: Optional[Dict[str, Any]] = None):
        """Trigger emergency response"""
        
        if data is None:
            data = {}
        
        # Create emergency event
        event = EmergencyEvent(
            event_type=emergency_type,
            severity=severity,
            message=message,
            timestamp=datetime.now(),
            source=source,
            data=data
        )
        
        # Log emergency
        self.emergency_history.append(event)
        self.current_emergency = event
        
        # Set emergency level
        severity_levels = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
        self.emergency_level = severity_levels.get(severity, 3)
        
        self.logger.critical(f"EMERGENCY TRIGGERED: {emergency_type.value} - {message}")
        
        # Execute emergency procedure
        if emergency_type in self.emergency_procedures:
            await self.emergency_procedures[emergency_type](event)
        else:
            await self._default_emergency_procedure(event)
        
        # Broadcast emergency alert
        await self._broadcast_emergency(event)
    
    async def _handle_gas_leak(self, event: EmergencyEvent):
        """Handle gas leak emergency"""
        self.emergency_active = True
        
        self.logger.critical("🚨 GAS LEAK EMERGENCY PROTOCOL ACTIVATED")
        
        # Immediate actions
        await self._stop_all_movement()
        await self._activate_ventilation()  # If available
        await self._trigger_evacuation_alert()
        
        # Voice announcement
        if self.robot_controller and hasattr(self.robot_controller, 'speak'):
            await self.robot_controller.speak(
                "EMERGENCY: Gas leak detected! Evacuating area immediately! "
                "All personnel must leave the lab now!"
            )
        
        # Log critical event
        self.logger.critical(f"Gas leak emergency: {event.data}")
    
    async def _handle_fire_emergency(self, event: EmergencyEvent):
        """Handle fire emergency"""
        self.emergency_active = True
        
        self.logger.critical("🔥 FIRE EMERGENCY PROTOCOL ACTIVATED")
        
        # Immediate actions
        await self._stop_all_movement()
        await self._shutdown_electrical_systems()
        await self._trigger_fire_alarm()
        
        # Voice announcement
        if self.robot_controller and hasattr(self.robot_controller, 'speak'):
            await self.robot_controller.speak(
                "FIRE EMERGENCY! Evacuate immediately! "
                "Exit the building using the nearest safe exit!"
            )
    
    async def _handle_security_breach(self, event: EmergencyEvent):
        """Handle security breach"""
        self.emergency_active = True
        
        self.logger.critical("🔐 SECURITY BREACH PROTOCOL ACTIVATED")
        
        # Security actions
        await self._lock_down_systems()
        await self._start_security_recording()
        await self._alert_security_personnel()
        
        # Voice announcement
        if self.robot_controller and hasattr(self.robot_controller, 'speak'):
            await self.robot_controller.speak(
                "Security alert: Unauthorized personnel detected. "
                "Security has been notified."
            )
    
    async def _handle_hardware_failure(self, event: EmergencyEvent):
        """Handle critical hardware failure"""
        self.emergency_active = True
        
        self.logger.critical("⚡ HARDWARE FAILURE EMERGENCY")
        
        # Safe shutdown procedures
        await self._stop_all_movement()
        await self._safe_shutdown_sequence()
        
        # Voice announcement
        if self.robot_controller and hasattr(self.robot_controller, 'speak'):
            await self.robot_controller.speak(
                "Critical hardware failure detected. "
                "Entering safe mode. Please check system status."
            )
    
    async def _handle_user_emergency(self, event: EmergencyEvent):
        """Handle user-triggered emergency"""
        self.emergency_active = True
        
        self.logger.critical("👤 USER EMERGENCY ACTIVATED")
        
        # User emergency actions
        await self._stop_all_movement()
        await self._alert_emergency_contacts()
        
        # Voice announcement
        if self.robot_controller and hasattr(self.robot_controller, 'speak'):
            await self.robot_controller.speak(
                "User emergency activated. Help is being contacted. "
                "Please stay calm and follow safety procedures."
            )
    
    async def _handle_system_critical(self, event: EmergencyEvent):
        """Handle critical system error"""
        self.emergency_active = True
        
        self.logger.critical("💻 CRITICAL SYSTEM ERROR")
        
        # System protection
        await self._emergency_data_backup()
        await self._controlled_shutdown()
        
        # Voice announcement
        if self.robot_controller and hasattr(self.robot_controller, 'speak'):
            await self.robot_controller.speak(
                "Critical system error. Initiating emergency shutdown. "
                "Data is being protected."
            )
    
    async def _handle_manual_stop(self, event: EmergencyEvent):
        """Handle manual emergency stop"""
        self.emergency_active = True
        
        self.logger.warning("🛑 MANUAL EMERGENCY STOP")
        
        # Immediate stop
        await self._stop_all_movement()
        await self._pause_all_operations()
        
        # Voice announcement
        if self.robot_controller and hasattr(self.robot_controller, 'speak'):
            await self.robot_controller.speak(
                "Manual emergency stop activated. All operations paused."
            )
    
    async def _default_emergency_procedure(self, event: EmergencyEvent):
        """Default emergency procedure for unknown types"""
        self.emergency_active = True
        
        self.logger.critical(f"UNKNOWN EMERGENCY TYPE: {event.event_type}")
        
        # Safe defaults
        await self._stop_all_movement()
        await self._alert_all_systems()
    
    async def _stop_all_movement(self):
        """Immediately stop all robot movement"""
        try:
            if self.robot_controller:
                if hasattr(self.robot_controller, 'motor_controller'):
                    await self.robot_controller.motor_controller.emergency_stop()
                if hasattr(self.robot_controller, 'navigation_manager'):
                    await self.robot_controller.navigation_manager.emergency_stop()
            
            self.logger.info("All movement stopped")
        except Exception as e:
            self.logger.error(f"Error stopping movement: {e}")
    
    async def _activate_ventilation(self):
        """Activate ventilation system if available"""
        # This would control lab ventilation fans
        self.logger.info("Ventilation system activation requested")
    
    async def _trigger_evacuation_alert(self):
        """Trigger lab evacuation procedures"""
        # This would interface with building alarm systems
        self.logger.critical("EVACUATION ALERT TRIGGERED")
    
    async def _shutdown_electrical_systems(self):
        """Safely shutdown electrical systems"""
        # This would control lab electrical systems
        self.logger.info("Electrical systems shutdown initiated")
    
    async def _trigger_fire_alarm(self):
        """Trigger fire alarm systems"""
        # This would interface with fire alarm systems
        self.logger.critical("FIRE ALARM TRIGGERED")
    
    async def _lock_down_systems(self):
        """Lock down all systems for security"""
        # This would lock access to systems
        self.logger.info("Systems locked down for security")
    
    async def _start_security_recording(self):
        """Start security recording"""
        # This would start video recording
        self.logger.info("Security recording started")
    
    async def _alert_security_personnel(self):
        """Alert security personnel"""
        # This would send alerts to security
        self.logger.info("Security personnel alerted")
    
    async def _safe_shutdown_sequence(self):
        """Execute safe shutdown sequence"""
        try:
            # Call all shutdown callbacks
            for callback in self.shutdown_callbacks:
                await callback()
            
            self.logger.info("Safe shutdown sequence completed")
        except Exception as e:
            self.logger.error(f"Error in shutdown sequence: {e}")
    
    async def _alert_emergency_contacts(self):
        """Alert emergency contacts"""
        # This would send notifications to emergency contacts
        self.logger.info("Emergency contacts alerted")
    
    async def _emergency_data_backup(self):
        """Perform emergency data backup"""
        # This would backup critical data
        self.logger.info("Emergency data backup initiated")
    
    async def _controlled_shutdown(self):
        """Perform controlled system shutdown"""
        await self._safe_shutdown_sequence()
        self.logger.info("Controlled shutdown completed")
    
    async def _pause_all_operations(self):
        """Pause all non-critical operations"""
        # This would pause robot operations
        self.logger.info("All operations paused")
    
    async def _alert_all_systems(self):
        """Alert all systems of emergency"""
        # This would broadcast to all subsystems
        self.logger.info("All systems alerted")
    
    async def _broadcast_emergency(self, event: EmergencyEvent):
        """Broadcast emergency to all registered callbacks"""
        alert_data = {
            'type': 'emergency',
            'emergency_type': event.event_type.value,
            'severity': event.severity,
            'message': event.message,
            'timestamp': event.timestamp,
            'source': event.source,
            'data': event.data
        }
        
        # Call all alert callbacks
        for callback in self.alert_callbacks:
            try:
                await callback(alert_data)
            except Exception as e:
                self.logger.error(f"Error in alert callback: {e}")
    
    async def reset_emergency(self):
        """Reset emergency state after resolution"""
        if self.emergency_active:
            self.logger.info("Resetting emergency state")
            
            self.emergency_active = False
            self.emergency_level = 0
            self.current_emergency = None
            
            # Voice announcement
            if self.robot_controller and hasattr(self.robot_controller, 'speak'):
                await self.robot_controller.speak(
                    "Emergency state cleared. Systems returning to normal operation."
                )
    
    def is_emergency_active(self) -> bool:
        """Check if emergency is currently active"""
        return self.emergency_active
    
    def get_emergency_level(self) -> int:
        """Get current emergency level"""
        return self.emergency_level
    
    def get_current_emergency(self) -> Optional[EmergencyEvent]:
        """Get current emergency event"""
        return self.current_emergency
    
    def get_emergency_history(self, limit: int = 50) -> List[EmergencyEvent]:
        """Get emergency history"""
        return self.emergency_history[-limit:]
    
    def get_status_report(self) -> str:
        """Get human-readable status report"""
        if not self.emergency_active:
            recent_emergencies = len([e for e in self.emergency_history 
                                    if (datetime.now() - e.timestamp).days < 1])
            return f"✅ No active emergencies. {recent_emergencies} events in last 24h."
        else:
            event = self.current_emergency
            duration = (datetime.now() - event.timestamp).total_seconds()
            return f"🚨 ACTIVE EMERGENCY: {event.event_type.value} ({duration:.0f}s ago) - {event.message}"
