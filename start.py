#!/usr/bin/env python3
"""
Bulk HTML Mailer - Startup Script
Automatically opens the web interface in the default browser
"""

import os
import sys
import time
import webbrowser
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import flask
        import yaml
        import jinja2
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_config():
    """Check if config file exists"""
    config_file = Path("config.yaml")
    if not config_file.exists():
        print("⚠️  Config file not found. Default config will be created.")
        return False
    print("✅ Config file found")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ["logs", "static/css", "static/js", "web_templates", "data"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ Directories created")

def start_server():
    """Start the Flask server"""
    print("🚀 Starting Bulk HTML Mailer...")
    print("📧 Web interface will be available at: http://localhost:5000")
    print("🔧 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    # Start the Flask app
    try:
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

def open_browser():
    """Open the web interface in the default browser"""
    time.sleep(2)  # Wait for server to start
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Opening web interface in your default browser...")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("Please manually open: http://localhost:5000")

def main():
    """Main startup function"""
    print("=" * 50)
    print("📧 BULK HTML MAILER")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Check config
    check_config()
    
    # Open browser in background
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
