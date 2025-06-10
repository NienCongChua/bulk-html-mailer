# 📧 Bulk HTML Mailer

A powerful Python-based bulk email sender with a modern web interface, responsive HTML templates, SMTP integration, and dynamic personalization.

## ✨ Features

### 🌐 Web Interface
*   **Modern Dashboard:** Beautiful web interface built with Flask and Bootstrap 5
*   **Template Management:** Create, edit, and preview email templates with live preview
*   **Recipient Management:** Add, edit, and import recipients via CSV
*   **Campaign Management:** Send emails with real-time progress tracking
*   **Configuration Panel:** Easy SMTP setup and testing

### 📧 Email Features
*   **Bulk Email Sending:** Efficiently send emails to large recipient lists
*   **Responsive Templates:** Professional HTML templates optimized for all devices
*   **SMTP Integration:** Support for Gmail, Outlook, Yahoo, SendGrid, Mailgun, and custom SMTP
*   **Dynamic Personalization:** Use placeholders like `{{name}}`, `{{product_name}}` for personalized content
*   **Template Preview:** Preview emails with sample data before sending
*   **Attachment Support:** Send files along with your emails

### 🛠️ Technical Features
*   **Real-time Logging:** Track email sending progress and errors
*   **CSV Import/Export:** Easy recipient management
*   **Template Editor:** Built-in HTML editor with syntax highlighting
*   **Responsive Design:** Works perfectly on desktop and mobile devices

## 📋 Prerequisites

*   Python 3.7+
*   Access to an SMTP server (Gmail, Outlook, Yahoo, or custom SMTP)
*   Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/NienCongChua/bulk-html-mailer.git
cd bulk-html-mailer

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

**Option 1: Simple Run (Recommended)**
```bash
python run.py
```

**Option 2: Direct Flask App**
```bash
python app.py
```

**Option 3: Test Setup First**
```bash
python test_app.py  # Check for issues
python run.py       # Start the app
```

The web interface will be available at: **http://localhost:5000**

### 3. Alternative: Command Line Usage

```bash
# Configure SMTP settings in config.yaml first, then:
python mailer.py
```

## 🔧 Configuration

### Web Interface Configuration

1. **Access the Configuration Panel**
   - Open http://localhost:5000
   - Navigate to "Cấu hình" in the menu

2. **SMTP Settings**
   - **Gmail:** `smtp.gmail.com:587` (use App Password if 2FA enabled)
   - **Outlook:** `smtp.office365.com:587`
   - **Yahoo:** `smtp.mail.yahoo.com:587`
   - **Custom SMTP:** Enter your server details

3. **Test Connection**
   - Use the "Test SMTP" button to verify your settings

### Manual Configuration (config.yaml)

```yaml
smtp:
  host: smtp.gmail.com
  port: 587
  username: your_email@gmail.com
  password: your_app_password

sender:
  name: Your Name
  email: your_email@gmail.com

email:
  subject: "Hello {{name}}!"
  template_path: templates/default.html
  recipients_csv: data/recipients.csv

attachments: []
```

## 📖 Usage Guide

### 🌐 Using the Web Interface (Recommended)

1. **Start the Application**
   ```bash
   python app.py
   ```
   Open http://localhost:5000 in your browser

2. **Configure SMTP Settings**
   - Go to "Cấu hình" → Enter your SMTP details
   - Test the connection to ensure it works

3. **Manage Recipients**
   - Go to "Người nhận" → Add recipients manually or import CSV
   - CSV format: `email,name,product_name,discount_code`

4. **Create/Edit Templates**
   - Go to "Templates" → Create new or edit existing templates
   - Use the built-in editor with live preview
   - Available templates: alert, welcome, newsletter, invoice, etc.

5. **Send Emails**
   - Go to "Gửi Email" → Select template and recipients
   - Preview before sending
   - Monitor progress in real-time

### 💻 Command Line Usage

```bash
# Make sure config.yaml is properly configured
python mailer.py
```

### 📄 CSV Format

Create a CSV file with recipient data:

```csv
email,name,product_name,discount_code
john.doe@example.com,John Doe,Awesome Widget,WELCOME10
jane.smith@example.com,Jane Smith,Super Gadget,SAVE20
alice@example.com,Alice Johnson,Premium Service,VIP30
```

### 🎨 Template Variables

Use these placeholders in your templates:

- `{{name}}` - Recipient's name
- `{{email}}` - Recipient's email
- `{{product_name}}` - Product name
- `{{discount_code}}` - Discount code
- `{{company_name}}` - Your company name
- `{{ip}}`, `{{location}}`, `{{device}}`, `{{time}}` - For security alerts

## 📁 Project Structure

```
bulk-html-mailer/
├── app.py                 # Flask web application
├── mailer.py             # Command-line email sender
├── config.yaml           # Configuration file
├── requirements.txt      # Python dependencies
├── static/               # Web assets
│   ├── css/style.css    # Custom styles
│   └── js/main.js       # JavaScript functionality
├── templates/            # Email templates
│   ├── alert.html       # Security alert template
│   ├── welcome.html     # Welcome email template
│   ├── newsletter.html  # Newsletter template
│   └── ...              # Other templates
├── web_templates/        # Web interface templates
│   ├── base.html        # Base template
│   ├── dashboard.html   # Dashboard page
│   └── ...              # Other web pages
├── data/                 # Data files
│   └── recipients.csv   # Recipient list
└── logs/                 # Log files
    └── send_log.txt     # Email sending logs
```

## 🔒 Security Notes

- **App Passwords:** Use App Passwords for Gmail/Outlook if 2FA is enabled
- **Credentials:** Keep your SMTP credentials secure
- **Rate Limiting:** Be mindful of SMTP server rate limits
- **Testing:** Always test with a small group before bulk sending

## 🐛 Troubleshooting

### Quick Fixes

**Template Not Found Error:**
```bash
python test_app.py  # Check what's missing
python run.py       # Auto-creates missing files
```

**Dependencies Missing:**
```bash
pip install -r requirements.txt
```

**Port Already in Use:**
```bash
# Kill process using port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or use different port
python -c "from app import app; app.run(port=5001)"
```

### Common Issues

1. **SMTP Authentication Failed**
   - Check username/password
   - Use App Password for Gmail with 2FA
   - Verify SMTP host and port

2. **Template Not Loading**
   - Run `python test_app.py` to check setup
   - Ensure all web_templates exist
   - Check file permissions

3. **CSV Import Issues**
   - Ensure CSV has proper headers
   - Check file encoding (UTF-8 recommended)
   - Verify email format in CSV

4. **Flask App Won't Start**
   - Check Python version (3.7+ required)
   - Install dependencies: `pip install -r requirements.txt`
   - Use `python run.py` instead of `python app.py`

### Getting Help

- Run `python test_app.py` for diagnostics
- Check the logs in the `logs/` directory
- Use the "Test SMTP" feature to verify connection
- Preview templates before sending

## 📄 License

This project is licensed under the MIT License. You can find the full license text in the [LICENSE](LICENSE) file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⭐ Features Coming Soon

- [ ] Email scheduling
- [ ] Advanced analytics
- [ ] Template marketplace
- [ ] API endpoints
- [ ] Docker support