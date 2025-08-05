# Hardware Configuration Template for Sarus Robot

"""
Copy this file to hardware_config.py and customize for your specific hardware setup.
This allows you to override default GPIO pin assignments and hardware settings
without modifying the main configuration files.
"""

# GPIO Pin Assignments (Raspberry Pi BCM numbering)
CUSTOM_GPIO_PINS = {
    # Motor controller (L298N)
    "motor_left_forward": 18,
    "motor_left_backward": 19,
    "motor_right_forward": 20,
    "motor_right_backward": 21,
    "motor_left_enable": 12,
    "motor_right_enable": 13,
    
    # Ultrasonic sensors (HC-SR04)
    "ultrasonic_front_trigger": 23,
    "ultrasonic_front_echo": 24,
    "ultrasonic_left_trigger": 25,
    "ultrasonic_left_echo": 8,
    "ultrasonic_right_trigger": 7,
    "ultrasonic_right_echo": 1,
    
    # LED matrix display (optional)
    "led_matrix_data": 10,
    "led_matrix_clock": 11,
    "led_matrix_latch": 9,
    
    # Status LEDs
    "status_led_red": 16,
    "status_led_green": 26,
    "status_led_blue": 6,
}

# Hardware-specific settings
HARDWARE_CONFIG = {
    # Enable/disable hardware components
    "hardware_enabled": True,
    
    # Camera settings
    "camera_device": 0,  # USB camera index or Pi camera
    "camera_resolution": (640, 480),
    "camera_fps": 30,
    
    # Motor settings
    "max_speed": 0.8,  # Maximum motor speed (0.0 to 1.0)
    "turn_speed": 0.6,  # Turn speed
    
    # Sensor settings
    "obstacle_distance_threshold": 30,  # cm
    "emergency_stop_distance": 10,  # cm
    
    # Display settings
    "display_type": "led_matrix",  # "led_matrix", "oled", "none"
    "display_brightness": 128,
    
    # Controller settings
    "controller_enabled": True,
    "controller_deadzone": 0.1,
}

# Audio device settings (if using specific audio hardware)
AUDIO_CONFIG = {
    # Audio input/output device indices
    # Use `python -m pyaudio` to list available devices
    "input_device_index": None,  # None for default
    "output_device_index": None,  # None for default
    
    # Audio settings
    "sample_rate": 16000,
    "chunk_size": 1024,
    "channels": 1,
}

# AI model preferences for this hardware
AI_CONFIG = {
    # Local model preferences (adjust based on Pi performance)
    "llm_model_local": "llama3.2:1b",  # Smaller model for Pi 4
    "stt_model": "tiny",  # Whisper tiny model for faster processing
    "vision_model": "yolo",  # YOLO for better Pi performance
    
    # Processing timeouts (adjust for Pi performance)
    "llm_timeout": 45.0,  # Longer timeout for Pi
    "stt_timeout": 8.0,
    
    # Resource limits
    "llm_max_tokens": 300,  # Shorter responses for faster generation
}

# Network settings (for remote control/monitoring)
NETWORK_CONFIG = {
    "web_dashboard_enabled": False,
    "web_dashboard_port": 8080,
    "websocket_enabled": False,
    "websocket_port": 8081,
    
    # Remote access
    "ssh_enabled": True,
    "vnc_enabled": False,
}

# Apply this configuration by importing in your main config:
# from hardware_config import CUSTOM_GPIO_PINS, HARDWARE_CONFIG
# SYSTEM_CONFIG['gpio_pins'].update(CUSTOM_GPIO_PINS)
# SYSTEM_CONFIG.update(HARDWARE_CONFIG)
