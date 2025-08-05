"""
Speech processing manager for Sarus robot

Handles speech-to-text (STT), text-to-speech (TTS), and wake word detection
using multiple backend engines for flexibility and reliability.
"""

import asyncio
import logging
import queue
import threading
import time
from typing import Optional, Dict, Any
import numpy as np

# Audio processing
try:
    import pyaudio
    import wave
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    logging.warning("PyAudio not available - audio features disabled")

# Speech recognition engines
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

try:
    import vosk
    import json
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    import pvporcupine
    PORCUPINE_AVAILABLE = True
except ImportError:
    PORCUPINE_AVAILABLE = False

from ..config.settings import SYSTEM_CONFIG, AUDIO_DIR
from ..utils.logger import get_logger, PerformanceLogger

class SpeechManager:
    """
    Manages all speech-related functionality including STT, TTS, and wake word detection
    """
    
    def __init__(self):
        self.logger = get_logger(__name__)
        
        # Audio configuration
        self.sample_rate = SYSTEM_CONFIG.get('sample_rate', 16000)
        self.chunk_size = SYSTEM_CONFIG.get('chunk_size', 1024)
        self.channels = SYSTEM_CONFIG.get('channels', 1)
        
        # Audio system
        self.audio = None
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.recording_thread = None
        
        # Speech engines
        self.whisper_model = None
        self.vosk_model = None
        self.tts_engine = None
        self.porcupine = None
        
        # Wake word detection
        self.wake_word_detected = False
        self.wake_word_sensitivity = SYSTEM_CONFIG.get('wake_word_sensitivity', 0.5)
        
    async def initialize(self):
        """Initialize speech processing systems"""
        self.logger.info("🎤 Initializing speech processing...")
        
        if not AUDIO_AVAILABLE:
            self.logger.warning("Audio not available - running in simulation mode")
            return
        
        try:
            # Initialize audio system
            self.audio = pyaudio.PyAudio()
            
            # Initialize STT engines
            await self._initialize_stt()
            
            # Initialize TTS engine
            await self._initialize_tts()
            
            # Initialize wake word detection
            await self._initialize_wake_word()
            
            self.logger.info("✅ Speech processing initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize speech processing: {e}")
            raise
    
    async def _initialize_stt(self):
        """Initialize speech-to-text engines"""
        stt_engine = SYSTEM_CONFIG.get('stt_engine', 'whisper')
        
        if stt_engine == 'whisper' and WHISPER_AVAILABLE:
            with PerformanceLogger("Loading Whisper model"):
                model_size = SYSTEM_CONFIG.get('stt_model', 'base')
                self.whisper_model = whisper.load_model(model_size)
                self.logger.info(f"✅ Whisper model '{model_size}' loaded")
        
        elif stt_engine == 'vosk' and VOSK_AVAILABLE:
            model_path = AUDIO_DIR / "vosk-model"
            if model_path.exists():
                self.vosk_model = vosk.Model(str(model_path))
                self.logger.info("✅ Vosk model loaded")
            else:
                self.logger.warning(f"Vosk model not found at {model_path}")
        
        else:
            self.logger.warning(f"STT engine '{stt_engine}' not available")
    
    async def _initialize_tts(self):
        """Initialize text-to-speech engine"""
        if PYTTSX3_AVAILABLE:
            self.tts_engine = pyttsx3.init()
            
            # Configure voice settings
            rate = SYSTEM_CONFIG.get('tts_voice_rate', 150)
            volume = SYSTEM_CONFIG.get('tts_voice_volume', 0.8)
            
            self.tts_engine.setProperty('rate', rate)
            self.tts_engine.setProperty('volume', volume)
            
            # Set voice if specified
            voices = self.tts_engine.getProperty('voices')
            voice_id = SYSTEM_CONFIG.get('tts_voice_id', 0)
            if voices and 0 <= voice_id < len(voices):
                self.tts_engine.setProperty('voice', voices[voice_id].id)
            
            self.logger.info("✅ TTS engine initialized")
        else:
            self.logger.warning("TTS engine not available")
    
    async def _initialize_wake_word(self):
        """Initialize wake word detection"""
        if PORCUPINE_AVAILABLE:
            access_key = SYSTEM_CONFIG.get('porcupine_access_key')
            if access_key:
                try:
                    self.porcupine = pvporcupine.create(
                        access_key=access_key,
                        keywords=['hey siri']  # Will use built-in keyword
                    )
                    self.logger.info("✅ Porcupine wake word detection initialized")
                except Exception as e:
                    self.logger.warning(f"Failed to initialize Porcupine: {e}")
        
        if not self.porcupine:
            self.logger.info("Using simple wake word detection")
    
    async def start_listening(self):
        """Start continuous audio listening"""
        if not AUDIO_AVAILABLE or self.is_listening:
            return
        
        self.is_listening = True
        
        # Start recording thread
        self.recording_thread = threading.Thread(target=self._recording_loop)
        self.recording_thread.daemon = True
        self.recording_thread.start()
        
        self.logger.info("👂 Started audio listening")
    
    async def stop_listening(self):
        """Stop audio listening"""
        self.is_listening = False
        
        if self.recording_thread:
            self.recording_thread.join(timeout=2)
        
        self.logger.info("🔇 Stopped audio listening")
    
    def _recording_loop(self):
        """Continuous audio recording loop (runs in separate thread)"""
        if not self.audio:
            return
        
        try:
            stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            while self.is_listening:
                try:
                    data = stream.read(self.chunk_size, exception_on_overflow=False)
                    self.audio_queue.put(data)
                except Exception as e:
                    self.logger.error(f"Audio recording error: {e}")
                    break
            
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            self.logger.error(f"Failed to start audio recording: {e}")
    
    async def check_wake_word(self) -> bool:
        """
        Check for wake word in audio stream
        
        Returns:
            True if wake word detected, False otherwise
        """
        if not self.is_listening:
            await self.start_listening()
        
        # Simple implementation - in reality would use Porcupine or Vosk
        # For now, simulate wake word detection
        if SYSTEM_CONFIG.get('debug_mode', False):
            # In debug mode, simulate wake word every 10 seconds
            return time.time() % 10 < 0.1
        
        # TODO: Implement actual wake word detection with audio processing
        return False
    
    async def listen_for_command(self, timeout: float = 5.0) -> Optional[str]:
        """
        Listen for a voice command after wake word detection
        
        Args:
            timeout: Maximum time to wait for command
        
        Returns:
            Transcribed command text or None if timeout/error
        """
        if not AUDIO_AVAILABLE:
            # Simulation mode for development
            await asyncio.sleep(1)
            return "what do you see"  # Simulate command
        
        try:
            with PerformanceLogger("Voice command recognition"):
                # Record audio for command
                audio_data = await self._record_command(timeout)
                
                if audio_data:
                    # Transcribe audio to text
                    command = await self._transcribe_audio(audio_data)
                    return command
                
        except Exception as e:
            self.logger.error(f"Failed to process voice command: {e}")
        
        return None
    
    async def _record_command(self, timeout: float) -> Optional[bytes]:
        """
        Record audio for a command with timeout
        
        Args:
            timeout: Maximum recording time
        
        Returns:
            Raw audio data or None
        """
        audio_frames = []
        start_time = time.time()
        
        # Clear any existing audio in queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except queue.Empty:
                break
        
        # Record audio until timeout or silence detected
        while time.time() - start_time < timeout:
            try:
                frame = self.audio_queue.get(timeout=0.1)
                audio_frames.append(frame)
            except queue.Empty:
                continue
        
        if audio_frames:
            return b''.join(audio_frames)
        
        return None
    
    async def _transcribe_audio(self, audio_data: bytes) -> Optional[str]:
        """
        Transcribe audio data to text
        
        Args:
            audio_data: Raw audio bytes
        
        Returns:
            Transcribed text or None
        """
        try:
            if self.whisper_model:
                return await self._transcribe_with_whisper(audio_data)
            elif self.vosk_model:
                return await self._transcribe_with_vosk(audio_data)
            else:
                self.logger.warning("No STT engine available")
                return None
                
        except Exception as e:
            self.logger.error(f"Transcription failed: {e}")
            return None
    
    async def _transcribe_with_whisper(self, audio_data: bytes) -> Optional[str]:
        """Transcribe using Whisper model"""
        try:
            # Convert audio data to numpy array
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Transcribe with Whisper
            result = self.whisper_model.transcribe(audio_np)
            text = result.get('text', '').strip()
            
            if text:
                self.logger.info(f"🎤 Transcribed: '{text}'")
                return text
            
        except Exception as e:
            self.logger.error(f"Whisper transcription error: {e}")
        
        return None
    
    async def _transcribe_with_vosk(self, audio_data: bytes) -> Optional[str]:
        """Transcribe using Vosk model"""
        try:
            rec = vosk.KaldiRecognizer(self.vosk_model, self.sample_rate)
            
            if rec.AcceptWaveform(audio_data):
                result = json.loads(rec.Result())
                text = result.get('text', '').strip()
                
                if text:
                    self.logger.info(f"🎤 Transcribed: '{text}'")
                    return text
            
        except Exception as e:
            self.logger.error(f"Vosk transcription error: {e}")
        
        return None
    
    async def speak(self, text: str) -> bool:
        """
        Convert text to speech and play it
        
        Args:
            text: Text to speak
        
        Returns:
            True if successful, False otherwise
        """
        if not text:
            return False
        
        try:
            self.logger.info(f"🔊 Speaking: '{text}'")
            
            if self.tts_engine:
                # Use pyttsx3 for TTS
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                return True
            else:
                # Fallback: just log the text
                self.logger.info(f"TTS not available, would speak: '{text}'")
                await asyncio.sleep(len(text) * 0.05)  # Simulate speaking time
                return True
                
        except Exception as e:
            self.logger.error(f"TTS failed: {e}")
            return False
    
    def cleanup(self):
        """Clean up speech processing resources"""
        self.is_listening = False
        
        if self.recording_thread:
            self.recording_thread.join(timeout=2)
        
        if self.audio:
            self.audio.terminate()
        
        if self.porcupine:
            self.porcupine.delete()
        
        self.logger.info("🧹 Speech processing cleanup complete")
