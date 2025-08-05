# Sarus Robot - Installation and Setup Guide

Welcome to Sarus, your autonomous AI-powered lab assistant robot! This guide will help you get Sarus up and running on your Raspberry Pi 4.

## 📋 Prerequisites

### Hardware Requirements
- **Raspberry Pi 4** (4GB RAM recommended, 8GB preferred)
- **MicroSD Card** (32GB minimum, Class 10)
- **Motor Driver**: L298N dual H-bridge motor controller
- **Motors**: 2x DC geared motors with wheels
- **Sensors**: 3x HC-SR04 ultrasonic sensors (front, left, right)
- **Display**: LED matrix or OLED display (optional)
- **Camera**: Raspberry Pi Camera Module v2 or USB webcam
- **Audio**: USB microphone and speaker/headphones
- **Power**: Battery pack (7.4V-12V) or power supply
- **Controller**: Xbox/PS4 controller (optional)

### Software Requirements
- **OS**: Raspberry Pi OS (64-bit recommended)
- **Python**: 3.8+ (included with Pi OS)
- **Internet**: For AI model downloads and updates

## 🚀 Quick Installation

### Option 1: Automated Setup (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/sarus-robot.git
cd sarus-robot

# Run the setup script
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Installation

#### 1. System Updates
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git
```

#### 2. Clone Repository
```bash
git clone https://github.com/yourusername/sarus-robot.git
cd sarus-robot
```

#### 3. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4. Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt

# Install system packages for GPIO
sudo apt install -y python3-gpiozero python3-rpi.gpio

# Install audio dependencies
sudo apt install -y portaudio19-dev python3-pyaudio espeak-ng

# Install computer vision dependencies
sudo apt install -y python3-opencv libopencv-dev

# Install Ollama for local LLM
curl -fsSL https://ollama.ai/install.sh | sh
```

#### 5. Hardware Setup

##### GPIO Connections (using BCM numbering):
```
Motor Controller (L298N):
- ENA → GPIO 12 (PWM)
- IN1 → GPIO 18
- IN2 → GPIO 19
- ENB → GPIO 13 (PWM)
- IN3 → GPIO 20
- IN4 → GPIO 21

Ultrasonic Sensors (HC-SR04):
Front Sensor:
- Trigger → GPIO 23
- Echo → GPIO 24

Left Sensor:
- Trigger → GPIO 25
- Echo → GPIO 8

Right Sensor:
- Trigger → GPIO 7
- Echo → GPIO 1

LED Matrix (optional):
- Data → GPIO 10
- Clock → GPIO 11
- Latch → GPIO 9

Status LEDs:
- Red → GPIO 16
- Green → GPIO 26
- Blue → GPIO 6
```

#### 6. Configure Audio
```bash
# Test speakers
speaker-test -t sine -f 1000 -l 1

# Test microphone
arecord -d 3 test.wav && aplay test.wav

# If using USB audio, you may need to configure default devices
sudo nano /etc/asound.conf
```

#### 7. Enable GPIO and Camera
```bash
sudo raspi-config
# Navigate to:
# 3 Interface Options → P4 SPI → Enable
# 3 Interface Options → P5 I2C → Enable
# 3 Interface Options → P1 Camera → Enable
sudo reboot
```

## ⚙️ Configuration

### 1. Hardware Configuration
Copy and customize the hardware configuration:
```bash
cp src/config/hardware_config.example.py src/config/hardware_config.py
nano src/config/hardware_config.py
```

Update GPIO pins and hardware settings to match your wiring.

### 2. AI Models Setup
```bash
# Download local LLM model (choose based on Pi performance)
ollama pull llama3.2:1b  # Smaller model for Pi 4
# or
ollama pull llama3.2:3b  # Larger model if you have 8GB RAM

# The system will automatically download other models on first use
```

### 3. Test Installation
```bash
# Activate virtual environment
source venv/bin/activate

# Run component tests
python test_components.py

# Run basic robot test
python start_sarus.py --mode test
```

## 🎮 Running Sarus

### Quick Start
```bash
# Activate virtual environment
source venv/bin/activate

# Run Sarus with default settings
python start_sarus.py

# Or use specific modes:
python start_sarus.py --mode interactive    # Voice interaction mode
python start_sarus.py --mode exploration   # Autonomous exploration
python start_sarus.py --mode simulation    # Simulation mode (no hardware)
```

### Available Commands
- `python start_sarus.py --mode interactive` - Voice interaction mode
- `python start_sarus.py --mode exploration` - Autonomous exploration
- `python start_sarus.py --mode manual` - Manual control via gamepad
- `python start_sarus.py --mode simulation` - Simulation mode
- `python start_sarus.py --mode test` - Test mode

### Environment Variables (Optional)
```bash
# Set in ~/.bashrc for permanent configuration
export SARUS_MODE=interactive
export SARUS_LLM_PROVIDER=ollama  # or openai
export SARUS_LOG_LEVEL=INFO
export OPENAI_API_KEY=your_key_here  # if using OpenAI
```

## 🔧 Troubleshooting

### Common Issues

#### GPIO Permission Errors
```bash
sudo usermod -a -G gpio $USER
sudo reboot
```

#### Audio Issues
```bash
# Check audio devices
aplay -l
arecord -l

# Test audio
speaker-test -c2 -twav -l7
arecord -d 5 -f cd test.wav && aplay test.wav
```

#### Camera Not Working
```bash
# Enable camera
sudo raspi-config  # Interface Options → Camera → Enable

# Test camera
raspistill -o test.jpg
```

#### Ollama Connection Issues
```bash
# Check if Ollama is running
systemctl status ollama

# Start Ollama service
sudo systemctl start ollama
sudo systemctl enable ollama

# Test Ollama
ollama list
```

#### Package Installation Issues
```bash
# If pip packages fail to install
sudo apt install python3-dev libffi-dev

# For OpenCV issues
sudo apt install libatlas-base-dev libhdf5-dev libhdf5-serial-dev
```

### Performance Optimization

#### For Better Performance on Pi 4:
```bash
# Increase GPU memory split
sudo raspi-config  # Advanced Options → Memory Split → 128

# Enable hardware acceleration for camera
echo 'start_x=1' | sudo tee -a /boot/config.txt
echo 'gpu_mem=128' | sudo tee -a /boot/config.txt
```

#### Memory Management:
```bash
# Monitor memory usage
htop

# For 4GB Pi, use smaller models:
# - Use Whisper tiny model for STT
# - Use LLaMA 1B model instead of 3B
# - Reduce camera resolution if needed
```

## 📖 Usage Examples

### Voice Interaction
```bash
python start_sarus.py --mode interactive
# Say "Hey Sarus" to wake up
# Then give commands like:
# - "Move forward"
# - "Look around and describe what you see"
# - "Find the red object"
# - "Return to base"
```

### Manual Control
```bash
python start_sarus.py --mode manual
# Use Xbox/PS4 controller:
# - Left stick: Move forward/backward
# - Right stick: Turn left/right
# - A/X button: Stop
# - B/Circle: Emergency stop
```

### Autonomous Exploration
```bash
python start_sarus.py --mode exploration
# Sarus will automatically:
# - Navigate around obstacles
# - Map the environment
# - Report interesting findings
# - Return when battery is low
```

## 🔄 Updates and Maintenance

### Update Sarus
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Update AI Models
```bash
ollama pull llama3.2:1b  # Update local LLM
# Other models update automatically
```

### Backup Configuration
```bash
# Backup your custom settings
cp src/config/hardware_config.py ~/sarus_config_backup.py
```

## 🆘 Support

- **Documentation**: Check the `docs/` folder for detailed guides
- **Issues**: Report bugs on GitHub Issues
- **Community**: Join our Discord server
- **Logs**: Check `logs/` folder for troubleshooting

## 🎯 Next Steps

Once Sarus is running:
1. Calibrate sensors and motors
2. Train custom voice commands
3. Add custom behaviors
4. Integrate with smart home systems
5. Develop custom applications

Welcome to the world of autonomous robotics with Sarus! 🤖✨
