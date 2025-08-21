"""
Large Language Model manager for Sarus robot

Handles communication with various LLM backends including local models
(via Ollama) and cloud services (OpenAI) for intelligent conversation
and command processing.
"""

import asyncio
import json
import logging
import os
import time
from typing import Dict, Any, Optional, List
import httpx

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# OpenAI client
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Google Gemini client
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from ..config.settings import SYSTEM_CONFIG, AI_PROMPTS
from ..utils.logger import get_logger, PerformanceLogger

class LLMManager:
    """
    Manages LLM interactions for conversational AI and command processing
    """
    
    def __init__(self):
        self.logger = get_logger(__name__)
        
        # Configuration
        self.primary_backend = SYSTEM_CONFIG.get('llm_primary', 'gemini')
        self.fallback_backend = SYSTEM_CONFIG.get('llm_fallback', 'ollama')
        self.local_model = SYSTEM_CONFIG.get('llm_model_local', 'llama3.2:3b')
        self.cloud_model = SYSTEM_CONFIG.get('llm_model_cloud', 'gemini-1.5-flash')
        self.openai_model = SYSTEM_CONFIG.get('llm_model_openai', 'gpt-4o-mini')
        self.max_tokens = SYSTEM_CONFIG.get('llm_max_tokens', 500)
        self.temperature = SYSTEM_CONFIG.get('llm_temperature', 0.7)
        self.timeout = SYSTEM_CONFIG.get('llm_timeout', 30.0)
        
        # API Keys
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        # Clients
        self.openai_client = None
        self.gemini_client = None
        self.ollama_available = False
        
        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
        self.max_history_length = 10
        
        # System prompts
        self.system_prompt = AI_PROMPTS.get('system_prompt', '')
        
    async def initialize(self):
        """Initialize LLM backends"""
        self.logger.info("🧠 Initializing LLM backends...")
        
        try:
            # Initialize OpenAI client
            await self._initialize_openai()
            
            # Initialize Gemini client
            await self._initialize_gemini()
            
            # Check Ollama availability
            await self._check_ollama()
            
            # Set up system conversation
            self._initialize_conversation()
            
            self.logger.info("✅ LLM manager initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize LLM manager: {e}")
            raise
    
    async def _initialize_openai(self):
        """Initialize OpenAI client"""
        if OPENAI_AVAILABLE and self.openai_api_key:
            self.openai_client = openai.AsyncOpenAI(api_key=self.openai_api_key)
            self.logger.info("✅ OpenAI client initialized")
        else:
            self.logger.warning("OpenAI not available or API key missing")
    
    async def _initialize_gemini(self):
        """Initialize Google Gemini client"""
        if GEMINI_AVAILABLE and self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_client = genai.GenerativeModel(self.cloud_model)
            self.logger.info(f"✅ Gemini client initialized with model: {self.cloud_model}")
        else:
            self.logger.warning("Gemini not available or API key missing")
    
    async def _check_ollama(self):
        """Check if Ollama service is available"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get("http://localhost:11434/api/tags")
                if response.status_code == 200:
                    models = response.json()
                    available_models = [model['name'] for model in models.get('models', [])]
                    
                    if self.local_model in available_models:
                        self.ollama_available = True
                        self.logger.info(f"✅ Ollama available with model: {self.local_model}")
                    else:
                        self.logger.warning(f"Model {self.local_model} not found in Ollama")
                        self.logger.info(f"Available models: {available_models}")
                else:
                    self.logger.warning(f"Ollama health check failed: {response.status_code}")
                    
        except Exception as e:
            self.logger.warning(f"Ollama not available: {e}")
            self.ollama_available = False
    
    def _initialize_conversation(self):
        """Initialize conversation with system prompt"""
        if self.system_prompt:
            self.conversation_history = [
                {"role": "system", "content": self.system_prompt}
            ]
    
    async def process_command(
        self, 
        command: str, 
        visual_context: Optional[str] = None,
        robot_state: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Process a user command and generate an appropriate response
        
        Args:
            command: User voice command
            visual_context: Description of what robot sees (optional)
            robot_state: Current robot state information (optional)
        
        Returns:
            Generated response text
        """
        try:
            self.logger.info(f"🤔 Processing command: '{command}'")
            
            # Build context-aware prompt
            enhanced_prompt = self._build_enhanced_prompt(
                command, visual_context, robot_state
            )
            
            # Try primary backend first
            response = None
            if self.primary_backend == 'gemini' and self.gemini_client:
                response = await self._query_gemini(enhanced_prompt)
            elif self.primary_backend == 'ollama' and self.ollama_available:
                response = await self._query_ollama(enhanced_prompt)
            elif self.primary_backend == 'openai' and self.openai_client:
                response = await self._query_openai(enhanced_prompt)
            
            # Fallback to secondary backend if primary fails
            if not response:
                self.logger.warning(f"Primary backend ({self.primary_backend}) failed, trying fallback")
                
                if self.fallback_backend == 'gemini' and self.gemini_client:
                    response = await self._query_gemini(enhanced_prompt)
                elif self.fallback_backend == 'openai' and self.openai_client:
                    response = await self._query_openai(enhanced_prompt)
                elif self.fallback_backend == 'ollama' and self.ollama_available:
                    response = await self._query_ollama(enhanced_prompt)
            
            # If all backends fail, use predefined responses
            if not response:
                response = self._get_fallback_response(command)
            
            # Update conversation history
            self._update_conversation_history(command, response)
            
            self.logger.info(f"💭 Generated response: '{response}'")
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to process command: {e}")
            return "I'm sorry, I'm having trouble processing your request right now."
    
    def _build_enhanced_prompt(
        self, 
        command: str, 
        visual_context: Optional[str] = None,
        robot_state: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build context-enhanced prompt for better AI responses"""
        
        prompt_parts = [f"User command: {command}"]
        
        if visual_context:
            prompt_parts.append(f"What I can see: {visual_context}")
        
        if robot_state:
            location = robot_state.get('location', 'unknown')
            battery = robot_state.get('battery_level', 'unknown')
            prompt_parts.append(f"My current location: {location}")
            prompt_parts.append(f"Battery level: {battery}%")
        
        # Add conversation context
        if len(self.conversation_history) > 1:
            recent_context = self.conversation_history[-2:]  # Last exchange
            context_str = " | ".join([f"{msg['role']}: {msg['content']}" for msg in recent_context])
            prompt_parts.append(f"Recent conversation: {context_str}")
        
        return "\n".join(prompt_parts)
    
    async def _query_ollama(self, prompt: str) -> Optional[str]:
        """Query Ollama local LLM"""
        try:
            with PerformanceLogger("Ollama query"):
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    payload = {
                        "model": self.local_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": self.temperature,
                            "num_predict": self.max_tokens
                        }
                    }
                    
                    response = await client.post(
                        "http://localhost:11434/api/generate",
                        json=payload
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        return result.get('response', '').strip()
                    else:
                        self.logger.error(f"Ollama API error: {response.status_code}")
                        
        except Exception as e:
            self.logger.error(f"Ollama query failed: {e}")
        
        return None
    
    async def _query_openai(self, prompt: str) -> Optional[str]:
        """Query OpenAI API"""
        if not self.openai_client:
            return None
        
        try:
            with PerformanceLogger("OpenAI query"):
                # Build messages for chat completion
                messages = self.conversation_history.copy()
                messages.append({"role": "user", "content": prompt})
                
                response = await self.openai_client.chat.completions.create(
                    model=self.cloud_model,
                    messages=messages,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    timeout=self.timeout
                )
                
                if response.choices:
                    return response.choices[0].message.content.strip()
                    
        except Exception as e:
            self.logger.error(f"OpenAI query failed: {e}")
        
        return None
    
    async def _query_gemini(self, prompt: str) -> Optional[str]:
        """Query Google Gemini API"""
        if not self.gemini_client:
            return None
        
        try:
            with PerformanceLogger("Gemini query"):
                # Build conversation context
                conversation_text = "\n".join([
                    f"{msg['role']}: {msg['content']}" 
                    for msg in self.conversation_history[-4:]  # Last 4 messages for context
                ])
                
                full_prompt = f"{conversation_text}\nuser: {prompt}"
                
                response = await asyncio.to_thread(
                    self.gemini_client.generate_content,
                    full_prompt
                )
                
                if response.text:
                    return response.text.strip()
                    
        except Exception as e:
            self.logger.error(f"Gemini query failed: {e}")
        
        return None
    
    def _get_fallback_response(self, command: str) -> str:
        """Generate fallback response when all LLM backends fail"""
        command_lower = command.lower()
        
        # Movement commands
        if any(word in command_lower for word in ['move', 'go', 'turn', 'forward', 'back']):
            return "I'll help you with movement. Please make sure the path is clear."
        
        # Vision commands
        if any(word in command_lower for word in ['see', 'look', 'what', 'describe']):
            return "Let me analyze what I can see through my camera."
        
        # Exploration commands
        if any(word in command_lower for word in ['explore', 'search', 'find']):
            return "I'll start exploring the area. This may take a few minutes."
        
        # Greeting
        if any(word in command_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm Sarus, your lab assistant. How can I help you today?"
        
        # Default response
        return AI_PROMPTS.get('error_responses', [
            "I'm sorry, I didn't understand that command."
        ])[0]
    
    def _update_conversation_history(self, user_input: str, assistant_response: str):
        """Update conversation history with new exchange"""
        self.conversation_history.extend([
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": assistant_response}
        ])
        
        # Keep history within limits
        if len(self.conversation_history) > self.max_history_length:
            # Keep system message and recent exchanges
            self.conversation_history = (
                self.conversation_history[:1] +  # System message
                self.conversation_history[-(self.max_history_length-1):]  # Recent exchanges
            )
    
    async def generate_exploration_summary(
        self, 
        discovered_objects: List[Dict[str, Any]],
        path_taken: List[str],
        duration: float
    ) -> str:
        """
        Generate a summary of an exploration mission
        
        Args:
            discovered_objects: List of objects found during exploration
            path_taken: List of directions/locations visited
            duration: Mission duration in seconds
        
        Returns:
            Generated mission summary
        """
        try:
            # Build exploration context
            objects_desc = ", ".join([obj.get('name', 'unknown object') for obj in discovered_objects])
            path_desc = " → ".join(path_taken[-5:])  # Last 5 movements
            duration_min = int(duration / 60)
            
            prompt = f"""Generate a brief mission report for a lab exploration:
            - Duration: {duration_min} minutes
            - Objects found: {objects_desc}
            - Path taken: {path_desc}
            
            Keep it concise and informative, as if reporting to a lab supervisor."""
            
            # Try to use LLM for summary
            summary = None
            if self.ollama_available:
                summary = await self._query_ollama(prompt)
            elif self.openai_client:
                summary = await self._query_openai(prompt)
            
            if summary:
                return summary
            else:
                # Fallback summary
                return f"Exploration complete. Found {len(discovered_objects)} objects in {duration_min} minutes."
                
        except Exception as e:
            self.logger.error(f"Failed to generate exploration summary: {e}")
            return "Exploration mission completed."
    
    def clear_conversation_history(self):
        """Clear conversation history except system prompt"""
        self._initialize_conversation()
        self.logger.info("🧹 Conversation history cleared")
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Get statistics about current conversation"""
        return {
            "message_count": len(self.conversation_history) - 1,  # Exclude system message
            "backends_available": {
                "ollama": self.ollama_available,
                "openai": self.openai_client is not None
            },
            "primary_backend": self.primary_backend,
            "fallback_backend": self.fallback_backend
        }
