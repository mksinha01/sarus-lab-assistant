"""
Logging configuration and utilities for Sarus robot

Provides centralized logging setup with appropriate handlers,
formatters, and log levels for different components.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from datetime import datetime

from ..config.settings import SYSTEM_CONFIG, LOGS_DIR

def setup_logging():
    """Configure logging for the entire Sarus system"""
    
    # Create logs directory if it doesn't exist
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, SYSTEM_CONFIG.get('log_level', 'INFO')))
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler with rotation
    log_file = LOGS_DIR / f"sarus_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=SYSTEM_CONFIG.get('log_file_max_size', 10 * 1024 * 1024),
        backupCount=SYSTEM_CONFIG.get('log_backup_count', 5)
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(file_handler)
    
    # Error handler - separate file for errors only
    error_file = LOGS_DIR / f"sarus_errors_{datetime.now().strftime('%Y%m%d')}.log"
    error_handler = logging.handlers.RotatingFileHandler(
        error_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(error_handler)
    
    # Component-specific loggers
    setup_component_loggers()
    
    logging.info("🔧 Logging system initialized")

def setup_component_loggers():
    """Setup specialized loggers for different components"""
    
    # AI components
    ai_logger = logging.getLogger('sarus.ai')
    ai_logger.setLevel(logging.DEBUG)
    
    # Hardware components
    hardware_logger = logging.getLogger('sarus.hardware')
    hardware_logger.setLevel(logging.DEBUG)
    
    # Navigation
    nav_logger = logging.getLogger('sarus.navigation')
    nav_logger.setLevel(logging.DEBUG)
    
    # Mission logging
    mission_logger = logging.getLogger('sarus.mission')
    mission_file = LOGS_DIR / f"missions_{datetime.now().strftime('%Y%m%d')}.log"
    mission_handler = logging.handlers.RotatingFileHandler(
        mission_file,
        maxBytes=50 * 1024 * 1024,  # 50MB for mission logs
        backupCount=10
    )
    mission_formatter = logging.Formatter(
        '%(asctime)s - MISSION - %(message)s'
    )
    mission_handler.setFormatter(mission_formatter)
    mission_logger.addHandler(mission_handler)
    mission_logger.setLevel(logging.INFO)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        Configured logger instance
    """
    return logging.getLogger(f"sarus.{name}")

class PerformanceLogger:
    """Utility class for logging performance metrics"""
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.logger = get_logger('performance')
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.debug(f"Starting {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = (datetime.now() - self.start_time).total_seconds()
            self.logger.info(f"{self.operation_name} completed in {duration:.3f}s")
        
        if exc_type:
            self.logger.error(f"{self.operation_name} failed: {exc_val}")

# Usage example:
# with PerformanceLogger("AI processing"):
#     result = ai_model.process(input_data)
