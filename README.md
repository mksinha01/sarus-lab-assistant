# Sarus - AI Lab Assistant Robot (Jarvis + Sarus Integration)

🔬 **Sarus** is an advanced autonomous AI lab assistant that merges the capabilities of Inventor Usman's Mark 1 (Jarvis) with Sarus robotic platform. Built on Raspberry Pi 4, this intelligent robot combines voice interaction, environmental monitoring, safety systems, and autonomous navigation to create a comprehensive lab assistant that can speak, reason, monitor conditions, detect hazards, and assist researchers with human-like proficiency.

## 🌟 Key Features

### 🎤 Voice Interaction & Control
- **Wake Word Detection**: Activated with "Hey Sarus" using Porcupine/VOSK
- **Offline Speech Processing**: Local STT (VOSK/Whisper) + LLaMA LLM + TTS pipeline
- **Intelligent Command Processing**: Natural language understanding for movement and queries
- **Technical Q&A**: Answers math calculations, definitions, and project-related questions
- **Web-Enhanced Knowledge**: Optional API calls for real-time information retrieval

### �️ Safety & Environmental Monitoring
- **Continuous Environmental Monitoring**: DHT22 sensor for temperature and humidity tracking
- **Gas Leak Detection**: MQ-series gas sensors with automatic alert system
- **Safety Protocols**: Autonomous hazard detection with vocal warnings and emergency stops
- **Real-Time Safety Reporting**: Voice-activated environmental status queries

### 🔐 Security & Access Control
- **Facial Recognition**: OpenCV-based user authentication system
- **Authorized User Control**: Only responds to recognized personnel
- **Intruder Detection**: Alerts and logging for unknown individuals
- **Lab Security Monitoring**: Continuous surveillance with intelligent alerts

### 👁️ Computer Vision & Object Recognition
- **Lab Equipment Detection**: YOLO-based identification of multimeters, oscilloscopes, etc.
- **Object Navigation**: Voice-commanded movement to specific equipment
- **Scene Understanding**: LLaVA/BLIP image captioning for descriptive responses
- **Visual Feedback**: LED matrix displays for robot status and emotions

### 🧭 Autonomous Navigation & Mobility
- **Voice-Controlled Movement**: "Move forward," "turn right," "go to the multimeter"
- **Obstacle Avoidance**: Ultrasonic sensors for collision prevention
- **Autonomous Exploration**: Goal-based movement with path learning
- **Manual Override**: Xbox controller for testing and debugging

### � Intelligent Logging & Reporting
- **Mission Summaries**: AI-generated natural language reports after tasks
- **Environmental Data Logging**: Time-series data of temperature, humidity, gas levels
- **Activity Monitoring**: Tracks interactions, observations, and system status
- **Voice Reports**: Spoken summaries of findings and observations

## 🧰 Hardware Requirements

| Component | Purpose | Notes |
|-----------|---------|-------|
| **Core Processing** |
| Raspberry Pi 4 | Main CPU for AI processing | 4GB+ RAM recommended |
| MicroSD Card (64GB+) | OS and model storage | Fast Class 10 or better |
| **Audio System** |
| USB Microphone | Voice input for commands | Noise-canceling preferred |
| USB Speaker/Audio HAT | TTS voice output | Clear audio for responses |
| **Vision & Display** |
| Pi Camera/USB Webcam | Computer vision and monitoring | 1080p or higher |
| LED Matrix Display | Facial animations and status | 8x8 or 16x16 matrix |
| **Environmental Sensors** |
| DHT22 Sensor | Temperature and humidity | ±0.5°C accuracy |
| MQ Gas Sensor (MQ-2/MQ-5) | Gas leak detection | For lab safety monitoring |
| ADC Module (MCP3008) | Analog sensor interface | For gas sensor readings |
| **Mobility & Control** |
| DC Motors + Wheels | Robot locomotion | Encoded motors preferred |
| Motor Driver (L298N) | Motor control interface | H-bridge for bidirectional control |
| Ultrasonic Sensors (HC-SR04) | Obstacle detection | Multiple sensors for 360° coverage |
| Xbox Controller | Manual override control | Wireless USB adapter |
| **Power & Structure** |
| Li-ion Battery Pack | Portable power supply | 5V/3A output minimum |
| 3D Printed Chassis | Physical robot body | Custom design for sensor mounting |
| Jumper Wires & Breadboard | Electronic connections | For prototyping and connections |

## 🧠 Enhanced Software Stack

| System | Technology | Purpose |
|--------|------------|---------|
| **Core OS** |
| Operating System | Raspberry Pi OS Lite | Lightweight Linux distribution |
| **AI & Language Processing** |
| Wake Word Detection | Porcupine/VOSK | "Hey Sarus" activation |
| Speech-to-Text | VOSK/Whisper | Offline voice transcription |
| Language Model (Local) | LLaMA via llama.cpp | Privacy-focused reasoning |
| Language Model (Cloud) | ChatGPT-4/Claude | Fallback for complex queries |
| Text-to-Speech | Coqui/Piper | Natural voice synthesis |
| **Computer Vision** |
| Object Detection | YOLOv5/YOLOv8 | Lab equipment recognition |
| Image Captioning | LLaVA/BLIP | Scene understanding |
| Face Recognition | OpenCV + dlib | User authentication |
| **Environmental Monitoring** |
| Sensor Interface | Adafruit CircuitPython | DHT22, MQ sensors |
| Data Logging | SQLite/InfluxDB | Time-series environmental data |
| Alert System | Custom Python | Real-time hazard detection |
| **Navigation & Control** |
| Motor Control | RPi.GPIO/gpiozero | DC motor driving |
| Path Planning | Custom algorithms | Obstacle avoidance |
| Controller Input | pygame | Xbox controller interface |
| **Safety & Security** |
| Access Control | Custom facial recognition | Authorized user verification |
| Emergency Systems | Hardware interrupts | Immediate safety responses |
| Logging & Audit | JSON/SQLite | Security event tracking |

## 🚀 Quick Start

### Installation

1. **Clone and setup the project**:
   ```bash
   git clone https://github.com/mksinha01/sarus-lab-assistant.git
   cd sarus-lab-assistant
   ```

2. **Install system dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv git cmake build-essential
   sudo apt install portaudio19-dev python3-pyaudio
   ```

3. **Create virtual environment and install Python dependencies**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Configure hardware settings**:
   ```bash
   cp src/config/hardware_config.example.py src/config/hardware_config.py
   # Edit the configuration file to match your hardware setup
   ```

5. **Download AI models**:
   ```bash
   # Download VOSK model for speech recognition
   ./scripts/download_models.sh
   
   # Or manually download and place in data/models/
   ```

6. **Run initial setup and calibration**:
   ```bash
   python setup_calibration.py
   ```

7. **Start Sarus**:
   ```bash
   python main.py
   ```

### Basic Usage Examples

#### 🎤 **Voice Commands**
1. **Wake up Sarus**: Say "Hey Sarus"
2. **Movement commands**:
   - "Move forward"
   - "Turn right" 
   - "Stop"
   - "Go to the multimeter"

3. **Environmental queries**:
   - "What's the lab temperature?"
   - "Check humidity levels"
   - "Any gas leaks detected?"

4. **Technical assistance**:
   - "What is 12 times 7?"
   - "Explain Ohm's law"
   - "What do you see?"

5. **Lab navigation**:
   - "Explore the room"
   - "Find the oscilloscope"
   - "Return to base"

#### 🎮 **Manual Control**
- Use Xbox controller for direct movement during testing
- Override voice commands with manual control
- Emergency stop with controller

#### 📊 **Status Monitoring**
- Check `logs/` directory for mission reports
- View real-time sensor data in web dashboard
- Monitor system health and alerts

## 💬 Example Interactions

### Environmental Monitoring
```
User: "Hey Sarus, what's the lab temperature and humidity?"
Sarus: "Lab temperature is 22°C and humidity is 45%. I detect no hazardous gases."

User: "Set up environmental monitoring for the next hour"
Sarus: "Environmental monitoring activated. I'll alert you if any values exceed safe thresholds."
```

### Safety & Security
```
User: "Sarus, patrol the lab"
Sarus: "Beginning lab patrol. I'll monitor for unauthorized personnel and safety hazards."

[Gas leak detected]
Sarus: "WARNING: Gas leak detected! Levels are above safe threshold. Evacuating area immediately!"
```

### Technical Assistance
```
User: "What's the formula for power calculation?"
Sarus: "Power equals voltage times current, P = V × I. For AC circuits, you may also need to consider power factor."

User: "Calculate the resistance for a 5V supply with 2A current"
Sarus: "Using Ohm's law, R = V/I = 5V/2A = 2.5 ohms."
```

### Object Recognition & Navigation
```
User: "What equipment do you see?"
Sarus: "I can see an oscilloscope on the left bench, a multimeter on the right table, and a power supply unit near the window."

User: "Go to the multimeter"
Sarus: "Navigating to the multimeter on the right table. Avoiding obstacles... Arrived at destination."
```

## 📁 Project Structure

```
sarus-lab-assistant/
├── main.py                     # Main entry point
├── requirements.txt            # Python dependencies
├── setup_calibration.py       # Initial setup and sensor calibration
├── README.md                  # This file
├── scripts/
│   ├── download_models.sh     # Download AI models
│   ├── install_dependencies.sh # System setup script
│   └── deploy_pi.sh          # Raspberry Pi deployment
├── src/
│   ├── core/                  # Core robot systems
│   │   ├── robot.py          # Main robot controller
│   │   ├── state_machine.py  # Robot state management
│   │   └── safety_manager.py # Safety protocols
│   ├── ai/                    # AI and ML modules
│   │   ├── speech/           # STT/TTS systems
│   │   ├── llm/              # Language model interface
│   │   ├── vision/           # Computer vision
│   │   └── voice_agent.py    # Voice conversation system
│   ├── hardware/             # Hardware control
│   │   ├── sensors/          # Environmental sensors
│   │   ├── motors/           # Motor control
│   │   ├── camera/           # Camera interface
│   │   └── display/          # LED matrix control
│   ├── navigation/           # Movement and pathfinding
│   │   ├── path_planner.py   # Route planning
│   │   ├── obstacle_avoidance.py # Collision avoidance
│   │   └── localization.py   # Position tracking
│   ├── safety/               # Safety and security
│   │   ├── gas_monitor.py    # Gas leak detection
│   │   ├── face_recognition.py # User authentication
│   │   └── emergency_stop.py # Emergency protocols
│   ├── communication/        # Voice and network
│   │   ├── voice_interface.py # Voice I/O
│   │   ├── web_dashboard.py  # Web interface
│   │   └── notifications.py  # Alert system
│   ├── config/              # Configuration files
│   │   ├── settings.py      # Main configuration
│   │   ├── hardware_config.py # Hardware pin assignments
│   │   └── ai_config.py     # AI model settings
│   └── utils/               # Utility functions
│       ├── logging.py       # Enhanced logging
│       ├── data_processing.py # Data analysis
│       └── calibration.py   # Sensor calibration
├── data/                    # AI models and datasets
│   ├── models/             # Downloaded AI models
│   ├── voice_samples/      # Training audio
│   ├── face_encodings/     # Authorized user faces
│   └── calibration/        # Sensor calibration data
├── logs/                   # Log files and reports
│   ├── mission_reports/    # Task summaries
│   ├── environmental/      # Sensor data logs
│   ├── security/          # Security events
│   └── system/            # System diagnostics
├── web/                   # Web dashboard files
│   ├── static/            # CSS, JS, images
│   ├── templates/         # HTML templates
│   └── app.py            # Flask web application
├── tests/                 # Unit and integration tests
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── hardware/         # Hardware tests
└── docs/                 # Documentation
    ├── hardware_setup.md # Hardware assembly guide
    ├── software_setup.md # Software installation
    ├── api_reference.md  # API documentation
    └── troubleshooting.md # Common issues and fixes
```

## 🔌 Advanced Features & Extensions

### 🌐 **Connectivity & Remote Access**
- **Wi-Fi Communication** – Remote access via SSH or WebSocket server
- **Web Dashboard** – Live video feed, logs, and control via Flask
- **Mobile App Integration** – Android/iOS app for remote control
- **API Endpoints** – RESTful API for external integrations

### � **Enhanced Security**
- **Multi-Factor Authentication** – Voice + face recognition
- **Encrypted Communications** – Secure data transmission
- **Access Logging** – Detailed audit trails
- **Intruder Deterrent** – Active response to unauthorized access

### 🧪 **Lab-Specific Features**
- **Equipment Interface** – Direct control of lab instruments
- **QR Code Reading** – Sample and equipment identification
- **Chemical Database** – Safety data sheet lookup
- **Experiment Assistance** – Step-by-step procedure guidance

### 🤖 **AI Enhancements**
- **Continuous Learning** – Adaptation to lab environment
- **Predictive Maintenance** – Equipment failure prediction
- **Natural Conversations** – Context-aware dialogue
- **Multi-Language Support** – International lab support

### 🔧 **Developer Features**
- **Plugin System** – Custom Python modules for specialized tasks
- **Model Swapping** – Easy AI model updates
- **Sensor Integration** – Simple addition of new sensors
- **Custom Commands** – User-defined voice commands

## 📄 Use Cases and Target Audience

### 🔬 **Research Laboratories**
- **Automated Experiments** – Voice-controlled instrument operation and data collection
- **Safety Monitoring** – Continuous environmental hazard detection and emergency response
- **Equipment Management** – Intelligent equipment location and status monitoring
- **Data Logging** – Comprehensive environmental and operational data recording
- **Protocol Assistance** – Step-by-step experimental procedure guidance

### 🏫 **Educational Institutions**
- **Student Interaction** – Interactive learning companion for lab safety and procedures
- **Equipment Training** – Voice-guided tutorials for lab equipment operation
- **Safety Education** – Real-time safety monitoring and hazard education
- **Research Support** – Assistance with data collection and analysis
- **Accessibility** – Voice interface for students with mobility limitations

### 🏠 **Makers & Hobbyists**
- **DIY Projects** – Voice-interactive assistant for electronics and robotics projects
- **Workshop Safety** – Environmental monitoring for home workshops
- **Learning Platform** – Hands-on AI and robotics education
- **Privacy-First** – Local processing keeps personal data secure
- **Customizable** – Open-source platform for experimentation

### 👨‍💻 **Developers & Engineers**
- **AI Research Platform** – Test bed for new AI models and algorithms
- **Robotics Development** – Complete robotics stack for prototyping
- **Edge Computing** – Local AI processing optimization and benchmarking
- **Sensor Integration** – Platform for testing new sensor technologies
- **Open Source Contribution** – Community-driven development and improvements

## 🛡️ Safety & Security Protocols

### ⚠️ **Emergency Response Systems**
- **Gas Leak Detection** – Immediate vocal alerts and area evacuation protocols
- **Fire Safety** – Temperature spike detection and emergency notifications
- **Chemical Spill Response** – Automated hazard identification and response procedures
- **Medical Emergency** – Integration with lab emergency systems
- **Hardware Failures** – Fail-safe modes for critical system failures

### 🔐 **Access Control & Security**
- **Multi-Level Authentication** – Face recognition + voice verification
- **Authorized Personnel Database** – Secure storage of approved user profiles
- **Activity Logging** – Complete audit trail of all interactions
- **Intrusion Detection** – Unauthorized access alerts and response
- **Data Encryption** – Secure storage and transmission of sensitive data

### 📊 **Compliance & Monitoring**
- **Environmental Standards** – Continuous monitoring against safety thresholds
- **Usage Analytics** – Equipment utilization and safety metrics
- **Incident Reporting** – Automated generation of safety incident reports
- **Regulatory Compliance** – Support for lab safety regulations and standards
- **Quality Assurance** – System reliability and performance monitoring

## 🚀 Implementation Roadmap

### Phase 1: Core Foundation (Weeks 1-4)
- [x] **Voice conversation system** - Implemented with Gemini AI integration
- [x] **Basic robot simulation** - PyBullet 3D environment ready
- [x] **Custom robot models** - Multiple robot types available
- [ ] **Hardware integration** - Raspberry Pi setup and sensor connections
- [ ] **Basic movement control** - Motor drivers and navigation

### Phase 2: AI & Vision (Weeks 5-8)
- [ ] **Local LLM integration** - LLaMA model deployment
- [ ] **Computer vision setup** - YOLO object detection
- [ ] **Face recognition system** - OpenCV user authentication
- [ ] **Speech processing optimization** - VOSK/Whisper integration
- [ ] **Natural language processing** - Command understanding

### Phase 3: Safety & Monitoring (Weeks 9-12)
- [ ] **Environmental sensors** - DHT22 temperature/humidity monitoring
- [ ] **Gas detection system** - MQ sensor integration and alerts
- [ ] **Safety protocols** - Emergency response procedures
- [ ] **Data logging system** - Environmental and operational data
- [ ] **Alert mechanisms** - Voice and visual warning systems

### Phase 4: Advanced Features (Weeks 13-16)
- [ ] **Web dashboard** - Remote monitoring and control interface
- [ ] **Mobile app integration** - Smartphone control capabilities
- [ ] **Advanced navigation** - SLAM and path planning
- [ ] **Lab equipment integration** - Direct instrument control
- [ ] **Machine learning optimization** - Performance improvements

### Phase 5: Testing & Deployment (Weeks 17-20)
- [ ] **Comprehensive testing** - Unit, integration, and field testing
- [ ] **Documentation completion** - User guides and API documentation
- [ ] **Performance optimization** - Speed and reliability improvements
- [ ] **Security auditing** - Penetration testing and vulnerability assessment
- [ ] **Production deployment** - Final system rollout and training

## 🛠️ Development & Configuration

### Testing
```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/unit/          # Unit tests
python -m pytest tests/integration/   # Integration tests
python -m pytest tests/hardware/      # Hardware tests

# Test voice system
python tests/voice_system_test.py

# Test safety systems
python tests/safety_test.py
```

### Configuration
Edit configuration files to customize behavior:

#### `src/config/settings.py` - Main Configuration
```python
# AI Model Settings
AI_MODEL_LOCAL = "llama-7b"
AI_MODEL_CLOUD = "gpt-4"
VOICE_WAKE_WORD = "hey sarus"

# Safety Thresholds
MAX_TEMPERATURE = 35.0  # Celsius
MAX_HUMIDITY = 80.0     # Percentage
GAS_ALARM_THRESHOLD = 400  # PPM

# Navigation Settings
MAX_SPEED = 0.5  # m/s
OBSTACLE_DISTANCE = 0.3  # meters
```

#### `src/config/hardware_config.py` - Hardware Pin Assignments
```python
# Motor Control Pins
MOTOR_LEFT_PWM = 18
MOTOR_LEFT_DIR1 = 24
MOTOR_LEFT_DIR2 = 25

# Sensor Pins
DHT22_PIN = 4
GAS_SENSOR_PIN = 0  # ADC channel
ULTRASONIC_TRIG = 23
ULTRASONIC_ECHO = 24

# LED Matrix
LED_MATRIX_DIN = 19
LED_MATRIX_CS = 8
LED_MATRIX_CLK = 11
```

### Adding New Features

#### 1. **New Sensor Integration**
```python
# Create sensor class in src/hardware/sensors/
class NewSensor:
    def __init__(self, pin):
        self.pin = pin
    
    def read(self):
        # Sensor reading logic
        return value

# Register in main robot controller
from src.hardware.sensors.new_sensor import NewSensor
robot.add_sensor("new_sensor", NewSensor(pin=22))
```

#### 2. **Custom Voice Commands**
```python
# Add to src/ai/voice_agent.py
def process_custom_command(self, command):
    if "custom action" in command.lower():
        return "Executing custom action"
    return None
```

#### 3. **New Safety Protocols**
```python
# Add to src/safety/safety_manager.py
def check_custom_safety(self):
    if self.custom_sensor.read() > threshold:
        self.trigger_alert("Custom safety alert!")
        return False
    return True
```

### Performance Optimization

#### **Model Quantization**
```bash
# Quantize LLaMA model for faster inference
python scripts/quantize_model.py --model llama-7b --output models/llama-7b-q4
```

#### **Memory Management**
```python
# Configure memory usage in src/config/ai_config.py
MODEL_MAX_MEMORY = "4GB"
CACHE_SIZE = 1000
BATCH_SIZE = 1
```

#### **CPU Optimization**
```bash
# Enable GPU acceleration (if available)
sudo apt install nvidia-cuda-toolkit
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

## 📚 Documentation & Resources

### 📖 **User Guides**
- [Hardware Assembly Guide](docs/hardware_setup.md) - Step-by-step hardware setup
- [Software Installation](docs/software_setup.md) - Complete software setup process  
- [Voice Command Reference](docs/voice_commands.md) - All available voice commands
- [Safety Procedures](docs/safety_guide.md) - Emergency protocols and safety features

### 🔧 **Developer Resources**
- [API Reference](docs/api_reference.md) - Complete API documentation
- [Architecture Overview](docs/architecture.md) - System design and components
- [Contributing Guidelines](CONTRIBUTING.md) - How to contribute to the project
- [Troubleshooting Guide](docs/troubleshooting.md) - Common issues and solutions

### 🌐 **Community & Support**
- **GitHub Issues** - Bug reports and feature requests
- **Discussions** - Community support and Q&A
- **Wiki** - Community-maintained documentation
- **Discord Server** - Real-time chat and support

## 📝 License & Legal

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses
- YOLO models: GPL-3.0 License
- LLaMA models: Custom License (see model documentation)
- OpenCV: Apache 2.0 License
- Raspberry Pi OS: Various open-source licenses

### Privacy & Data Protection
- **Local Processing**: All sensitive data processed on-device
- **No Cloud Storage**: Personal data never leaves the device
- **Encrypted Storage**: User profiles and sensitive data encrypted
- **GDPR Compliant**: Full user control over personal data

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Ways to Contribute
- 🐛 **Bug Reports** - Report issues and bugs
- ✨ **Feature Requests** - Suggest new features
- 💻 **Code Contributions** - Submit pull requests
- 📚 **Documentation** - Improve docs and guides
- 🧪 **Testing** - Help test new features
- 🎨 **Design** - UI/UX improvements for web dashboard

### Development Setup
```bash
# Fork the repository
git clone https://github.com/yourusername/sarus-lab-assistant.git
cd sarus-lab-assistant

# Create development branch
git checkout -b feature/your-feature-name

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests before submitting
python -m pytest tests/
```

---

## 🎯 **Project Vision**

*Sarus represents the future of intelligent lab assistance - where AI, robotics, and safety converge to create a truly autonomous lab companion. By combining the conversational intelligence of Jarvis with the mobility and sensors of Sarus, we're building a robot that doesn't just follow commands, but understands, reasons, and actively contributes to safer, more efficient laboratory environments.*

**Sarus - Making labs smarter, safer, and more interactive, one conversation at a time** 🤖✨

---

*For the latest updates, documentation, and community discussions, visit our [GitHub repository](https://github.com/mksinha01/sarus-lab-assistant).*
