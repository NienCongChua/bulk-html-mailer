import smtplib
import csv
import ssl
import yaml
from jinja2 import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

def load_config(path='config.yaml'):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_template(path):
    with open(path, 'r', encoding='utf-8') as f:
        return Template(f.read())

def read_recipients(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def attach_files(msg, attachments):
    for filepath in attachments:
        try:
            with open(filepath, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={Path(filepath).name}",
                )
                msg.attach(part)
        except Exception as e:
            print(f"⚠️ Could not attach {filepath}: {e}")

def send_email(smtp_config, sender_info, recipient, subject_template, html_template, attachments):
    subject = Template(subject_template).render(**recipient)
    html_content = html_template.render(**recipient)

    msg = MIMEMultipart("mixed")
    msg['Subject'] = subject
    msg['From'] = f"{sender_info['name']} <{sender_info['email']}>"
    msg['To'] = recipient['email']

    # Add HTML body
    alternative_part = MIMEMultipart("alternative")
    mime_html = MIMEText(html_content, 'html')
    alternative_part.attach(mime_html)
    msg.attach(alternative_part)

    # Add attachments
    attach_files(msg, attachments)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
        server.starttls(context=context)
        server.login(smtp_config['username'], smtp_config['password'])
        server.sendmail(sender_info['email'], recipient['email'], msg.as_string())

def main():
    config = load_config()
    smtp_config = config['smtp']
    sender_info = config['sender']
    email_conf = config['email']
    attachments = config.get('attachments', [])

    recipients = read_recipients(email_conf['recipients_csv'])
    html_template = load_template(email_conf['template_path'])
    subject_template = email_conf['subject']

    success = 0
    fail = 0

    Path("logs").mkdir(exist_ok=True)
    with open("logs/send_log.txt", "w", encoding="utf-8") as log_file:
        for recipient in recipients:
            try:
                send_email(smtp_config, sender_info, recipient, subject_template, html_template, attachments)
                print(f"✅ Sent to {recipient['email']}")
                log_file.write(f"✅ Sent to {recipient['email']}\n")
                success += 1
            except Exception as e:
                print(f"❌ Failed to send to {recipient['email']}: {e}")
                log_file.write(f"❌ Failed to {recipient['email']}: {e}\n")
                fail += 1

    print(f"\n📊 Done! Success: {success}, Failures: {fail}")

if __name__ == "__main__":
    main()
