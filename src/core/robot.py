"""
🤖 SARUS AI LAB ASSISTANT ROBOT - CORE CONTROLLER
Main robot controller integrating Jarvis + Sarus capabilities

This module contains the SarusRobot class which orchestrates all
subsystems including AI, hardware, navigation, safety, and communication.
"""

import asyncio
import logging
import time
import json
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime
from pathlib import Path

# Import subsystem managers (will be implemented)
try:
    from ..ai.speech_manager import SpeechManager
    from ..ai.llm_manager import LLMManager
    from ..ai.vision_manager import VisionManager
    from ..hardware.motor_controller import MotorController
    from ..hardware.sensor_manager import SensorManager
    from ..hardware.display_controller import DisplayController
    from ..navigation.navigation_manager import NavigationManager
    from ..safety.gas_monitor import GasMonitor
    from ..safety.face_recognition import FaceRecognition
    from ..safety.emergency_stop import EmergencyStop
    from ..communication.voice_interface import VoiceInterface
    from ..utils.state_manager import StateManager
    from ..utils.mission_logger import MissionLogger
    from ..config.settings import Config
except ImportError as e:
    # Graceful handling during development
    logging.warning(f"Some modules not yet implemented: {e}")

class RobotState(Enum):
    """Robot operational states for Jarvis + Sarus integration"""
    INITIALIZING = "initializing"
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"
    MOVING = "moving"
    EXPLORING = "exploring"
    MONITORING = "monitoring"
    ALERT = "alert"
    EMERGENCY = "emergency"
    ERROR = "error"
    SHUTDOWN = "shutdown"

class SarusRobot:
    """
    🤖 Main Sarus Robot Controller
    
    Integrates Jarvis safety features with Sarus mobility:
    - Voice interaction with Gemini AI
    - Environmental monitoring (temperature, humidity, gas)
    - Computer vision and face recognition
    - Autonomous navigation and movement
    - Safety protocols and emergency response
    """
    
    def __init__(self, config: Config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.state = RobotState.INITIALIZING
        self.start_time = datetime.now()
        
        # System status
        self.is_running = False
        self.last_heartbeat = time.time()
        self.authorized_users: List[str] = []
        self.current_mission: Optional[str] = None
        
        # Subsystem managers (will be initialized)
        self.speech_manager: Optional[SpeechManager] = None
        self.llm_manager: Optional[LLMManager] = None
        self.vision_manager: Optional[VisionManager] = None
        self.motor_controller: Optional[MotorController] = None
        self.sensor_manager: Optional[SensorManager] = None
        self.display_controller: Optional[DisplayController] = None
        self.navigation_manager: Optional[NavigationManager] = None
        self.voice_interface: Optional[VoiceInterface] = None
        self.state_manager: Optional[StateManager] = None
        self.mission_logger: Optional[MissionLogger] = None
        
        # System flags
        self.is_running = False
        self.wake_word_detected = False
        self.current_mission: Optional[Dict[str, Any]] = None
        
    async def initialize(self):
        """Initialize all robot subsystems"""
        try:
            self.logger.info("🤖 Initializing Sarus robot subsystems...")
            
            # Initialize core managers
            self.state_manager = StateManager()
            self.mission_logger = MissionLogger()
            
            # Initialize hardware
            if SYSTEM_CONFIG.get('hardware_enabled', True):
                self.motor_controller = MotorController()
                self.sensor_manager = SensorManager()
                self.display_controller = DisplayController()
                await self._initialize_hardware()
            
            # Initialize AI subsystems
            self.speech_manager = SpeechManager()
            self.llm_manager = LLMManager()
            self.vision_manager = VisionManager()
            await self._initialize_ai_systems()
            
            # Initialize navigation
            self.navigation_manager = NavigationManager(
                self.motor_controller,
                self.sensor_manager,
                self.vision_manager
            )
            
            # Initialize voice interface
            self.voice_interface = VoiceInterface(
                self.speech_manager,
                self.llm_manager,
                self.display_controller
            )
            
            self.state = RobotState.IDLE
            self.is_running = True
            
            self.logger.info("✅ Sarus initialization complete!")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize Sarus: {e}")
            self.state = RobotState.ERROR
            raise
    
    async def _initialize_hardware(self):
        """Initialize hardware subsystems"""
        self.logger.info("🔧 Initializing hardware...")
        
        if self.motor_controller:
            await self.motor_controller.initialize()
        
        if self.sensor_manager:
            await self.sensor_manager.initialize()
        
        if self.display_controller:
            await self.display_controller.initialize()
            await self.display_controller.show_startup_animation()
    
    async def _initialize_ai_systems(self):
        """Initialize AI subsystems"""
        self.logger.info("🧠 Initializing AI systems...")
        
        # Initialize speech processing
        if self.speech_manager:
            await self.speech_manager.initialize()
        
        # Initialize LLM
        if self.llm_manager:
            await self.llm_manager.initialize()
        
        # Initialize vision
        if self.vision_manager:
            await self.vision_manager.initialize()
    
    async def run(self):
        """Main robot operation loop"""
        self.logger.info("🚀 Starting Sarus main operation loop...")
        
        try:
            while self.is_running:
                if self.state == RobotState.IDLE:
                    await self._idle_loop()
                elif self.state == RobotState.LISTENING:
                    await self._listening_loop()
                elif self.state == RobotState.PROCESSING:
                    await self._processing_loop()
                elif self.state == RobotState.SPEAKING:
                    await self._speaking_loop()
                elif self.state == RobotState.MOVING:
                    await self._moving_loop()
                elif self.state == RobotState.EXPLORING:
                    await self._exploring_loop()
                elif self.state == RobotState.ERROR:
                    await self._error_loop()
                
                # Small delay to prevent busy waiting
                await asyncio.sleep(0.1)
                
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
            self.state = RobotState.ERROR
    
    async def _idle_loop(self):
        """Handle idle state - listen for wake word"""
        if self.voice_interface and await self.voice_interface.check_wake_word():
            self.logger.info("👂 Wake word detected!")
            self.state = RobotState.LISTENING
            if self.display_controller:
                await self.display_controller.show_listening_animation()
    
    async def _listening_loop(self):
        """Handle listening state - capture and process speech"""
        if self.voice_interface:
            command = await self.voice_interface.listen_for_command()
            if command:
                self.logger.info(f"🎤 Received command: {command}")
                self.state_manager.set_current_command(command)
                self.state = RobotState.PROCESSING
            else:
                # Timeout or no command detected
                self.state = RobotState.IDLE
    
    async def _processing_loop(self):
        """Handle processing state - analyze command and generate response"""
        command = self.state_manager.get_current_command()
        
        if command:
            # Get visual context if needed
            visual_context = None
            if self.vision_manager and self._command_needs_vision(command):
                visual_context = await self.vision_manager.analyze_scene()
            
            # Process command with LLM
            response = await self.llm_manager.process_command(
                command, 
                visual_context=visual_context,
                robot_state=self.state_manager.get_status()
            )
            
            # Determine action type
            action = self._parse_response_for_action(response)
            
            if action['type'] == 'speech':
                self.state_manager.set_current_response(response)
                self.state = RobotState.SPEAKING
            elif action['type'] == 'movement':
                self.state_manager.set_current_action(action)
                self.state = RobotState.MOVING
            elif action['type'] == 'exploration':
                await self._start_exploration_mission()
                self.state = RobotState.EXPLORING
            else:
                self.state = RobotState.IDLE
    
    async def _speaking_loop(self):
        """Handle speaking state - generate and play speech"""
        response = self.state_manager.get_current_response()
        
        if response and self.voice_interface:
            if self.display_controller:
                await self.display_controller.show_speaking_animation()
            
            await self.voice_interface.speak(response)
            
            if self.display_controller:
                await self.display_controller.show_idle_face()
        
        self.state = RobotState.IDLE
    
    async def _moving_loop(self):
        """Handle movement state - execute movement commands"""
        action = self.state_manager.get_current_action()
        
        if action and self.navigation_manager:
            success = await self.navigation_manager.execute_action(action)
            
            if not success:
                self.logger.warning("Movement failed, returning to idle")
        
        self.state = RobotState.IDLE
    
    async def _exploring_loop(self):
        """Handle exploration state - autonomous navigation"""
        if self.current_mission and self.navigation_manager:
            mission_complete = await self.navigation_manager.continue_exploration(
                self.current_mission
            )
            
            if mission_complete:
                await self._complete_exploration_mission()
                self.state = RobotState.IDLE
    
    async def _error_loop(self):
        """Handle error state - attempt recovery"""
        self.logger.warning("🚨 Robot in error state, attempting recovery...")
        
        # Basic recovery attempts
        await asyncio.sleep(5)  # Wait before retry
        
        try:
            # Reset subsystems if needed
            if self.display_controller:
                await self.display_controller.show_error_animation()
            
            self.state = RobotState.IDLE
            self.logger.info("✅ Recovery successful")
            
        except Exception as e:
            self.logger.error(f"❌ Recovery failed: {e}")
            await asyncio.sleep(10)  # Wait longer before next attempt
    
    def _command_needs_vision(self, command: str) -> bool:
        """Determine if command requires vision analysis"""
        vision_keywords = [
            'see', 'look', 'what', 'where', 'identify', 'find', 'describe'
        ]
        return any(keyword in command.lower() for keyword in vision_keywords)
    
    def _parse_response_for_action(self, response: str) -> Dict[str, Any]:
        """Parse LLM response to determine required action"""
        response_lower = response.lower()
        
        # Movement commands
        if any(word in response_lower for word in ['move', 'go', 'turn', 'navigate']):
            return {
                'type': 'movement',
                'command': response,
                'direction': self._extract_direction(response_lower)
            }
        
        # Exploration commands
        if any(word in response_lower for word in ['explore', 'search', 'patrol']):
            return {
                'type': 'exploration',
                'command': response
            }
        
        # Default to speech response
        return {
            'type': 'speech',
            'command': response
        }
    
    def _extract_direction(self, command: str) -> str:
        """Extract movement direction from command"""
        if 'forward' in command or 'ahead' in command:
            return 'forward'
        elif 'backward' in command or 'back' in command:
            return 'backward'
        elif 'left' in command:
            return 'left'
        elif 'right' in command:
            return 'right'
        else:
            return 'forward'  # Default
    
    async def _start_exploration_mission(self):
        """Start a new exploration mission"""
        self.current_mission = {
            'id': f"mission_{int(time.time())}",
            'start_time': time.time(),
            'objective': 'autonomous_exploration',
            'discovered_objects': [],
            'path_taken': [],
            'obstacles_encountered': []
        }
        
        self.mission_logger.start_mission(self.current_mission)
        self.logger.info(f"🗺️ Starting exploration mission: {self.current_mission['id']}")
    
    async def _complete_exploration_mission(self):
        """Complete current exploration mission"""
        if self.current_mission:
            self.current_mission['end_time'] = time.time()
            self.current_mission['duration'] = (
                self.current_mission['end_time'] - self.current_mission['start_time']
            )
            
            # Generate mission report
            report = await self._generate_mission_report()
            
            # Log mission completion
            self.mission_logger.complete_mission(self.current_mission, report)
            
            # Speak mission summary
            if self.voice_interface:
                await self.voice_interface.speak(report)
            
            self.logger.info(f"✅ Completed exploration mission: {self.current_mission['id']}")
            self.current_mission = None
    
    async def _generate_mission_report(self) -> str:
        """Generate a summary report of the exploration mission"""
        if not self.current_mission:
            return "No mission data available."
        
        objects_found = len(self.current_mission.get('discovered_objects', []))
        obstacles_hit = len(self.current_mission.get('obstacles_encountered', []))
        duration_minutes = int(self.current_mission.get('duration', 0) / 60)
        
        report = f"Mission complete. I explored for {duration_minutes} minutes, "
        report += f"found {objects_found} objects, and encountered {obstacles_hit} obstacles."
        
        if objects_found > 0:
            objects = self.current_mission['discovered_objects']
            object_names = [obj.get('name', 'unknown') for obj in objects[:3]]
            report += f" Notable objects include: {', '.join(object_names)}."
        
        return report
    
    def shutdown(self):
        """Shutdown robot gracefully"""
        self.logger.info("🛑 Shutting down Sarus...")
        self.is_running = False
        self.state = RobotState.SHUTDOWN
        
        # Shutdown all subsystems
        if self.motor_controller:
            self.motor_controller.stop_all_motors()
        
        if self.display_controller:
            asyncio.create_task(self.display_controller.show_shutdown_animation())
        
        # Save any pending mission data
        if self.current_mission and self.mission_logger:
            self.mission_logger.emergency_save(self.current_mission)
        
        self.logger.info("🔌 Sarus shutdown complete")
