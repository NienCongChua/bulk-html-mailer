#!/usr/bin/env python3
"""
Fix script for Bulk HTML Mailer
Automatically fixes common issues and ensures all files exist
"""

import os
import sys
from pathlib import Path

def create_missing_templates():
    """Create any missing email templates"""
    
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    # Check if default.html exists
    default_template = templates_dir / "default.html"
    if not default_template.exists():
        content = """<!DOCTYPE html>
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
            f.write(content)
        print(f"✅ Created {default_template}")

def create_missing_web_templates():
    """Ensure all web templates exist"""
    
    web_templates_dir = Path("web_templates")
    web_templates_dir.mkdir(exist_ok=True)
    
    # List of required web templates
    required_templates = [
        'base.html', 'dashboard.html', 'templates.html', 
        'recipients.html', 'send.html', 'config.html', 'preview.html'
    ]
    
    for template_name in required_templates:
        template_path = web_templates_dir / template_name
        if not template_path.exists():
            print(f"❌ Missing web template: {template_name}")
            # Create a basic template
            basic_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{template_name}</title>
</head>
<body>
    <h1>{template_name} - Template Missing</h1>
    <p>This template needs to be created.</p>
</body>
</html>"""
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(basic_content)
            print(f"✅ Created basic {template_name}")
        else:
            print(f"✅ {template_name} exists")

def create_missing_directories():
    """Create all required directories"""
    
    directories = [
        "templates", "web_templates", "static", "static/css", 
        "static/js", "data", "logs", "attachments"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Directory: {directory}")

def create_basic_config():
    """Create basic config if missing"""
    
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

def create_basic_recipients():
    """Create basic recipients CSV if missing"""
    
    recipients_file = Path("data/recipients.csv")
    if not recipients_file.exists():
        recipients_content = """email,name,product_name,discount_code
demo@example.com,Demo User,Sample Product,DEMO10
test@example.com,Test User,Premium Service,SAVE20
"""
        with open(recipients_file, 'w', encoding='utf-8') as f:
            f.write(recipients_content)
        print("✅ Created recipients.csv")

def test_app_import():
    """Test if the app can be imported"""
    try:
        import app
        print("✅ App imports successfully")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def main():
    """Main fix function"""
    print("🔧 Fixing Bulk HTML Mailer...")
    print("=" * 40)
    
    # Create missing directories
    create_missing_directories()
    
    # Create missing templates
    create_missing_templates()
    create_missing_web_templates()
    
    # Create basic config and data
    create_basic_config()
    create_basic_recipients()
    
    # Test app import
    app_ok = test_app_import()
    
    print("\n" + "=" * 40)
    if app_ok:
        print("🎉 All fixes applied successfully!")
        print("✅ App should now work properly")
        print("\n🚀 Try running: python run.py")
    else:
        print("⚠️  Some issues remain. Check the error messages above.")
        print("\n🔧 Try installing dependencies: pip install -r requirements.txt")
    
    return 0 if app_ok else 1

if __name__ == "__main__":
    sys.exit(main())
