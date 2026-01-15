#!/usr/bin/env python
"""
Skintelli Application Launcher
Run this file to start the application
"""

import sys
import logging
import os
from pathlib import Path

# Setup path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('skintelli.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    try:
        logger.info("Starting Skintelli application...")
        
        from PyQt6.QtWidgets import QApplication
        from ui.main_window_new import MainWindow
        
        app = QApplication(sys.argv)
        
        logger.info("Creating main window...")
        window = MainWindow()
        window.show()
        
        logger.info("Application running...")
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Error starting application: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
