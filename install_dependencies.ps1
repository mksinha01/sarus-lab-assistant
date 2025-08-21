# Sarus Robot Dependencies Installer
# Run this script to install all required hardware dependencies

Write-Host "🤖 Installing Sarus Robot Dependencies..." -ForegroundColor Green

# Activate virtual environment if it exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
}

Write-Host "`n📦 Installing Hardware Dependencies..." -ForegroundColor Cyan

# GPIO Libraries (for Raspberry Pi hardware)
Write-Host "Installing GPIO libraries..." -ForegroundColor Yellow
pip install gpiozero RPi.GPIO

# Audio Libraries
Write-Host "Installing audio libraries..." -ForegroundColor Yellow
pip install pyaudio speechrecognition openai-whisper

# Computer Vision Libraries
Write-Host "Installing computer vision libraries..." -ForegroundColor Yellow
pip install opencv-python opencv-contrib-python

# Additional AI Libraries
Write-Host "Installing additional AI libraries..." -ForegroundColor Yellow
pip install google-generativeai

Write-Host "`n✅ Hardware Dependencies Installation Complete!" -ForegroundColor Green
Write-Host "Note: Some hardware features may still show warnings on Windows/non-Pi systems." -ForegroundColor Yellow
