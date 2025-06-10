#!/usr/bin/env python3
"""
Quick Start Script for Bulk HTML Mailer
Automatically fixes common issues and starts the app
"""

import os
import sys
import time
import webbrowser
import threading
from pathlib import Path

def create_missing_files():
    """Create any missing files and directories"""
    
    # Create directories
    directories = [
        "web_templates", "templates", "static/css", "static/js", 
        "data", "logs", "attachments"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Create config.yaml if missing
    config_file = Path("config.yaml")
    if not config_file.exists():
        config_content = """# SMTP Configuration
smtp:
  host: smtp.gmail.com
  port: 587
  username: your_email@gmail.com
  password: your_app_password

# Sender Info  
sender:
  name: Your Name
  email: your_email@gmail.com

# Email Content
email:
  subject: "Hello {{name}}!"
  template_path: templates/default.html
  recipients_csv: data/recipients.csv

# Attachments
attachments: []
"""
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("✅ Created config.yaml")
    
    # Create recipients.csv if missing
    recipients_file = Path("data/recipients.csv")
    if not recipients_file.exists():
        recipients_content = """email,name,product_name,discount_code
demo@example.com,Demo User,Sample Product,DEMO10
test@example.com,Test User,Premium Service,SAVE20
"""
        with open(recipients_file, 'w', encoding='utf-8') as f:
            f.write(recipients_content)
        print("✅ Created recipients.csv")
    
    # Create default.html template if missing
    default_template = Path("templates/default.html")
    if not default_template.exists():
        template_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{subject}}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f4f4f4; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
        .header { text-align: center; margin-bottom: 30px; }
        .content { line-height: 1.6; }
        .footer { margin-top: 30px; text-align: center; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Hello {{name}}!</h1>
        </div>
        <div class="content">
            <p>Thank you for your interest in {{product_name}}!</p>
            <p>Use code <strong>{{discount_code}}</strong> to get a special discount.</p>
        </div>
        <div class="footer">
            <p>Best regards,<br>The Team</p>
        </div>
    </div>
</body>
</html>"""
        with open(default_template, 'w', encoding='utf-8') as f:
            f.write(template_content)
        print("✅ Created default.html template")

def check_dependencies():
    """Check if dependencies are installed"""
    try:
        import flask
        import yaml
        import jinja2
        return True
    except ImportError:
        print("❌ Missing dependencies. Installing...")
        os.system("pip install -r requirements.txt")
        return True

def open_browser_delayed():
    """Open browser after a delay"""
    time.sleep(3)
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Opened web interface in browser")
    except:
        print("⚠️  Please manually open: http://localhost:5000")

def main():
    """Main function"""
    print("🚀 Bulk HTML Mailer - Quick Start")
    print("=" * 40)
    
    # Check and install dependencies
    if not check_dependencies():
        print("❌ Failed to install dependencies")
        return 1
    
    # Create missing files
    create_missing_files()
    
    # Start browser in background
    browser_thread = threading.Thread(target=open_browser_delayed)
    browser_thread.daemon = True
    browser_thread.start()
    
    print("\n🎉 Setup complete!")
    print("📧 Starting web interface at: http://localhost:5000")
    print("🔧 Press Ctrl+C to stop")
    print("-" * 40)
    
    # Start Flask app
    try:
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\n🔧 Try these solutions:")
        print("1. Check if port 5000 is free")
        print("2. Run: python test_app.py")
        print("3. Run: python run.py")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
