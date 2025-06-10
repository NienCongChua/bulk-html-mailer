# 🚀 Quick Start Guide

## 1. Setup (First Time Only)

### Windows Users
```bash
# Double-click start.bat or run in Command Prompt:
start.bat
```

### Mac/Linux Users
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application (recommended)
python run.py

# Or use the startup script
python start.py
```

## 2. Configure SMTP

### Gmail Setup
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use these settings:
   - Host: `smtp.gmail.com`
   - Port: `587`
   - Username: `your_email@gmail.com`
   - Password: `your_app_password`

### Outlook Setup
- Host: `smtp.office365.com`
- Port: `587`
- Username: `your_email@outlook.com`
- Password: `your_password`

## 3. Quick Demo

```bash
# Create demo data
python demo.py

# Start web interface
python app.py
```

Open: http://localhost:5000

## 4. Basic Usage

1. **Configure SMTP** → Test connection
2. **Add Recipients** → Import CSV or add manually
3. **Select Template** → Preview before sending
4. **Send Emails** → Monitor progress

## 5. CSV Format

```csv
email,name,product_name,discount_code
john@example.com,John Doe,Widget Pro,SAVE20
jane@example.com,Jane Smith,Super Tool,WELCOME10
```

## 6. Template Variables

- `{{name}}` - Recipient name
- `{{email}}` - Recipient email
- `{{product_name}}` - Product name
- `{{discount_code}}` - Discount code

## 🆘 Need Help?

- Check logs in `logs/` folder
- Use "Test SMTP" button
- Preview templates before sending
- Start with small test groups

## 🔧 Troubleshooting

**Internal Server Error?**
```bash
python debug_app.py  # Diagnose issues
python fix_app.py    # Auto-fix problems
python run.py        # Start app
```

**App Won't Start?**
```bash
python test_app.py  # Check setup
python run.py       # Auto-fix and start
```

**Template Not Found Error?**
```bash
# The app will auto-create missing templates
python fix_app.py   # Fix all template issues
python run.py       # Start with fixes
```

**SMTP Error?**
- Check credentials
- Use App Password for Gmail
- Verify host/port settings

**Template Not Loading?**
- Run `python test_app.py`
- Check file path
- Ensure file exists

**CSV Issues?**
- Use UTF-8 encoding
- Include proper headers
- Check email format

**Port 5000 Busy?**
```bash
# Use different port
python -c "from app import app; app.run(port=5001)"
```
