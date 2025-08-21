# 🤖 Sarus Robot - Hardware Wiring Guide

## 📌 GPIO Pinout Reference
```
     3V3  (1) (2)  5V    
   GPIO2  (3) (4)  5V    
   GPIO3  (5) (6)  GND   
   GPIO4  (7) (8)  GPIO14
     GND  (9) (10) GPIO15
  GPIO17 (11) (12) GPIO18  ← Motor Left 1
  GPIO27 (13) (14) GND    
  GPIO22 (15) (16) GPIO23  ← Ultrasonic Trigger
     3V3 (17) (18) GPIO24  ← Ultrasonic Echo
  GPIO10 (19) (20) GND    
   GPIO9 (21) (22) GPIO25
  GPIO11 (23) (24) GPIO8  
     GND (25) (26) GPIO7  
   GPIO0 (27) (28) GPIO1  
   GPIO5 (29) (30) GND    
   GPIO6 (31) (32) GPIO12
  GPIO13 (33) (34) GND    
  GPIO19 (35) (36) GPIO16  ← Motor Left 2
  GPIO26 (37) (38) GPIO20  ← Motor Right 1
     GND (39) (40) GPIO21  ← Motor Right 2
```

## 🔌 Component Wiring

### 1. Ultrasonic Sensor (HC-SR04)
```
HC-SR04          Raspberry Pi
-------          ------------
VCC    ────────→ 5V (Pin 2)
GND    ────────→ GND (Pin 6)
Trig   ────────→ GPIO23 (Pin 16)
Echo   ────────→ GPIO24 (Pin 18)
```

### 2. Motor Controller (L298N)
```
L298N            Raspberry Pi
-----            ------------
VCC    ────────→ 5V (Pin 4)
GND    ────────→ GND (Pin 14)
IN1    ────────→ GPIO18 (Pin 12)  [Left Motor Forward]
IN2    ────────→ GPIO19 (Pin 35)  [Left Motor Backward]
IN3    ────────→ GPIO20 (Pin 38)  [Right Motor Forward]
IN4    ────────→ GPIO21 (Pin 40)  [Right Motor Backward]

Motor Connections:
OUT1   ────────→ Left Motor (+)
OUT2   ────────→ Left Motor (-)
OUT3   ────────→ Right Motor (+)
OUT4   ────────→ Right Motor (-)
```

### 3. Camera Module
```
Pi Camera        Raspberry Pi
---------        ------------
Ribbon Cable ──→ CSI Port (between HDMI and Audio jack)
```

### 4. Audio Components
```
USB Microphone ─→ USB Port
Speaker        ─→ 3.5mm Audio Jack or USB Port
```

### 5. Optional: OLED Display (I2C)
```
OLED Display     Raspberry Pi
------------     ------------
VCC    ────────→ 3.3V (Pin 1)
GND    ────────→ GND (Pin 9)
SDA    ────────→ GPIO2 (Pin 3)
SCL    ────────→ GPIO3 (Pin 5)
```

### 6. Optional: LED Indicators
```
Status LEDs      Raspberry Pi
-----------      ------------
LED1 (+) ──────→ GPIO12 (Pin 32) [Status LED]
LED2 (+) ──────→ GPIO16 (Pin 36) [Error LED]
LED (-) ───────→ GND (Pin 34)

Note: Use 220Ω resistors with LEDs
```

## ⚡ Power Requirements

### Power Distribution
```
┌─────────────────────────────────────┐
│         Power Supply                │
│                                     │
│  5V 3A ────┬─→ Raspberry Pi         │
│            └─→ Motor Controller     │
│                                     │
│  12V 2A ───────→ Motors (via L298N) │
└─────────────────────────────────────┘
```

### Recommended Power Setup:
- **Raspberry Pi**: 5V 3A USB-C power supply
- **Motors**: 12V 2A power supply (connected to L298N VIN)
- **Shared Ground**: Connect all GND pins together

## 🔧 Assembly Steps

### Step 1: Prepare the Chassis
1. Mount Raspberry Pi on robot chassis
2. Mount motor controller (L298N)
3. Mount ultrasonic sensor on front
4. Mount camera module

### Step 2: Wire Power
1. Connect 5V power to Pi and L298N logic
2. Connect 12V power to L298N motor supply
3. Ensure all grounds are connected

### Step 3: Wire Sensors
1. Connect ultrasonic sensor (4 wires)
2. Connect camera ribbon cable
3. Connect USB microphone
4. Connect speaker

### Step 4: Wire Motors
1. Connect motor controller to GPIO pins
2. Connect motors to motor controller outputs
3. Test motor directions

### Step 5: Test Connections
```bash
# Run hardware validation
python validate_raspberry_pi.py

# Test individual components
python test_components.py
```

## ⚠️ Safety Notes

1. **Double-check wiring** before powering on
2. **Use proper resistors** with LEDs
3. **Don't exceed GPIO current limits** (16mA per pin)
4. **Use separate power supplies** for Pi and motors
5. **Connect grounds together** but keep power separate

## 🔍 Troubleshooting

### No GPIO Access
```bash
sudo usermod -a -G gpio pi
sudo reboot
```

### Motors Not Working
- Check L298N power connections
- Verify GPIO pin numbers in code
- Test with simple GPIO commands

### Ultrasonic Sensor Issues
- Check VCC connection (needs 5V)
- Verify Trig/Echo pin connections
- Ensure proper timing in code

### Camera Not Detected
```bash
sudo raspi-config  # Enable camera
sudo reboot
libcamera-hello    # Test camera
```

## 📱 Remote Control (Optional)

For wireless control, you can also add:
- WiFi (built-in Pi 4)
- Bluetooth gamepad support
- Web interface access

## 🎯 Final Validation

Before first run:
1. ✅ All connections secure
2. ✅ Power supplies connected
3. ✅ Camera and audio working
4. ✅ GPIO permissions set
5. ✅ Software tests passing

Your Sarus robot is ready to explore! 🚀
