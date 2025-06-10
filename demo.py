#!/usr/bin/env python3
"""
Demo script to test the Bulk HTML Mailer functionality
"""

import os
import sys
from pathlib import Path

def create_demo_data():
    """Create demo data files"""
    
    # Create demo recipients CSV
    demo_csv = """email,name,product_name,discount_code
demo1@example.com,John Doe,Premium Widget,SAVE20
demo2@example.com,Jane Smith,Super Gadget,WELCOME10
demo3@example.com,Bob Johnson,Awesome Tool,VIP30"""
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    with open(data_dir / "recipients.csv", "w", encoding="utf-8") as f:
        f.write(demo_csv)
    
    print("✅ Demo recipients.csv created")

def create_demo_config():
    """Create demo configuration"""
    
    demo_config = """# ========================
# SMTP Configuration
# ========================
smtp:
  # Gmail example - replace with your settings
  host: smtp.gmail.com
  port: 587
  username: your_email@gmail.com
  password: your_app_password

# ========================
# Sender Info
# ========================
sender:
  name: Your Name
  email: your_email@gmail.com

# ========================
# Email Content
# ========================
email:
  subject: "Hello {{name}}, welcome to our service!"
  template_path: templates/welcome.html
  recipients_csv: data/recipients.csv

# ========================
# Attachments (Optional)
# ========================
attachments: []
"""
    
    with open("config.yaml", "w", encoding="utf-8") as f:
        f.write(demo_config)
    
    print("✅ Demo config.yaml created")

def create_demo_template():
    """Create a demo welcome template"""
    
    demo_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Our Service</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }
        .container {
            max-width: 600px;
            background: white;
            margin: 0 auto;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #007bff, #0056b3);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }
        .content {
            padding: 30px;
        }
        .welcome-box {
            background: #e7f3ff;
            border: 1px solid #b3d9ff;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
        }
        .cta-button {
            display: inline-block;
            background: #007bff;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            margin: 20px 0;
        }
        .footer {
            background: #f8f9fa;
            padding: 20px 30px;
            text-align: center;
            color: #6c757d;
            font-size: 14px;
        }
        @media (max-width: 600px) {
            body { padding: 10px; }
            .header, .content { padding: 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Welcome!</h1>
        </div>
        
        <div class="content">
            <div class="welcome-box">
                <h2>Hi {{name}}!</h2>
                <p>Thank you for joining our service. We're excited to have you on board!</p>
            </div>
            
            <p>You've successfully signed up for <strong>{{product_name}}</strong>.</p>
            
            <p>As a welcome gift, here's your exclusive discount code:</p>
            <div style="text-align: center; font-size: 24px; font-weight: bold; color: #007bff; margin: 20px 0;">
                {{discount_code}}
            </div>
            
            <div style="text-align: center;">
                <a href="#" class="cta-button">Get Started</a>
            </div>
            
            <p>If you have any questions, feel free to reach out to our support team.</p>
        </div>
        
        <div class="footer">
            <p>Best regards,<br>The Team</p>
            <p style="margin: 0;">This email was sent to {{email}}</p>
        </div>
    </div>
</body>
</html>"""
    
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    with open(templates_dir / "welcome.html", "w", encoding="utf-8") as f:
        f.write(demo_template)
    
    print("✅ Demo welcome.html template created")

def main():
    """Main demo setup function"""
    print("🚀 Setting up Bulk HTML Mailer Demo")
    print("=" * 40)
    
    # Create necessary directories
    for directory in ["data", "templates", "logs", "static/css", "static/js", "web_templates"]:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Create demo files
    create_demo_data()
    create_demo_config()
    create_demo_template()
    
    print("\n✅ Demo setup complete!")
    print("\n📋 Next steps:")
    print("1. Edit config.yaml with your SMTP settings")
    print("2. Run: python app.py (for web interface)")
    print("3. Or run: python mailer.py (for command line)")
    print("4. Open http://localhost:5000 in your browser")
    print("\n⚠️  Remember to use real SMTP credentials for sending emails!")

if __name__ == "__main__":
    main()
