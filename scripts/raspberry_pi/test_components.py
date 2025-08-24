#!/usr/bin/env python3
"""
Quick hardware sanity tests for Raspberry Pi. Safe to run without hardware (simulation fallback).
"""
import time
import json
from pathlib import Path

try:
    from src.config.settings import Config
    from src.hardware.sensors.environmental_sensor import EnvironmentalSensor
    from src.safety.gas_monitor import GasMonitor
    from src.safety.emergency_stop import EmergencyStop, EmergencyType
except Exception as e:
    print("Import error:", e)
    raise


def main():
    cfg = Config(simulation=True)
    print("Config loaded. Simulation:", cfg.simulation)

    # Environmental sensor test
    env = EnvironmentalSensor(cfg)
    reading = env.read()
    print("Environmental reading:", reading)

    # Gas monitor test (one simulated poll)
    gm = GasMonitor(cfg, alert_callback=lambda lvl, ppm: print(f"[ALERT] Gas level {lvl} ppm={ppm:.1f}"))
    ppm = gm._read_gas_ppm_simulated()
    print(f"Gas PPM (sim): {ppm:.1f}")
    lvl = gm._classify_level(ppm)
    print("Gas level:", lvl)

    # Emergency stop test
    estop = EmergencyStop()
    estop.trigger(EmergencyType.USER, reason="Test button")
    print("Emergency active?", estop.is_active)
    estop.clear()
    print("Emergency cleared?", not estop.is_active)

    # Write results to file
    out = {
        "env": reading.__dict__ if hasattr(reading, "__dict__") else dict(reading),
        "gas_ppm": ppm,
        "gas_level": lvl.name if hasattr(lvl, "name") else str(lvl),
        "emergency_active": estop.is_active,
    }
    Path(".artifacts").mkdir(parents=True, exist_ok=True)
    Path(".artifacts/pi_sanity.json").write_text(json.dumps(out, indent=2))
    print("Wrote .artifacts/pi_sanity.json")


if __name__ == "__main__":
    main()
