"""
Voice interface for Sarus robot

Coordinates speech processing, LLM responses, and display feedback
to provide seamless voice interaction capabilities.
"""

import asyncio
import logging
import random
import time
from typing import Optional, Dict, Any

from ..ai.speech_manager import SpeechManager
from ..ai.llm_manager import LLMManager
from ..hardware.display_controller import DisplayController
from ..config.settings import SYSTEM_CONFIG, AI_PROMPTS
from ..utils.logger import get_logger

class VoiceInterface:
    """
    Manages voice interaction flow including wake word detection,
    speech recognition, AI processing, and response generation
    """
    
    def __init__(self, speech_manager: SpeechManager, 
                 llm_manager: LLMManager,
                 display_controller: Optional[DisplayController] = None):
        self.logger = get_logger(__name__)
        
        # Component references
        self.speech_manager = speech_manager
        self.llm_manager = llm_manager
        self.display_controller = display_controller
        
        # Configuration
        self.wake_word = SYSTEM_CONFIG.get('wake_word', 'hey sarus')
        self.command_timeout = SYSTEM_CONFIG.get('stt_timeout', 5.0)
        self.max_response_length = SYSTEM_CONFIG.get('llm_max_tokens', 500)
        
        # State tracking
        self.is_active = False
        self.last_interaction_time = 0
        self.conversation_count = 0
        
        # Performance metrics
        self.wake_word_detections = 0
        self.successful_interactions = 0
        self.failed_interactions = 0
        
    async def initialize(self):
        """Initialize voice interface"""
        self.logger.info("🎙️ Initializing voice interface...")
        
        try:
            # Start speech monitoring
            await self.speech_manager.start_listening()
            
            # Show ready state on display
            if self.display_controller:
                await self.display_controller.show_idle_face()
            
            self.is_active = True
            self.logger.info("✅ Voice interface initialized and active")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize voice interface: {e}")
            raise
    
    async def check_wake_word(self) -> bool:
        """
        Check for wake word detection
        
        Returns:
            True if wake word was detected, False otherwise
        """
        try:
            if await self.speech_manager.check_wake_word():
                self.wake_word_detections += 1
                self.last_interaction_time = time.time()
                
                self.logger.info(f"👂 Wake word '{self.wake_word}' detected!")
                
                # Provide audio feedback if possible
                await self._play_wake_acknowledgment()
                
                return True
                
        except Exception as e:
            self.logger.error(f"Error in wake word detection: {e}")
        
        return False
    
    async def listen_for_command(self) -> Optional[str]:
        """
        Listen for voice command after wake word
        
        Returns:
            Transcribed command text or None if failed/timeout
        """
        try:
            self.logger.info("🎤 Listening for voice command...")
            
            # Show listening state
            if self.display_controller:
                await self.display_controller.show_listening_animation()
            
            # Listen for command with timeout
            command = await self.speech_manager.listen_for_command(self.command_timeout)
            
            if command:
                self.conversation_count += 1
                self.logger.info(f"📝 Command received: '{command}'")
                
                return command.strip()
            else:
                self.logger.info("⏰ No command received within timeout")
                await self._handle_no_command()
                
        except Exception as e:
            self.logger.error(f"Error listening for command: {e}")
            self.failed_interactions += 1
        
        finally:
            # Return to idle state
            if self.display_controller:
                await self.display_controller.show_idle_face()
        
        return None
    
    async def speak(self, text: str) -> bool:
        """
        Convert text to speech and speak it
        
        Args:
            text: Text to speak
        
        Returns:
            True if successful, False otherwise
        """
        if not text:
            return False
        
        try:
            self.logger.info(f"🗣️ Speaking: '{text}'")
            
            # Show speaking animation
            if self.display_controller:
                await self.display_controller.show_speaking_animation()
            
            # Generate and play speech
            success = await self.speech_manager.speak(text)
            
            if success:
                self.successful_interactions += 1
            else:
                self.failed_interactions += 1
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error in speech generation: {e}")
            self.failed_interactions += 1
            return False
        
        finally:
            # Return to idle state
            if self.display_controller:
                await self.display_controller.show_idle_face()
    
    async def process_voice_interaction(self, visual_context: Optional[str] = None,
                                      robot_state: Optional[Dict[str, Any]] = None) -> bool:
        """
        Complete voice interaction flow: listen → process → respond
        
        Args:
            visual_context: Current visual scene description
            robot_state: Current robot state information
        
        Returns:
            True if interaction was successful, False otherwise
        """
        try:
            # Listen for command
            command = await self.listen_for_command()
            if not command:
                return False
            
            # Show thinking state
            if self.display_controller:
                await self.display_controller.show_thinking_animation()
            
            # Process command with LLM
            response = await self.llm_manager.process_command(
                command,
                visual_context=visual_context,
                robot_state=robot_state
            )
            
            if not response:
                response = "I'm sorry, I couldn't process that command."
            
            # Speak response
            success = await self.speak(response)
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error in voice interaction: {e}")
            
            # Try to provide error feedback
            await self.speak("I'm sorry, I encountered an error processing your request.")
            return False
    
    async def handle_voice_command(self, command: str, 
                                 visual_context: Optional[str] = None,
                                 robot_state: Optional[Dict[str, Any]] = None) -> str:
        """
        Process a voice command and return response
        
        Args:
            command: Voice command text
            visual_context: Current visual scene description
            robot_state: Current robot state information
        
        Returns:
            Generated response text
        """
        try:
            self.logger.info(f"🤔 Processing voice command: '{command}'")
            
            # Show thinking animation
            if self.display_controller:
                await self.display_controller.show_thinking_animation()
            
            # Process with LLM
            response = await self.llm_manager.process_command(
                command,
                visual_context=visual_context,
                robot_state=robot_state
            )
            
            if not response:
                response = self._get_fallback_response(command)
            
            self.logger.info(f"💭 Generated response: '{response}'")
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing voice command: {e}")
            return "I'm sorry, I'm having trouble understanding right now."
        
        finally:
            # Return to idle display
            if self.display_controller:
                await self.display_controller.show_idle_face()
    
    async def _play_wake_acknowledgment(self):
        """Play acknowledgment sound/response for wake word"""
        # Could play a short beep or say "Yes?" 
        # For now, just show visual feedback
        if self.display_controller:
            await self.display_controller.show_listening_animation()
        
        # Optional: brief acknowledgment sound
        # await self.speech_manager.speak("Yes?")
    
    async def _handle_no_command(self):
        """Handle case when no command is received after wake word"""
        # Provide helpful feedback
        responses = [
            "I didn't hear anything. Try saying your command clearly.",
            "I'm listening. What would you like me to do?",
            "I'm ready for your command.",
            "How can I help you?"
        ]
        
        import random
        response = random.choice(responses)
        await self.speak(response)
    
    def _get_fallback_response(self, command: str) -> str:
        """Generate fallback response when LLM fails"""
        command_lower = command.lower()
        
        # Greeting responses
        if any(word in command_lower for word in ['hello', 'hi', 'hey']):
            return random.choice(AI_PROMPTS.get('greeting_responses', [
                "Hello! How can I help you today?"
            ]))
        
        # Movement commands
        if any(word in command_lower for word in ['move', 'go', 'turn']):
            return "I understand you want me to move. Let me check if the path is clear."
        
        # Vision commands
        if any(word in command_lower for word in ['see', 'look', 'what']):
            return "Let me analyze what I can see with my camera."
        
        # Status commands
        if any(word in command_lower for word in ['status', 'how are you', 'battery']):
            return "I'm functioning normally and ready to assist you."
        
        # Default fallback
        return random.choice(AI_PROMPTS.get('error_responses', [
            "I'm sorry, I didn't understand that command."
        ]))
    
    async def announce_status(self, status_message: str):
        """Announce robot status via voice"""
        await self.speak(status_message)
    
    async def announce_discovery(self, object_name: str, description: str):
        """Announce object discovery"""
        announcement = f"I found a {object_name}. {description}"
        await self.speak(announcement)
    
    async def announce_mission_start(self, mission_type: str):
        """Announce mission start"""
        announcement = f"Starting {mission_type} mission. I'll let you know what I find."
        await self.speak(announcement)
    
    async def announce_mission_complete(self, summary: str):
        """Announce mission completion"""
        announcement = f"Mission complete. {summary}"
        await self.speak(announcement)
    
    async def provide_help(self):
        """Provide voice help/usage instructions"""
        help_text = """I'm Sarus, your lab assistant. You can ask me to:
        - Move around by saying 'move forward', 'turn left', or 'turn right'
        - Explore by saying 'explore the room' or 'search the area'
        - Describe what I see by saying 'what do you see' or 'look around'
        - Find objects by saying 'find the multimeter' or 'go to the computer'
        - Check my status by saying 'how are you' or 'battery level'
        
        Just say 'Hey Sarus' to get my attention, then give me a command."""
        
        await self.speak(help_text)
    
    def get_interaction_stats(self) -> Dict[str, Any]:
        """Get voice interaction statistics"""
        total_interactions = self.successful_interactions + self.failed_interactions
        success_rate = (self.successful_interactions / max(1, total_interactions)) * 100
        
        return {
            'wake_word_detections': self.wake_word_detections,
            'total_conversations': self.conversation_count,
            'successful_interactions': self.successful_interactions,
            'failed_interactions': self.failed_interactions,
            'success_rate_percent': success_rate,
            'last_interaction_time': self.last_interaction_time,
            'is_active': self.is_active,
            'time_since_last_interaction': time.time() - self.last_interaction_time if self.last_interaction_time > 0 else 0
        }
    
    async def test_voice_system(self):
        """Test voice system functionality"""
        self.logger.info("🧪 Testing voice system...")
        
        try:
            # Test TTS
            await self.speak("Voice system test. Can you hear me clearly?")
            
            # Test display integration
            if self.display_controller:
                await self.display_controller.show_happy_animation()
                await asyncio.sleep(2)
                await self.display_controller.show_idle_face()
            
            # Test wake word simulation (in debug mode)
            if SYSTEM_CONFIG.get('debug_mode', False):
                self.logger.info("Simulating wake word detection...")
                await self._play_wake_acknowledgment()
            
            self.logger.info("✅ Voice system test completed")
            
        except Exception as e:
            self.logger.error(f"Voice system test failed: {e}")
    
    async def shutdown(self):
        """Shutdown voice interface"""
        self.logger.info("🔇 Shutting down voice interface...")
        
        self.is_active = False
        
        # Stop speech processing
        await self.speech_manager.stop_listening()
        
        # Final announcement
        await self.speak("Voice interface shutting down. Goodbye!")
        
        # Cleanup display
        if self.display_controller:
            await self.display_controller.show_shutdown_animation()
        
        self.logger.info("🔌 Voice interface shutdown complete")
