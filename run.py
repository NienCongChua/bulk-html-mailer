#!/usr/bin/env python3
"""
Simple run script for Bulk HTML Mailer
"""

import os
import sys
from pathlib import Path

def run_fixes():
    """Run automatic fixes"""
    try:
        print("🔧 Running automatic fixes...")
        import fix_app
        fix_app.main()
        print("✅ Fixes completed")
    except Exception as e:
        print(f"⚠️  Could not run fixes: {e}")
        # Manual fixes
        required_dirs = [
            "web_templates", "templates", "static/css", "static/js", "data", "logs"
        ]
        for directory in required_dirs:
            Path(directory).mkdir(parents=True, exist_ok=True)

# Run fixes first
run_fixes()

# Create a basic config if it doesn't exist
config_file = Path("config.yaml")
if not config_file.exists():
    default_config = """# SMTP Configuration
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
        f.write(default_config)
    print("✅ Created default config.yaml")

# Create basic recipients CSV if it doesn't exist
recipients_file = Path("data/recipients.csv")
if not recipients_file.exists():
    default_recipients = """email,name,product_name,discount_code
demo@example.com,Demo User,Sample Product,DEMO10
"""
    with open(recipients_file, 'w', encoding='utf-8') as f:
        f.write(default_recipients)
    print("✅ Created default recipients.csv")

# Start the Flask app
if __name__ == "__main__":
    print("🚀 Starting Bulk HTML Mailer...")
    print("📧 Web interface: http://localhost:5000")
    print("🔧 Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check if port 5000 is available")
        print("3. Run: python test_app.py to diagnose issues")
        sys.exit(1)
