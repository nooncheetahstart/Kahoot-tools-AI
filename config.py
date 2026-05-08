"""
Configuration Management for Kahoot AI Helper
Handles settings, logging, and environment configuration
"""

import os
import yaml
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


class Config:
    """Configuration manager"""
    
    def __init__(self):
        """Initialize configuration"""
        self.config_file = Path("config.yaml")
        self.logs_dir = Path("logs")
        self.db_dir = Path("database")
        
        # Create directories
        self.logs_dir.mkdir(exist_ok=True)
        self.db_dir.mkdir(exist_ok=True)
        
        # Default configuration
        self.app_name = "Kahoot AI Helper"
        self.version = "2.5.0"
        self.language = "en"
        self.theme = "dark"
        self.ai_model = "advanced"
        self.accuracy_mode = "high"
        self.auto_answer = True
        self.show_confidence = True
        self.debug_mode = False
    
    def load(self):
        """Load configuration from YAML file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config_data = yaml.safe_load(f) or {}
                    for key, value in config_data.items():
                        setattr(self, key, value)
            except Exception as e:
                logger = logging.getLogger(__name__)
                logger.warning(f"Could not load config file: {e}")
    
    def save(self):
        """Save configuration to YAML file"""
        config_data = {
            'app_name': self.app_name,
            'version': self.version,
            'language': self.language,
            'theme': self.theme,
            'ai_model': self.ai_model,
            'accuracy_mode': self.accuracy_mode,
            'auto_answer': self.auto_answer,
            'show_confidence': self.show_confidence,
            'debug_mode': self.debug_mode,
        }
        try:
            with open(self.config_file, 'w') as f:
                yaml.dump(config_data, f)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Could not save config: {e}")


def setup_logging():
    """Setup logging configuration"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"kahoot_ai_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger


if __name__ == '__main__':
    setup_logging()
    config = Config()
    config.save()
    print("Configuration initialized!")
