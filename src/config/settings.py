"""
⚙️ SARUS ROBOT CONFIGURATION SETTINGS
Main configuration file for Sarus AI Lab Assistant Robot (Jarvis + Sarus Integration)
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Config:
    """Main configuration class for Sarus robot"""
    
    # Project paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    LOGS_DIR: Path = PROJECT_ROOT / "logs"
    MODELS_DIR: Path = DATA_DIR / "models"
    
    # AI Model Settings
    AI_MODEL_LOCAL: str = "llama-7b"
    AI_MODEL_CLOUD: str = "gpt-4"
    VOICE_WAKE_WORD: str = "hey sarus"
    
    # Voice System Settings
    STT_MODEL: str = "vosk"  # vosk, whisper
    TTS_ENGINE: str = "pyttsx3"  # pyttsx3, coqui
    VOICE_TIMEOUT: int = 5
    VOICE_RATE: int = 150
    VOICE_VOLUME: float = 1.0
    
    # Safety Thresholds
    MAX_TEMPERATURE: float = 35.0  # Celsius
    MAX_HUMIDITY: float = 80.0     # Percentage
    GAS_ALARM_THRESHOLD: int = 400  # PPM
    
    # Navigation Settings
    MAX_SPEED: float = 0.5  # m/s
    OBSTACLE_DISTANCE: float = 0.3  # meters
    TURN_SPEED: float = 0.3
    
    # Hardware Pins (Raspberry Pi GPIO)
    # Motor Control Pins
    MOTOR_LEFT_PWM: int = 18
    MOTOR_LEFT_DIR1: int = 24
    MOTOR_LEFT_DIR2: int = 25
    MOTOR_RIGHT_PWM: int = 19
    MOTOR_RIGHT_DIR1: int = 26
    MOTOR_RIGHT_DIR2: int = 27
    
    # Sensor Pins
    DHT22_PIN: int = 4
    GAS_SENSOR_PIN: int = 0  # ADC channel
    ULTRASONIC_TRIG: int = 23
    ULTRASONIC_ECHO: int = 24
    
    # LED Matrix Pins
    LED_MATRIX_DIN: int = 19
    LED_MATRIX_CS: int = 8
    LED_MATRIX_CLK: int = 11
    
    # Camera Settings
    CAMERA_WIDTH: int = 640
    CAMERA_HEIGHT: int = 480
    CAMERA_FPS: int = 30
    
    # Web Dashboard
    WEB_HOST: str = "0.0.0.0"
    WEB_PORT: int = 5000
    WEB_DEBUG: bool = False
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Security Settings
    FACE_RECOGNITION_TOLERANCE: float = 0.6
    MAX_FAILED_ATTEMPTS: int = 3
    SECURITY_LOCKOUT_TIME: int = 300  # seconds
    
    # Environmental Monitoring
    SENSOR_READ_INTERVAL: float = 1.0  # seconds
    LOG_INTERVAL: float = 60.0  # seconds
    ALERT_COOLDOWN: float = 30.0  # seconds
    
    # Simulation Settings (for development/testing)
    SIMULATION_MODE: bool = True  # Set to False for real hardware
    PYBULLET_GUI: bool = True
    
    def __post_init__(self):
        """Initialize and validate configuration"""
        # Create necessary directories
        self.DATA_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)
        self.MODELS_DIR.mkdir(exist_ok=True)
        
        # Create log subdirectories
        (self.LOGS_DIR / "mission_reports").mkdir(exist_ok=True)
        (self.LOGS_DIR / "environmental").mkdir(exist_ok=True)
        (self.LOGS_DIR / "security").mkdir(exist_ok=True)
        (self.LOGS_DIR / "system").mkdir(exist_ok=True)

# Legacy settings for backward compatibility
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
MODELS_DIR = DATA_DIR / "models"
AUDIO_DIR = DATA_DIR / "audio"

# Ensure directories exist
for directory in [DATA_DIR, LOGS_DIR, MODELS_DIR, AUDIO_DIR]:
    directory.mkdir(exist_ok=True)

# System Configuration
SYSTEM_CONFIG = {
    # General settings
    "robot_name": "Sarus",
    "version": "1.0.0",
    "debug_mode": True,
    "hardware_enabled": True,  # Set to False for development without hardware
    
    # Wake word settings
    "wake_word": "hey sarus",
    "wake_word_sensitivity": 0.5,
    "wake_word_model": "porcupine",  # or "vosk"
    
    # Audio settings
    "sample_rate": 16000,
    "chunk_size": 1024,
    "channels": 1,
    "audio_format": "int16",
    
    # Speech recognition
    "stt_engine": "whisper",  # "whisper", "vosk", or "openai"
    "stt_model": "base",  # For Whisper: "tiny", "base", "small", "medium", "large"
    "stt_language": "en",
    "stt_timeout": 5.0,
    
    # Text-to-speech
    "tts_engine": "pyttsx3",  # "pyttsx3", "coqui", "piper"
    "tts_voice_rate": 150,
    "tts_voice_volume": 0.8,
    "tts_voice_id": 0,  # System voice ID
    
    # LLM settings
    "llm_primary": "gemini",  # "gemini", "ollama", "openai"
    "llm_fallback": "ollama",
    "llm_model_local": "llama3.2:3b",  # Ollama model
    "llm_model_cloud": "gemini-1.5-flash",  # Gemini model
    "llm_model_openai": "gpt-4o-mini",  # OpenAI model
    "llm_max_tokens": 500,
    "llm_temperature": 0.7,
    "llm_timeout": 30.0,
    
    # Computer vision
    "vision_model": "llava",  # "llava", "yolo", "custom"
    "vision_confidence_threshold": 0.5,
    "camera_resolution": (640, 480),
    "camera_fps": 30,
    "camera_device": 0,  # Camera device index
    
    # Navigation settings
    "max_speed": 0.8,  # Motor speed (0.0 to 1.0)
    "turn_speed": 0.6,
    "obstacle_distance_threshold": 30,  # cm
    "navigation_update_rate": 10,  # Hz
    "exploration_duration": 300,  # seconds (5 minutes)
    
    # Hardware pin assignments (Raspberry Pi GPIO)
    "gpio_pins": {
        # Motor controller (L298N)
        "motor_left_forward": 18,
        "motor_left_backward": 19,
        "motor_right_forward": 20,
        "motor_right_backward": 21,
        "motor_left_enable": 12,
        "motor_right_enable": 13,
        
        # Ultrasonic sensors
        "ultrasonic_front_trigger": 23,
        "ultrasonic_front_echo": 24,
        "ultrasonic_left_trigger": 25,
        "ultrasonic_left_echo": 8,
        "ultrasonic_right_trigger": 7,
        "ultrasonic_right_echo": 1,
        
        # LED matrix display
        "led_matrix_data": 10,
        "led_matrix_clock": 11,
        "led_matrix_latch": 9,
        
        # Status LEDs
        "status_led_red": 16,
        "status_led_green": 26,
        "status_led_blue": 6,
    },
    
    # Display settings
    "display_type": "led_matrix",  # "led_matrix", "oled", "none"
    "display_width": 8,
    "display_height": 8,
    "display_brightness": 128,
    
    # Xbox controller settings
    "controller_enabled": True,
    "controller_deadzone": 0.1,
    "controller_mapping": {
        "move_forward": "left_stick_up",
        "move_backward": "left_stick_down",
        "turn_left": "left_stick_left",
        "turn_right": "left_stick_right",
        "emergency_stop": "start_button",
        "voice_trigger": "a_button",
    },
    
    # API keys (use environment variables for security)
    "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
    "porcupine_access_key": os.getenv("PORCUPINE_ACCESS_KEY", ""),
    
    # Logging settings
    "log_level": "INFO",
    "log_file_max_size": 10 * 1024 * 1024,  # 10MB
    "log_backup_count": 5,
    "mission_log_enabled": True,
    
    # Safety settings
    "emergency_stop_distance": 10,  # cm
    "max_continuous_movement_time": 30,  # seconds
    "battery_low_threshold": 20,  # percentage
    "temperature_warning_threshold": 70,  # Celsius
}

# AI Prompts and responses
AI_PROMPTS = {
    "system_prompt": """You are Sarus, an intelligent lab assistant robot. You help in laboratory environments by:
- Responding to voice commands
- Describing what you see through your camera
- Moving safely through the lab
- Identifying lab equipment and objects
- Providing assistance to students and researchers

Keep responses concise, friendly, and helpful. Always prioritize safety.""",
    
    "exploration_prompt": """You are exploring a laboratory environment. Describe what you observe, 
including any equipment, people, or notable features. Be specific but concise.""",
    
    "movement_prompt": """Analyze this movement command and provide the appropriate action. 
Respond with just the action needed: forward, backward, left, right, stop, or explore.""",
    
    "error_responses": [
        "I'm sorry, I didn't understand that command.",
        "Could you please repeat that?",
        "I'm having trouble processing your request.",
        "Please try again with a different command."
    ],
    
    "greeting_responses": [
        "Hello! I'm Sarus, your lab assistant. How can I help you today?",
        "Hi there! Ready to explore the lab together?",
        "Greetings! I'm here to assist you in the laboratory."
    ]
}

# Hardware specifications for different setups
HARDWARE_PROFILES = {
    "development": {
        "hardware_enabled": False,
        "camera_device": None,
        "gpio_pins": {},
        "controller_enabled": False,
    },
    
    "raspberry_pi_4": {
        "hardware_enabled": True,
        "camera_device": 0,
        "gpio_pins": SYSTEM_CONFIG["gpio_pins"],
        "controller_enabled": True,
    },
    
    "jetson_nano": {
        "hardware_enabled": True,
        "camera_device": 0,
        "gpio_pins": SYSTEM_CONFIG["gpio_pins"],
        "controller_enabled": True,
        "gpu_acceleration": True,
    }
}

def get_config(profile: str = "development") -> dict:
    """
    Get configuration for specific hardware profile
    
    Args:
        profile: Hardware profile name ("development", "raspberry_pi_4", "jetson_nano")
    
    Returns:
        Combined configuration dictionary
    """
    config = SYSTEM_CONFIG.copy()
    
    if profile in HARDWARE_PROFILES:
        config.update(HARDWARE_PROFILES[profile])
    
    return config

def update_config(updates: dict):
    """
    Update system configuration at runtime
    
    Args:
        updates: Dictionary of configuration updates
    """
    SYSTEM_CONFIG.update(updates)
