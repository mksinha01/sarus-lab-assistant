# Sarus Robot - Project Documentation

## 📁 Project Structure

```
sarus-robot/
├── src/                          # Main source code
│   ├── ai/                       # AI and ML components
│   │   ├── speech_manager.py     # Speech recognition & synthesis
│   │   ├── llm_manager.py        # Large Language Model interface
│   │   └── vision_manager.py     # Computer vision & object detection
│   ├── core/                     # Core robot functionality
│   │   └── robot.py              # Main robot controller
│   ├── hardware/                 # Hardware control modules
│   │   ├── motor_controller.py   # Motor control (L298N)
│   │   ├── sensor_manager.py     # Sensor management (ultrasonic, etc.)
│   │   └── display_controller.py # LED/OLED display control
│   ├── navigation/               # Navigation and movement
│   │   └── navigation_manager.py # Autonomous navigation logic
│   ├── communication/            # Communication interfaces
│   │   └── voice_interface.py    # Voice interaction coordinator
│   ├── utils/                    # Utility modules
│   │   ├── logger.py             # Logging system
│   │   ├── state_manager.py      # State management
│   │   └── mission_logger.py     # Mission logging
│   └── config/                   # Configuration files
│       ├── settings.py           # Main configuration
│       └── hardware_config.py    # Hardware-specific settings
├── main.py                       # Application entry point
├── start_sarus.py               # Quick start script
├── test_components.py           # Component testing suite
├── requirements.txt             # Python dependencies
├── setup.sh                     # Automated setup script
├── README.md                    # Main documentation
├── INSTALLATION.md              # Installation guide
└── docs/                        # Additional documentation
```

## 🏗️ Architecture Overview

### Core Components

1. **SarusRobot** (`src/core/robot.py`)
   - Central robot controller
   - Coordinates all subsystems
   - Manages robot state and lifecycle
   - Handles main operation loop
   mkmk

2. **AI Managers**
   - **SpeechManager**: Speech-to-text, text-to-speech, wake word detection
   - **LLMManager**: Local and cloud LLM integration (Ollama, OpenAI)
   - **VisionManager**: Computer vision, scene analysis, object detection

3. **Hardware Controllers**
   - **MotorController**: L298N motor driver control, movement patterns
   - **SensorManager**: Ultrasonic sensors, environmental monitoring
   - **DisplayController**: LED matrix expressions, status indicators

4. **Navigation System**
   - **NavigationManager**: Autonomous movement, path planning, exploration

5. **Communication**
   - **VoiceInterface**: Coordinates voice-based interactions

### Data Flow

```
Voice Input → SpeechManager → LLMManager → ActionPlanning
                ↓                              ↓
          SarusRobot ← NavigationManager ← Hardware Control
                ↓                              ↓
        VisionManager → Scene Analysis → Object Detection
```

## 🔧 Hardware Integration

### Supported Hardware
- **Raspberry Pi 4** (4GB+ recommended)
- **L298N Motor Driver** for dual DC motors
- **HC-SR04 Ultrasonic Sensors** (front, left, right)
- **LED Matrix Display** for expressions
- **Camera Module** for computer vision
- **USB Audio** for voice interaction
- **Xbox/PS4 Controller** for manual control

### GPIO Pin Configuration
Default GPIO assignments (BCM numbering):
- Motors: Pins 12, 13, 18-21
- Ultrasonic: Pins 1, 7, 8, 23-25
- Display: Pins 9-11
- Status LEDs: Pins 6, 16, 26

## 🤖 AI Integration

### Local AI Models
- **Whisper**: Speech recognition (offline capable)
- **Ollama + LLaMA**: Local language model processing
- **YOLO/OpenCV**: Object detection and scene analysis
- **Porcupine**: Wake word detection

### Cloud AI Fallback
- **OpenAI GPT**: Advanced language processing
- **Cloud STT/TTS**: Backup speech services

## 🎮 Operation Modes

1. **Interactive Mode**: Voice-controlled operation
2. **Exploration Mode**: Autonomous environment exploration
3. **Manual Mode**: Gamepad-controlled movement
4. **Simulation Mode**: Software testing without hardware
5. **Test Mode**: Component validation and diagnostics

## 🛡️ Safety Features

- **Emergency Stop**: Immediate halt of all movement
- **Obstacle Detection**: Automatic collision avoidance
- **Battery Monitoring**: Low power warnings and safe shutdown
- **Movement Limits**: Speed and duration constraints
- **Failsafe Modes**: Graceful degradation when components fail

## 📊 State Management

### Robot States
- `IDLE`: Waiting for commands
- `LISTENING`: Processing voice input
- `THINKING`: AI processing
- `MOVING`: Physical movement
- `EXPLORING`: Autonomous exploration
- `ERROR`: Error recovery mode
- `SHUTDOWN`: Safe shutdown sequence

### Mission Logging
All robot activities are logged including:
- Voice interactions and commands
- Movement patterns and navigation decisions
- Object detection and scene analysis
- Error conditions and recovery actions
- Performance metrics and system status

## 🔄 Development Workflow

### Testing Strategy
1. **Unit Tests**: Individual component validation
2. **Integration Tests**: Multi-component interactions
3. **Simulation Tests**: Full robot behavior without hardware
4. **Hardware Tests**: Real-world validation

### Debugging Tools
- **Component Tester**: `test_components.py`
- **Simulation Mode**: Hardware-free testing
- **Verbose Logging**: Detailed system diagnostics
- **Mission Logs**: Historical activity tracking

## 🚀 Deployment

### Development Environment
```bash
python start_sarus.py --mode simulation
```

### Production Deployment
```bash
python start_sarus.py --mode interactive
```

### Service Installation (Optional)
```bash
# Create systemd service for auto-start
sudo cp scripts/sarus.service /etc/systemd/system/
sudo systemctl enable sarus
```

## 🔧 Customization

### Adding New Hardware
1. Update GPIO pin configuration in `hardware_config.py`
2. Create new controller in `src/hardware/`
3. Integrate with main robot controller
4. Add component tests

### Adding New AI Models
1. Implement model interface in appropriate AI manager
2. Add model configuration to settings
3. Update fallback logic
4. Test with simulation mode

### Creating Custom Behaviors
1. Add new methods to `SarusRobot` class
2. Implement in `NavigationManager` or AI managers
3. Add voice commands to `VoiceInterface`
4. Update mission logging

## 📈 Performance Optimization

### Memory Management
- Use appropriate model sizes for hardware
- Implement model caching
- Monitor memory usage during operation

### Processing Optimization
- Async/await for non-blocking operations
- Hardware acceleration where available
- Efficient sensor polling

### Battery Life
- Dynamic performance scaling
- Sleep modes during idle periods
- Low-power sensor configurations

## 🔐 Security Considerations

### Network Security
- Local-first AI processing
- Encrypted connections for cloud services
- Secure API key management

### Physical Security
- Emergency stop mechanisms
- Movement boundary enforcement
- Safe operating parameters

## 📚 Additional Resources

- **API Documentation**: Auto-generated from docstrings
- **Hardware Guides**: Wiring diagrams and setup instructions
- **Troubleshooting**: Common issues and solutions
- **Community**: Discord server and GitHub discussions

---

**Built with ❤️ for the maker community**
