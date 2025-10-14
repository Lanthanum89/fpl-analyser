#!/usr/bin/env python3
"""
FPL Stats & Team Selector Launcher
Quick launcher script for the FPL GUI application
"""

import sys
import subprocess
import os

def check_requirements():
    """Check if required packages are installed"""
    try:
        import requests
        import tkinter
        return True
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    """Main launcher function"""
    print("🏆 FPL Stats & Team Selector")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("fpl_gui.py"):
        print("Error: fpl_gui.py not found in current directory")
        print("Please run this script from the FPL project directory")
        return 1
    
    # Check requirements
    if not check_requirements():
        return 1
    
    print("Starting FPL GUI application...")
    
    try:
        # Import and run the GUI
        from fpl_gui import main as gui_main
        gui_main()
    except KeyboardInterrupt:
        print("\nApplication closed by user")
    except Exception as e:
        print(f"Error running application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())