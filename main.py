#!/usr/bin/env python3
"""
Kahoot AI Helper - Main Application Entry Point
The Ultimate AI-Powered Kahoot Study Assistant v2.5.0
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from app import KahootAIHelperApp
from config import setup_logging, Config


def print_banner():
    """Display application banner"""
    banner = r"""
    
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║        🎮 KAHOOT AI HELPER v2.5.0 🎮                        ║
    ║                                                               ║
    ║        The Ultimate AI-Powered Kahoot Study Assistant        ║
    ║                                                               ║
    ║        ⭐ Join 100,000+ Students                             ║
    ║        🤖 AI-Powered Answers                                 ║
    ║        📊 Smart Analytics                                    ║
    ║        🚀 Instant Results                                    ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    
    """
    print(banner)


def main():
    """Main application entry point"""
    
    # Display banner
    print_banner()
    
    try:
        # Setup logging
        logger = setup_logging()
        logger.info("="*70)
        logger.info("🎮 KAHOOT AI HELPER - STARTING APPLICATION")
        logger.info("="*70)
        
        # Load configuration
        logger.info("📋 Loading configuration...")
        config = Config()
        config.load()
        logger.info("✅ Configuration loaded successfully")
        
        # Initialize application
        logger.info("🚀 Initializing application...")
        app = KahootAIHelperApp(config)
        
        # Setup database
        logger.info("💾 Setting up database...")
        app.setup_database()
        logger.info("✅ Database ready")
        
        # Start application
        logger.info("🎯 Starting main loop...")
        print("\n")
        app.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Thank you for using Kahoot AI Helper!")
        print("📚 Keep studying! Good luck on your next Kahoot! 🎉\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        if logger:
            logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
