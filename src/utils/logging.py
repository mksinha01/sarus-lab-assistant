#!/usr/bin/env python3
"""
📊 SARUS ROBOT LOGGING SYSTEM
Enhanced logging system for Sarus AI Lab Assistant Robot
"""

import logging
import logging.handlers
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

def setup_logging(
    log_level: str = "INFO",
    log_format: Optional[str] = None,
    log_dir: Optional[Path] = None
) -> logging.Logger:
    """
    Setup comprehensive logging system for Sarus robot
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Custom log format string
        log_dir: Directory for log files
    
    Returns:
        Configured logger instance
    """
    
    # Default log format
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Default log directory
    if log_dir is None:
        log_dir = Path(__file__).parent.parent.parent / "logs"
    
    # Ensure log directory exists
    log_dir.mkdir(exist_ok=True)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt=log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    console_formatter = logging.Formatter(
        fmt="%(levelname)s - %(name)s - %(message)s"
    )
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # Main log file handler
    main_log_file = log_dir / "sarus_main.log"
    file_handler = logging.handlers.RotatingFileHandler(
        main_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(file_handler)
    
    # Error log file handler
    error_log_file = log_dir / "sarus_errors.log"
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(error_handler)
    
    # System log for startup/shutdown
    startup_logger = logging.getLogger("sarus.startup")
    startup_logger.info("🚀 Sarus logging system initialized")
    startup_logger.info(f"📁 Log directory: {log_dir}")
    startup_logger.info(f"📊 Log level: {log_level}")
    
    return root_logger

def get_mission_logger(mission_id: str) -> logging.Logger:
    """
    Create a dedicated logger for mission reporting
    
    Args:
        mission_id: Unique identifier for the mission
    
    Returns:
        Mission-specific logger
    """
    
    logger_name = f"sarus.mission.{mission_id}"
    logger = logging.getLogger(logger_name)
    
    # Mission log directory
    log_dir = Path(__file__).parent.parent.parent / "logs" / "mission_reports"
    log_dir.mkdir(exist_ok=True)
    
    # Mission log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"mission_{mission_id}_{timestamp}.log"
    
    # File handler for mission
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    logger.info(f"🎯 Mission {mission_id} started")
    
    return logger

def get_security_logger() -> logging.Logger:
    """
    Create a dedicated logger for security events
    
    Returns:
        Security-specific logger
    """
    
    logger = logging.getLogger("sarus.security")
    
    # Security log directory
    log_dir = Path(__file__).parent.parent.parent / "logs" / "security"
    log_dir.mkdir(exist_ok=True)
    
    # Daily security log file
    date_str = datetime.now().strftime("%Y%m%d")
    log_file = log_dir / f"security_{date_str}.log"
    
    # File handler for security events
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.WARNING)
    
    formatter = logging.Formatter(
        "%(asctime)s - SECURITY - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)
    
    return logger

def get_environmental_logger() -> logging.Logger:
    """
    Create a dedicated logger for environmental monitoring
    
    Returns:
        Environmental monitoring logger
    """
    
    logger = logging.getLogger("sarus.environmental")
    
    # Environmental log directory
    log_dir = Path(__file__).parent.parent.parent / "logs" / "environmental"
    log_dir.mkdir(exist_ok=True)
    
    # Daily environmental log file
    date_str = datetime.now().strftime("%Y%m%d")
    log_file = log_dir / f"environmental_{date_str}.log"
    
    # File handler for environmental data
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.INFO)
    
    formatter = logging.Formatter(
        "%(asctime)s,%(message)s",  # CSV format for easy parsing
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    return logger

class SarusLoggerAdapter(logging.LoggerAdapter):
    """
    Custom logger adapter for Sarus robot with additional context
    """
    
    def process(self, msg, kwargs):
        """Add robot context to log messages"""
        robot_id = self.extra.get('robot_id', 'sarus')
        return f"[{robot_id}] {msg}", kwargs

def log_system_event(event_type: str, message: str, level: str = "INFO"):
    """
    Log a system event with standardized format
    
    Args:
        event_type: Type of event (startup, shutdown, error, etc.)
        message: Event message
        level: Log level
    """
    
    logger = logging.getLogger("sarus.system")
    log_level = getattr(logging, level.upper())
    
    formatted_message = f"[{event_type.upper()}] {message}"
    logger.log(log_level, formatted_message)

def log_performance_metric(metric_name: str, value: float, unit: str = ""):
    """
    Log a performance metric
    
    Args:
        metric_name: Name of the metric
        value: Metric value
        unit: Unit of measurement
    """
    
    logger = logging.getLogger("sarus.performance")
    
    if unit:
        message = f"{metric_name}: {value} {unit}"
    else:
        message = f"{metric_name}: {value}"
    
    logger.info(message)
