#!/bin/bash

# 🤖 Sarus Robot - Raspberry Pi 4 Automated Setup Script
# This script will set up your Raspberry Pi for the Sarus lab assistant robot

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

# Check if running on Raspberry Pi
check_raspberry_pi() {
    if [[ ! -f /proc/device-tree/model ]] || ! grep -q "Raspberry Pi" /proc/device-tree/model; then
        error "This script must be run on a Raspberry Pi!"
        exit 1
    fi
    
    PI_MODEL=$(tr -d '\0' </proc/device-tree/model)
    log "Detected: $PI_MODEL"
}

# Update system
update_system() {
    log "🔄 Updating system packages..."
    sudo apt update
    sudo apt upgrade -y
}

# Install system dependencies
install_system_deps() {
    log "📦 Installing system dependencies..."
    
    # Core packages
    sudo apt install -y \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        git \
        build-essential \
        cmake \
        pkg-config
    
    # Audio packages
    sudo apt install -y \
        portaudio19-dev \
        python3-pyaudio \
        alsa-utils \
        pulseaudio \
        espeak \
        espeak-data \
        libespeak-dev
    
    # Computer vision packages
    sudo apt install -y \
        libopencv-dev \
        python3-opencv \
        libatlas-base-dev \
        libjpeg-dev \
        libtiff5-dev \
        libpng-dev \
        libavcodec-dev \
        libavformat-dev \
        libswscale-dev \
        libv4l-dev \
        libxvidcore-dev \
        libx264-dev
    
    # GPIO and hardware packages
    sudo apt install -y \
        python3-gpiozero \
        python3-rpi.gpio
    
    log "✅ System dependencies installed"
}

# Enable hardware interfaces
enable_hardware() {
    log "🔧 Enabling hardware interfaces..."
    
    # Enable camera
    sudo raspi-config nonint do_camera 0
    
    # Enable I2C
    sudo raspi-config nonint do_i2c 0
    
    # Enable SPI
    sudo raspi-config nonint do_spi 0
    
    # Add user to gpio group
    sudo usermod -a -G gpio $USER
    
    log "✅ Hardware interfaces enabled"
}

# Set up Python environment
setup_python_env() {
    log "🐍 Setting up Python virtual environment..."
    
    # Create virtual environment
    python3 -m venv venv
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    if [[ -f requirements.txt ]]; then
        log "Installing Python dependencies..."
        pip install -r requirements.txt
    else
        warning "requirements.txt not found, installing basic packages..."
        pip install numpy opencv-python pillow pygame
        pip install pyaudio wave pydub
        pip install openai-whisper pyttsx3
        pip install google-generativeai openai httpx
        pip install RPi.GPIO gpiozero
        pip install python-dotenv asyncio-mqtt
    fi
    
    log "✅ Python environment set up"
}

# Configure audio
configure_audio() {
    log "🔊 Configuring audio..."
    
    # Set default audio output to headphones
    sudo raspi-config nonint do_audio 1
    
    # Set volume to 70%
    amixer set PCM 70% 2>/dev/null || true
    
    # Test audio (optional)
    if command -v speaker-test >/dev/null; then
        info "Testing audio output (5 seconds)..."
        timeout 5 speaker-test -t wav -c 2 >/dev/null 2>&1 || true
    fi
    
    log "✅ Audio configured"
}

# Configure camera
configure_camera() {
    log "📷 Configuring camera..."
    
    # Increase GPU memory split for camera
    if ! grep -q "gpu_mem" /boot/config.txt; then
        echo "gpu_mem=128" | sudo tee -a /boot/config.txt
    fi
    
    # Test camera (optional)
    if command -v libcamera-hello >/dev/null; then
        info "Testing camera (5 seconds)..."
        timeout 5 libcamera-hello --preview 2>/dev/null || true
    elif command -v raspistill >/dev/null; then
        info "Testing camera..."
        raspistill -t 1000 -o /tmp/test.jpg 2>/dev/null || true
        rm -f /tmp/test.jpg
    fi
    
    log "✅ Camera configured"
}

# Create environment file
create_env_file() {
    log "⚙️ Creating environment configuration..."
    
    if [[ ! -f .env ]]; then
        cat > .env << EOF
# API Keys (replace with your actual keys)
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

# Logging
LOG_LEVEL=INFO
LOG_FILE=/home/pi/sarus-robot.log
EOF
        log "✅ Environment file created (.env)"
        warning "Please edit .env file and add your API keys!"
    else
        info "Environment file (.env) already exists"
    fi
}

# Create systemd service
create_systemd_service() {
    log "🔄 Creating systemd service..."
    
    sudo tee /etc/systemd/system/sarus-robot.service > /dev/null << EOF
[Unit]
Description=Sarus Lab Assistant Robot
After=network.target sound.target

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=$PWD
Environment=PATH=$PWD/venv/bin
ExecStart=$PWD/venv/bin/python main.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
    
    sudo systemctl daemon-reload
    
    log "✅ Systemd service created"
    info "To enable auto-start: sudo systemctl enable sarus-robot.service"
    info "To start now: sudo systemctl start sarus-robot.service"
}

# Run tests
run_tests() {
    log "🧪 Running component tests..."
    
    source venv/bin/activate
    
    if [[ -f test_components.py ]]; then
        python test_components.py << EOF
2
EOF
        log "✅ Hardware tests completed"
    else
        warning "test_components.py not found, skipping tests"
    fi
}

# Main setup function
main() {
    log "🤖 Starting Sarus Robot Raspberry Pi Setup"
    log "This will take 15-30 minutes depending on your internet connection"
    
    check_raspberry_pi
    update_system
    install_system_deps
    enable_hardware
    setup_python_env
    configure_audio
    configure_camera
    create_env_file
    create_systemd_service
    run_tests
    
    log "🎉 Setup completed successfully!"
    echo
    info "Next steps:"
    echo "1. Edit .env file with your API keys: nano .env"
    echo "2. Wire up your hardware components (see RASPBERRY_PI_SETUP.md)"
    echo "3. Test components: source venv/bin/activate && python test_components.py"
    echo "4. Start robot: python main.py"
    echo "5. Enable auto-start: sudo systemctl enable sarus-robot.service"
    echo
    warning "REBOOT REQUIRED for all hardware changes to take effect!"
    echo "Run: sudo reboot"
}

# Run main function
main "$@"
