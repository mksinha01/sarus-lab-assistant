#!/bin/bash

# Sarus Robot - Automated Setup Script
# This script sets up the Sarus robot environment on Raspberry Pi 4

set -e  # Exit on any error

echo "🤖 Setting up Sarus - Autonomous AI-Powered Lab Assistant Robot"
echo "================================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Warning: This doesn't appear to be a Raspberry Pi${NC}"
    echo "Setup will continue but hardware features may not work."
fi

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}❌ Please don't run this script as root (no sudo)${NC}"
    exit 1
fi

echo -e "${BLUE}📋 Starting system update...${NC}"
sudo apt update && sudo apt upgrade -y

echo -e "${BLUE}🐍 Installing Python dependencies...${NC}"
sudo apt install -y python3-pip python3-venv python3-dev git

echo -e "${BLUE}🔊 Installing audio dependencies...${NC}"
sudo apt install -y portaudio19-dev python3-pyaudio espeak-ng alsa-utils

echo -e "${BLUE}📷 Installing computer vision dependencies...${NC}"
sudo apt install -y python3-opencv libopencv-dev libatlas-base-dev

echo -e "${BLUE}⚡ Installing GPIO and hardware dependencies...${NC}"
sudo apt install -y python3-gpiozero python3-rpi.gpio i2c-tools

echo -e "${BLUE}🧠 Installing Ollama for local AI...${NC}"
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.ai/install.sh | sh
    echo "Ollama installed successfully"
else
    echo "Ollama already installed"
fi

echo -e "${BLUE}🐍 Creating Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

echo -e "${BLUE}📦 Installing Python packages...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${BLUE}🔧 Configuring system settings...${NC}"

# Enable GPIO, I2C, SPI, and Camera
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_camera 0

# Increase GPU memory for camera
if ! grep -q "gpu_mem=128" /boot/config.txt; then
    echo "gpu_mem=128" | sudo tee -a /boot/config.txt
fi

if ! grep -q "start_x=1" /boot/config.txt; then
    echo "start_x=1" | sudo tee -a /boot/config.txt
fi

# Add user to gpio group
sudo usermod -a -G gpio $USER

echo -e "${BLUE}🎯 Downloading AI models...${NC}"
# Start Ollama service
sudo systemctl enable ollama
sudo systemctl start ollama

# Wait a moment for service to start
sleep 5

# Download local LLM model
echo "Downloading LLaMA model (this may take a while)..."
ollama pull llama3.2:1b

echo -e "${BLUE}⚙️ Creating configuration files...${NC}"
if [ ! -f src/config/hardware_config.py ]; then
    cp src/config/hardware_config.example.py src/config/hardware_config.py
    echo "Hardware configuration copied. Please edit src/config/hardware_config.py to match your wiring."
fi

echo -e "${BLUE}🧪 Running system tests...${NC}"
python test_components.py --choice 2  # Hardware tests only

echo -e "${GREEN}✅ Sarus Robot setup completed successfully!${NC}"
echo ""
echo -e "${YELLOW}📋 Next Steps:${NC}"
echo "1. Review and edit src/config/hardware_config.py for your hardware setup"
echo "2. Connect your hardware according to INSTALLATION.md"
echo "3. Test individual components: python test_components.py"
echo "4. Run Sarus: python start_sarus.py"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANT: Reboot required for GPIO changes to take effect${NC}"
echo "Run: sudo reboot"
echo ""
echo -e "${GREEN}🎉 Welcome to Sarus! Your AI lab assistant is ready to go!${NC}"
