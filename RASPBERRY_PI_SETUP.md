# 🤖 Sarus Robot - Raspberry Pi 4 Setup Guide

## Prerequisites
- Raspberry Pi 4 (4GB RAM recommended, 8GB preferred)
- MicroSD card (32GB+ Class 10)
- Raspberry Pi OS (64-bit recommended)
- Internet connection
- SSH access or monitor/keyboard for initial setup

## 📋 Hardware Checklist
Before starting, ensure you have:
- [ ] Ultrasonic sensors (HC-SR04)
- [ ] Motor controller (L298N or similar)
- [ ] DC motors/servos
- [ ] Camera module (Pi Camera or USB webcam)
- [ ] Microphone (USB or I2S)
- [ ] Speaker (USB or 3.5mm jack)
- [ ] Display (optional - OLED/LCD)
- [ ] Jumper wires and breadboard
- [ ] Power supply for Pi and motors

## 🚀 Quick Setup Script

### 1. Download and Run Auto-Setup
```bash
# Clone the repository
git clone https://github.com/mksinha01/sarus-lab-assistant.git
cd sarus-lab-assistant

# Make setup script executable
chmod +x setup_raspberry_pi.sh

# Run the complete setup (this will take 15-30 minutes)
./setup_raspberry_pi.sh

# If using PowerShell on Pi (pwsh):
powershell -ExecutionPolicy Bypass -File scripts/raspberry_pi/setup_raspberry_pi.ps1
```

## 🔧 Manual Setup Instructions

### 1. System Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.9+ and pip
sudo apt install python3 python3-pip python3-venv git -y

# Install system dependencies
sudo apt install portaudio19-dev python3-pyaudio -y
sudo apt install libopencv-dev python3-opencv -y
sudo apt install espeak espeak-data libespeak-dev -y
sudo apt install alsa-utils pulseaudio -y
```

### 2. Enable Hardware Interfaces
```bash
sudo raspi-config
# Enable: Camera, I2C, SPI, GPIO
# Or use command line:
sudo raspi-config nonint do_camera 0
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
```

### 3. Python Environment Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install additional Pi-specific packages
pip install RPi.GPIO gpiozero
```

### 4. Audio Configuration
```bash
# Test audio output
speaker-test -t wav -c 2

# Test microphone
arecord -l
arecord -d 5 test.wav
aplay test.wav
```

### 5. Camera Test
```bash
# Test camera
libcamera-hello --preview
# Or for older Pi OS:
raspistill -o test.jpg
```

## ⚙️ Configuration

### 1. Environment Variables
Create `/home/pi/sarus-lab-assistant/.env`:
```bash
# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Hardware Configuration
HARDWARE_ENABLED=true
CAMERA_ENABLED=true
AUDIO_ENABLED=true

# GPIO Pin Configuration
MOTOR_LEFT_PIN1=18
MOTOR_LEFT_PIN2=19
MOTOR_RIGHT_PIN1=20
MOTOR_RIGHT_PIN2=21
ULTRASONIC_TRIGGER_PIN=23
ULTRASONIC_ECHO_PIN=24
```

### 2. Hardware Wiring Guide
```
Ultrasonic Sensor (HC-SR04):
├── VCC → 5V (Pin 2)
├── GND → Ground (Pin 6)
├── Trig → GPIO 23 (Pin 16)
└── Echo → GPIO 24 (Pin 18)

Motor Controller (L298N):
├── IN1 → GPIO 18 (Pin 12)
├── IN2 → GPIO 19 (Pin 35)
├── IN3 → GPIO 20 (Pin 38)
├── IN4 → GPIO 21 (Pin 40)
├── VCC → 5V (Pin 4)
└── GND → Ground (Pin 14)

Camera Module:
└── CSI Port (ribbon cable)

Audio:
├── USB Microphone → USB Port
└── Speaker → 3.5mm jack or USB
```

## 🧪 Testing on Raspberry Pi

### 1. Quick System Test
```bash
cd /home/pi/sarus-lab-assistant
source venv/bin/activate
python test_components.py
# Choose option 1 (All tests)
```

### 2. Hardware-Only Test
```bash
python test_components.py
# Choose option 2 (Hardware only)
```

### 3. Start Robot
```bash
python main.py
```

## 🔄 Auto-Start Setup

### 1. Create Systemd Service
```bash
sudo nano /etc/systemd/system/sarus-robot.service
```

Add this content:
```ini
[Unit]
Description=Sarus Lab Assistant Robot
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/sarus-lab-assistant
Environment=PATH=/home/pi/sarus-lab-assistant/venv/bin
ExecStart=/home/pi/sarus-lab-assistant/venv/bin/python main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### 2. Enable Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable sarus-robot.service
sudo systemctl start sarus-robot.service

# Check status
sudo systemctl status sarus-robot.service

# Optionally, copy the pre-made unit from scripts:
# sudo cp scripts/raspberry_pi/sarus-robot.service /etc/systemd/system/sarus-robot.service
```

## 📊 Performance Optimization

### 1. GPU Memory Split
```bash
sudo raspi-config
# Advanced Options → Memory Split → 128MB
```

### 2. Disable Unnecessary Services
```bash
sudo systemctl disable bluetooth
sudo systemctl disable wifi-powersave
```

### 3. Overclock (Optional)
```bash
sudo nano /boot/config.txt
# Add these lines:
arm_freq=2000
gpu_freq=750
```

## 🔍 Troubleshooting

### Common Issues:
1. **GPIO Permission Denied**: Add user to gpio group
   ```bash
   sudo usermod -a -G gpio pi
   ```

2. **Audio Not Working**: Check ALSA configuration
   ```bash
   sudo alsamixer
   amixer set PCM 100%
   ```

3. **Camera Not Detected**: Check cable connection and enable camera
   ```bash
   sudo raspi-config # Enable camera
   sudo reboot
   ```

4. **Import Errors**: Ensure virtual environment is activated
   ```bash
   source venv/bin/activate
   ```

## 🎯 Next Steps
1. Complete hardware wiring
2. Run setup script
3. Test all components
4. Configure auto-start
5. Start exploring with your Sarus robot!

## 📞 Support
- Check logs: `journalctl -u sarus-robot.service -f`
- GPIO pinout: `pinout` command
- Test individual components with `test_components.py`
