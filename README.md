# Sarus - Autonomous AI-Powered Lab Assistant Robot

🔬 **Sarus** is an intelligent robotic lab assistant powered by multiple AI models, including an offline LLaMA-based LLM, real-time speech-to-text and text-to-speech systems, and a computer vision model. Built on a Raspberry Pi 4, Sarus is designed to help in lab environments by interacting through voice, exploring autonomously, navigating based on object recognition, and logging its journey.

## 🌟 Key Features

### 🎤 Communication & Control
- **Wake Word Detection**: Activated with "Hey Sarus," avoiding unnecessary triggers
- **Voice Interaction**: Real-time conversation using STT + LLM + TTS pipeline
- **Manual Control**: Controlled with an Xbox controller for testing/debugging
- **Spoken Movement Commands**: Recognizes phrases like "move forward" or "turn right"

### 📺 Visual Feedback
- **Facial Display**: Dynamic face/mouth animations to show listening, idle, or processing states
- **State Indicators**: LED/mouth display blinks during listening, thinking, and responses

### 🤖 Intelligence Engine
- **Multiple AI Backends**:
  - 🔁 Offline LLaMA for privacy-focused conversation
  - 🌐 ChatGPT (fallback or benchmark)
  - 👁 LLaVA or custom vision model for image understanding
- **Real-Time Response**: Transcribes audio → AI inference → Speech output

### 🧭 Navigation & Perception
- **Environmental Awareness**: Camera-based scene understanding and description
- **Object Navigation**: Can recognize and move toward objects intelligently
- **Obstacle Avoidance**: Detects and avoids objects using sensor data
- **Autonomous Exploration**: Randomized or goal-based movement with path learning
- **Optional SLAM**: 2D/3D mapping integration

### 📋 Logging & Reporting
- **Mission Reports**: Generates voice or text summary after exploration
- **Real-Time Logs**: Stores direction, object detection logs, obstacle data
- **Map Generation**: Potential to create 2D map using SLAM-compatible frameworks

## 🧰 Hardware Requirements

| Component | Purpose |
|-----------|---------|
| Raspberry Pi 4 | Core processing unit |
| Pi Camera or USB Cam | Vision and environment perception |
| Mic & Speaker | Voice input/output |
| OLED or LED Matrix | Facial animation display |
| Xbox Controller | Manual movement (wired/wireless) |
| Motor Driver (L298N) | Driving motors |
| DC Motors + Wheels | Locomotion |
| Ultrasonic Sensors | Obstacle detection |
| Li-ion Battery Pack | Portable power supply |
| 3D Printed Chassis | Physical body |

## 🧠 Software Stack

| System | Technology Used |
|--------|----------------|
| OS | Raspberry Pi OS Lite (or Ubuntu Lite) |
| Wake Word | Porcupine / Vosk Wakeword |
| STT | Whisper / Vosk |
| TTS | Coqui / Piper / pyttsx3 |
| LLM (Local) | LLaMA via Ollama or llama.cpp |
| LLM (Cloud) | ChatGPT (fallback) |
| Vision Model | LLaVA or YOLO + Captioning Model |
| Display | Python-based LED matrix controller |
| Controller | Xbox Controller with pygame or inputs lib |
| Navigation | Custom logic + OpenCV + SLAM (optional) |
| Logging | SQLite/JSON + simple 2D map generator |

## 🚀 Quick Start

### Installation

1. **Clone and setup the project**:
   ```bash
   git clone <repository-url>
   cd sarus-robot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure hardware settings**:
   ```bash
   cp src/config/hardware_config.example.py src/config/hardware_config.py
   # Edit the configuration file to match your hardware setup
   ```

4. **Run Sarus**:
   ```bash
   python main.py
   ```

### Basic Usage

1. **Wake up Sarus**: Say "Hey Sarus"
2. **Give commands**:
   - "Move forward"
   - "Turn right"
   - "What do you see?"
   - "Explore the room"
   - "Go to the multimeter"

3. **Manual control**: Use Xbox controller for direct movement
4. **View logs**: Check `logs/` directory for mission reports

## 📁 Project Structure

```
sarus-robot/
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/
│   ├── core/              # Core robot systems
│   ├── ai/                # AI modules (STT, TTS, LLM, Vision)
│   ├── hardware/          # Hardware control
│   ├── navigation/        # Movement and navigation
│   ├── communication/     # Voice and display
│   ├── config/           # Configuration files
│   └── utils/            # Utility functions
├── logs/                 # Log files and mission reports
├── data/                 # AI models and training data
├── tests/               # Unit tests
└── docs/                # Documentation
```

## 🔌 Extensions

- 📡 **Wi-Fi Communication** – Remote access via SSH or WebSocket server
- 🌍 **Web Dashboard** – Live video, logs, and control via Flask
- 🕵️ **Security Mode** – Intruder detection using facial recognition
- 📚 **Lab Data Assistant** – Reads labels, QR codes, or texts from samples
- 📦 **Plugin System** – Custom Python modules for specialized tasks
- 🎮 **Mobile App** – Android app controller
- 🔐 **Facial Recognition** – Only responds to authorized personnel
- 🧭 **Advanced SLAM** – Indoor navigation with path memory

## 📄 Usage Scenarios

### In a College Lab
- Sarus listens for student queries and helps navigate lab equipment
- Explains what objects it sees: "I see an oscilloscope to the left"
- After exploring: "I explored the lab. I saw 3 computers, 2 students, and one whiteboard"
- Navigation: "Sarus, go to the multimeter" → navigates safely and stops before collision

### Research Laboratory
- Assists with equipment identification and location
- Provides voice-controlled movement for hands-free operation
- Logs environmental conditions and equipment status
- Generates reports of lab activities and observations

## 🛠️ Development

### Testing
```bash
python -m pytest tests/
```

### Configuration
Edit `src/config/settings.py` to customize:
- AI model preferences
- Hardware pin assignments
- Voice recognition sensitivity
- Navigation parameters

### Adding New Features
1. Create module in appropriate `src/` subdirectory
2. Add configuration options to `src/config/`
3. Update main robot controller in `src/core/robot.py`
4. Add tests in `tests/`

## 📝 License

This project is open source. See LICENSE file for details.

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

---

*Sarus - Making labs smarter, one conversation at a time* 🤖✨
