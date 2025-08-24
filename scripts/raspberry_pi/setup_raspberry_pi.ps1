# Requires: Windows PowerShell/PowerShell on the Pi with SSH remoting or run via pwsh on Pi. If running on Pi, execute: pwsh ./scripts/raspberry_pi/setup_raspberry_pi.ps1
param(
    [switch]$InstallDevTools
)

Write-Host "[Sarus Setup] Updating APT and installing base packages..."
sudo apt-get update -y ; sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-pip python3-venv git libatlas-base-dev portaudio19-dev sox ffmpeg
sudo apt-get install -y python3-opencv python3-picamera2 # prefer distro OpenCV & Picamera2

Write-Host "[Sarus Setup] Creating virtual environment..."
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip wheel setuptools

Write-Host "[Sarus Setup] Installing Python requirements (Pi-friendly)..."
./.venv/bin/python -m pip install -r requirements.txt

if ($InstallDevTools) {
  Write-Host "[Sarus Setup] Installing developer tools (optional)..."
  sudo apt-get install -y vim htop i2c-tools
}

Write-Host "[Sarus Setup] Enabling I2C and Camera..."
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_camera 0

Write-Host "[Sarus Setup] Done. Activate venv with: source .venv/bin/activate"
