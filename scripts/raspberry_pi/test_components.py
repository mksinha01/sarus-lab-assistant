#!/usr/bin/env python3
"""
Quick hardware sanity tests for Raspberry Pi. Safe to run without hardware (simulation fallback).
"""
import time
import json
from pathlib import Path

try:
    from src.config.settings import Config
    from src.hardware.sensors.environmental_sensor import EnvironmentalSensorManager
    from src.safety.gas_monitor import GasMonitor
    from src.safety.emergency_stop import EmergencyStop, EmergencyType
except Exception as e:
    print("Import error:", e)
    raise


def main():
    cfg = Config()
    print("Config loaded. Simulation:", getattr(cfg, 'SIMULATION_MODE', True))

    # Environmental sensor test
    env = EnvironmentalSensorManager(cfg)
    # Run one sensor read via simulate path
    reading = env._simulate_reading()
    print("Environmental reading:", reading.__dict__)

    # Gas monitor test (one simulated poll)
    gm = GasMonitor(cfg)
    # Get simulated sensor value and convert
    import asyncio as _asyncio
    ppm = env_value = None
    async def _one():
        nonlocal ppm
        raw = await gm._read_sensor('mq2')
        ppm = gm._convert_to_ppm('mq2', raw)
    _asyncio.get_event_loop().run_until_complete(_one())
    print(f"Gas PPM (sim, mq2): {ppm:.1f}")

    # Emergency stop test
    estop = EmergencyStop(cfg)
    async def _trig():
        await estop.trigger_emergency(EmergencyType.USER_EMERGENCY, "Test button", severity='low')
        print("Emergency active?", estop.is_emergency_active())
        await estop.reset_emergency()
        print("Emergency cleared?", not estop.is_emergency_active())
    _asyncio.get_event_loop().run_until_complete(_trig())

    # Write results to file
    out = {
        "env": reading.__dict__ if hasattr(reading, "__dict__") else {},
        "gas_ppm": ppm,
    "gas_level": "simulated",
    "emergency_active": estop.is_emergency_active(),
    }
    Path(".artifacts").mkdir(parents=True, exist_ok=True)
    Path(".artifacts/pi_sanity.json").write_text(json.dumps(out, indent=2))
    print("Wrote .artifacts/pi_sanity.json")


if __name__ == "__main__":
    main()
