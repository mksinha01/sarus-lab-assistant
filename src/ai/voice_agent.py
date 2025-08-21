#!/usr/bin/env python3
"""
🎤 VOICE CONVERSATION SYSTEM FOR SARUS ROBOT
Interactive voice communication with the robot agent
"""

import sys
import os
import threading
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class VoiceAgent:
    """Voice conversation system for Sarus Robot"""
    
    def __init__(self):
        self.is_listening = False
        self.is_speaking = False
        self.conversation_active = False
        self.robot_name = "Sarus"
        
    def check_voice_dependencies(self):
        """Check if voice dependencies are available"""
        missing_deps = []
        
        try:
            import speech_recognition as sr
        except ImportError:
            missing_deps.append("speech_recognition")
        
        try:
            import pyttsx3
        except ImportError:
            missing_deps.append("pyttsx3")
        
        try:
            import pyaudio
        except ImportError:
            missing_deps.append("pyaudio")
        
        return missing_deps
    
    def install_voice_dependencies(self):
        """Install voice conversation dependencies"""
        print("🎤 Installing Voice Conversation Dependencies...")
        
        packages = [
            "SpeechRecognition>=3.10.0",
            "pyttsx3>=2.90",
            "pyaudio>=0.2.11"
        ]
        
        import subprocess
        for package in packages:
            print(f"   Installing {package}...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                             check=True, capture_output=True)
                print(f"   ✅ {package} installed")
            except subprocess.CalledProcessError as e:
                print(f"   ⚠️ Could not install {package}: {e}")
        
        print("✅ Voice dependencies installation complete!")
    
    def initialize_voice_system(self):
        """Initialize speech recognition and text-to-speech"""
        try:
            import speech_recognition as sr
            import pyttsx3
            
            print("🔧 Initializing speech recognition...")
            # Initialize speech recognition
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            print("🔧 Initializing text-to-speech...")
            # Initialize text-to-speech
            self.tts_engine = pyttsx3.init(driverName='sapi5')  # Use Windows SAPI
            
            # Configure TTS voice
            print("🔧 Configuring voice settings...")
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # Try to use a clear voice (prefer David or Zira)
                for voice in voices:
                    if 'david' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        print(f"   Selected voice: {voice.name}")
                        break
                else:
                    # Use first available voice
                    self.tts_engine.setProperty('voice', voices[0].id)
                    print(f"   Using default voice: {voices[0].name}")
            
            # Set speech rate and volume for clarity
            self.tts_engine.setProperty('rate', 150)  # Slower for clarity
            self.tts_engine.setProperty('volume', 1.0)  # Maximum volume
            
            print("✅ Voice system initialized successfully!")
            
            # Test the voice system
            print("🔊 Testing voice output...")
            self.tts_engine.say("Voice system ready")
            self.tts_engine.runAndWait()
            
            return True
            
        except Exception as e:
            print(f"❌ Error initializing voice system: {e}")
            return False
    
    def initialize(self):
        """Alias for initialize_voice_system for compatibility"""
        return self.initialize_voice_system()
    
    def speak_response(self, text):
        """Alias for speak method for compatibility"""
        return self.speak(text)
    
    def process_voice_command(self, command):
        """Alias for process_user_command for compatibility"""
        return self.process_user_command(command)
    
    def speak(self, text):
        """Make robot speak the given text"""
        if not hasattr(self, 'tts_engine') or self.tts_engine is None:
            print(f"🤖 Sarus: {text}")
            print("   (Voice output not available)")
            return
        
        try:
            print(f"🤖 Sarus: {text}")
            print("   🔊 Speaking...")
            
            self.is_speaking = True
            
            # Clear any previous speech
            self.tts_engine.stop()
            
            # Configure voice settings for clarity
            self.tts_engine.setProperty('rate', 150)  # Slower speech
            self.tts_engine.setProperty('volume', 1.0)  # Max volume
            
            # Speak the text
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            
            self.is_speaking = False
            print("   ✅ Speech completed")
            
        except Exception as e:
            print(f"❌ Speech error: {e}")
            print(f"🤖 Sarus (text only): {text}")
            self.is_speaking = False
    
    def listen_for_speech(self, timeout=5):
        """Listen for user speech input"""
        if not hasattr(self, 'recognizer'):
            return None
        
        try:
            import speech_recognition as sr
            
            print("👂 Listening... (speak now)")
            
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout)
            
            print("🎵 Processing speech...")
            
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You said: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            print("⏰ No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand speech")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
    
    def process_user_command(self, command):
        """Process user voice command and generate response"""
        if not command:
            return "I didn't catch that. Could you please repeat?"
        
        command = command.lower()
        
        # Greeting responses
        if any(word in command for word in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! I'm Sarus, your autonomous lab assistant robot. How can I help you today?"
        
        # Name and identity
        elif any(word in command for word in ['name', 'who are you', 'what are you']):
            return "I'm Sarus, an advanced autonomous lab assistant robot. I can navigate, avoid obstacles, and help with laboratory tasks."
        
        # Capabilities
        elif any(word in command for word in ['what can you do', 'capabilities', 'features']):
            return "I can navigate autonomously, avoid obstacles with my sensors, recognize voice commands, and assist with laboratory tasks. I'm equipped with ultrasonic sensors, a camera, and AI decision-making."
        
        # Movement commands
        elif any(word in command for word in ['move', 'go', 'forward', 'backward']):
            return "I can move in any direction! My 4-wheel drive system and obstacle avoidance keep me safe while navigating."
        
        # Sensors
        elif any(word in command for word in ['sensors', 'see', 'detect']):
            return "I have ultrasonic sensors for obstacle detection, a camera for vision, and wheel encoders for precise movement. My sensors help me navigate safely."
        
        # College/demo specific
        elif any(word in command for word in ['college', 'demo', 'presentation', 'project']):
            return "This is a college demonstration of autonomous robotics! I showcase AI navigation, sensor integration, and voice interaction for educational purposes."
        
        # Technical questions
        elif any(word in command for word in ['how do you work', 'technology', 'ai']):
            return "I use PyBullet physics simulation, computer vision, and AI pathfinding algorithms. My brain runs on Python with real-time sensor processing."
        
        # Fun interactions
        elif any(word in command for word in ['joke', 'funny', 'laugh']):
            return "Why don't robots ever panic? Because they have nerves of steel and circuits of silicon!"
        
        elif any(word in command for word in ['sing', 'song', 'music']):
            return "Beep boop beep! That's my favorite robot song. I'm better at navigation than singing though!"
        
        # Goodbye
        elif any(word in command for word in ['bye', 'goodbye', 'see you', 'exit']):
            return "Goodbye! It was great talking with you. Thanks for checking out my autonomous capabilities!"
        
        # Status and health
        elif any(word in command for word in ['status', 'how are you', 'battery']):
            return "All systems operational! Battery at 98%, sensors active, and ready for any mission you give me."
        
        # Help
        elif any(word in command for word in ['help', 'commands', 'what to say']):
            return "You can ask me about my capabilities, tell me to move, ask about my sensors, or just have a friendly chat! Try asking 'what can you do?' or 'how do you work?'"
        
        # Default response
        else:
            responses = [
                "That's interesting! I'm still learning about that topic. Is there something specific about my robotics capabilities you'd like to know?",
                "I'm not sure about that, but I'd love to tell you about my navigation and sensor systems!",
                "Hmm, that's beyond my current knowledge. Would you like to see a demonstration of my autonomous movement?",
                "I might need more training on that topic! How about asking me about my AI or sensor capabilities?"
            ]
            import random
            return random.choice(responses)
    
    def start_conversation_mode(self):
        """Start interactive conversation with the robot"""
        print("\n🎤 VOICE CONVERSATION WITH SARUS ROBOT")
        print("=" * 50)
        
        # Check dependencies
        missing_deps = self.check_voice_dependencies()
        if missing_deps:
            print(f"❌ Missing voice dependencies: {missing_deps}")
            print("Installing required packages...")
            self.install_voice_dependencies()
            
            # Check again
            missing_deps = self.check_voice_dependencies()
            if missing_deps:
                print("❌ Could not install voice dependencies.")
                print("Falling back to text-based conversation...")
                self.start_text_conversation()
                return
        
        # Initialize voice system
        if not self.initialize_voice_system():
            print("Falling back to text-based conversation...")
            self.start_text_conversation()
            return
        
        # Start voice conversation
        self.speak("Hello! I'm Sarus, your autonomous lab assistant robot. I'm ready to chat!")
        self.speak("You can ask me about my capabilities, tell me to move, or just have a conversation.")
        
        self.conversation_active = True
        conversation_count = 0
        
        while self.conversation_active and conversation_count < 10:  # Limit to prevent infinite loop
            try:
                # Listen for user input
                user_input = self.listen_for_speech(timeout=10)
                
                if user_input:
                    # Process command and respond
                    response = self.process_user_command(user_input)
                    self.speak(response)
                    
                    # Check for exit commands
                    if any(word in user_input for word in ['bye', 'goodbye', 'exit', 'stop']):
                        self.conversation_active = False
                    
                    conversation_count += 1
                else:
                    # No input detected
                    if conversation_count == 0:
                        self.speak("I'm waiting for you to say something. Try saying 'Hello Sarus' or ask me about my capabilities.")
                    else:
                        self.speak("Are you still there? Say something or say 'goodbye' to end our conversation.")
                    
                    conversation_count += 1
                
            except KeyboardInterrupt:
                self.speak("Conversation interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Conversation error: {e}")
                break
        
        if conversation_count >= 10:
            self.speak("That was a great conversation! Thanks for chatting with me.")
        
        print("\n✅ Voice conversation ended!")
    
    def start_text_conversation(self):
        """Fallback text-based conversation"""
        print("\n💬 TEXT CONVERSATION WITH SARUS ROBOT")
        print("=" * 50)
        print("🤖 Sarus: Hello! I'm Sarus, your autonomous lab assistant robot.")
        print("🤖 Sarus: Type your questions or commands. Type 'bye' to exit.")
        print()
        
        conversation_count = 0
        
        while conversation_count < 15:  # Limit conversations
            try:
                user_input = input("👤 You: ").strip()
                
                if not user_input:
                    print("🤖 Sarus: Please type something!")
                    continue
                
                # Process and respond
                response = self.process_user_command(user_input)
                print(f"🤖 Sarus: {response}")
                
                # Check for exit
                if any(word in user_input.lower() for word in ['bye', 'goodbye', 'exit', 'quit']):
                    break
                
                conversation_count += 1
                
            except KeyboardInterrupt:
                print("\n🤖 Sarus: Conversation interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                break
        
        print("\n✅ Text conversation ended!")

def create_voice_demo():
    """Create voice conversation demo"""
    agent = VoiceAgent()
    
    print("🎤 SARUS ROBOT VOICE CONVERSATION DEMO")
    print("=" * 50)
    print("Choose conversation mode:")
    print("1. 🎤 Voice Conversation (with microphone)")
    print("2. 💬 Text Conversation (keyboard input)")
    print("3. 🔧 Install Voice Dependencies")
    print("4. ❌ Back to main menu")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        agent.start_conversation_mode()
    elif choice == "2":
        agent.start_text_conversation()
    elif choice == "3":
        agent.install_voice_dependencies()
    elif choice == "4":
        return
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    create_voice_demo()
