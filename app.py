from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, send_file
import os
import yaml
import csv
import json
from pathlib import Path
from datetime import datetime
from mailer import load_config, load_template, read_recipients, send_email
import smtplib
import ssl
from jinja2 import Template
from glob import glob

app = Flask(__name__, template_folder='web_templates')
app.secret_key = 'your-secret-key-change-this'

# Ensure required directories exist
Path("logs").mkdir(exist_ok=True)
Path("static/css").mkdir(parents=True, exist_ok=True)
Path("static/js").mkdir(parents=True, exist_ok=True)
Path("web_templates").mkdir(exist_ok=True)

@app.route('/')
def index():
    """Dashboard chính"""
    try:
        config = load_config()
        
        # Đọc logs gần đây từ file log mới nhất (theo thời gian chỉnh sửa)
        log_files = glob("logs/send_log_*.txt")
        log_files = sorted(log_files, key=os.path.getmtime, reverse=True)
        recent_logs = []
        if log_files:
            with open(log_files[0], 'r', encoding='utf-8') as f:
                recent_logs = f.readlines()[-10:]  # 10 dòng cuối
        
        # Đếm templates có sẵn
        template_files = list(Path("templates").glob("*.html"))
        
        # Đọc recipients
        recipients = []
        try:
            recipients = read_recipients(config['email']['recipients_csv'])
        except:
            pass
            
        stats = {
            'total_templates': len(template_files),
            'total_recipients': len(recipients),
            'recent_logs': recent_logs
        }
        
        return render_template('dashboard.html', config=config, stats=stats)
    except Exception as e:
        flash(f'Lỗi tải dashboard: {str(e)}', 'error')
        return render_template('dashboard.html', config={}, stats={})

@app.route('/templates')
def templates():
    """Quản lý templates"""
    try:
        template_files = []
        templates_dir = Path("templates")

        # Ensure templates directory exists
        templates_dir.mkdir(exist_ok=True)

        for template_file in templates_dir.glob("*.html"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    template_files.append({
                        'name': template_file.name,
                        'path': str(template_file),
                        'size': len(content),
                        'preview': content[:200] + '...' if len(content) > 200 else content
                    })
            except Exception as e:
                print(f"Error reading template {template_file}: {e}")
                # Add template with error info
                template_files.append({
                    'name': template_file.name,
                    'path': str(template_file),
                    'size': 0,
                    'preview': f'Error reading file: {str(e)}'
                })

        return render_template('templates.html', templates=template_files)
    except Exception as e:
        flash(f'Lỗi tải templates: {str(e)}', 'error')
        return render_template('templates.html', templates=[])

@app.route('/preview/<template_name>')
def preview_template(template_name):
    """Preview template với sample data"""
    try:
        template_path = Path("templates") / template_name
        if not template_path.exists():
            flash('Template không tồn tại', 'error')
            return redirect(url_for('templates'))
        
        # Sample data cho preview
        sample_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'product_name': 'Sample Product',
            'discount_code': 'PREVIEW20',
            'ip': '192.168.1.1',
            'location': 'Ho Chi Minh City, Vietnam',
            'device': 'Chrome on Windows',
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'security_url': 'https://example.com/security',
            'verification_url': 'https://example.com/verify',
            'reset_url': 'https://example.com/reset',
            'amount': '$99.99',
            'invoice_number': 'INV-2024-001',
            'company_name': 'Your Company'
        }
        
        template = load_template(template_path)
        rendered_html = template.render(**sample_data)
        
        return render_template('preview.html', 
                             template_name=template_name, 
                             rendered_html=rendered_html,
                             sample_data=sample_data)
    except Exception as e:
        flash(f'Lỗi preview template: {str(e)}', 'error')
        return redirect(url_for('templates'))

@app.route('/recipients')
def recipients():
    """Quản lý danh sách người nhận"""
    try:
        config = load_config()
        recipients_data = read_recipients(config['email']['recipients_csv'])
        
        # Lấy headers từ CSV
        csv_path = config['email']['recipients_csv']
        headers = []
        if Path(csv_path).exists():
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader, [])
        
        return render_template('recipients.html', 
                             recipients=recipients_data, 
                             headers=headers,
                             csv_path=csv_path)
    except Exception as e:
        flash(f'Lỗi tải danh sách người nhận: {str(e)}', 'error')
        return render_template('recipients.html', recipients=[], headers=[])

@app.route('/config')
def config():
    """Cấu hình SMTP và email"""
    try:
        config_data = load_config()
        return render_template('config.html', config=config_data)
    except Exception as e:
        flash(f'Lỗi tải cấu hình: {str(e)}', 'error')
        return render_template('config.html', config={})

@app.route('/send', methods=['GET', 'POST'])
def send_emails():
    """Gửi email"""
    if request.method == 'GET':
        try:
            config = load_config()
            recipients_data = read_recipients(config['email']['recipients_csv'])
            template_files = list(Path("templates").glob("*.html"))
            
            return render_template('send.html', 
                                 config=config,
                                 recipients=recipients_data,
                                 templates=[t.name for t in template_files])
        except Exception as e:
            flash(f'Lỗi tải trang gửi email: {str(e)}', 'error')
            return render_template('send.html', config={}, recipients=[], templates=[])
    
    # POST request - thực hiện gửi email
    try:
        config = load_config()
        smtp_config = config['smtp']
        sender_info = config['sender']
        
        # Lấy thông tin từ form
        template_name = request.form.get('template')
        subject = request.form.get('subject')
        selected_recipients = request.form.getlist('recipients')
        
        if not template_name or not subject:
            flash('Vui lòng chọn template và nhập subject', 'error')
            return redirect(url_for('send_emails'))
        
        # Load template
        template_path = Path("templates") / template_name
        html_template = load_template(template_path)
        
        # Load recipients
        all_recipients = read_recipients(config['email']['recipients_csv'])
        
        # Filter recipients nếu có chọn cụ thể
        if selected_recipients:
            recipients_to_send = [r for r in all_recipients if r['email'] in selected_recipients]
        else:
            recipients_to_send = all_recipients
        
        success = 0
        fail = 0
        
        # Log file
        log_file = Path("logs") / f"send_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(log_file, "w", encoding="utf-8") as log:
            log.write(f"Email Campaign Started: {datetime.now()}\n")
            log.write(f"Template: {template_name}\n")
            log.write(f"Subject: {subject}\n")
            log.write(f"Recipients: {len(recipients_to_send)}\n")
            log.write("-" * 50 + "\n")
            
            for recipient in recipients_to_send:
                try:
                    send_email(smtp_config, sender_info, recipient, subject, html_template, [])
                    log.write(f"✅ Sent to {recipient['email']}\n")
                    success += 1
                except Exception as e:
                    log.write(f"❌ Failed to {recipient['email']}: {e}\n")
                    fail += 1
            
            log.write("-" * 50 + "\n")
            log.write(f"Campaign Completed: {datetime.now()}\n")
            log.write(f"Success: {success}, Failures: {fail}\n")
        
        flash(f'Hoàn thành! Thành công: {success}, Thất bại: {fail}', 'success')
        return redirect(url_for('send_emails'))
        
    except Exception as e:
        flash(f'Lỗi gửi email: {str(e)}', 'error')
        return redirect(url_for('send_emails'))

@app.route('/test-smtp', methods=['POST'])
def test_smtp():
    """Test kết nối SMTP"""
    try:
        config = load_config()
        smtp_config = config['smtp']

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
            server.starttls(context=context)
            server.login(smtp_config['username'], smtp_config['password'])

        return jsonify({'success': True, 'message': 'Kết nối SMTP thành công!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi kết nối SMTP: {str(e)}'})

@app.route('/api/template/<template_name>')
def get_template_content(template_name):
    """API để lấy nội dung template"""
    try:
        template_path = Path("templates") / template_name
        if not template_path.exists():
            return "Template không tồn tại", 404

        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Lỗi đọc template: {str(e)}", 500

@app.route('/api/save-template', methods=['POST'])
def save_template_api():
    """API để lưu template"""
    try:
        data = request.get_json()
        template_name = data.get('name')
        content = data.get('content')

        if not template_name or not content:
            return jsonify({'success': False, 'message': 'Thiếu tên template hoặc nội dung'})

        # Ensure template name ends with .html
        if not template_name.endswith('.html'):
            template_name += '.html'

        template_path = Path("templates") / template_name

        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return jsonify({'success': True, 'message': 'Template đã được lưu thành công!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi lưu template: {str(e)}'})

@app.route('/api/save-recipients', methods=['POST'])
def save_recipients_api():
    """API để lưu danh sách người nhận"""
    try:
        data = request.get_json()
        recipients_data = data.get('recipients', [])

        config = load_config()
        csv_path = config['email']['recipients_csv']

        # Ensure data directory exists
        Path(csv_path).parent.mkdir(exist_ok=True)

        # Write to CSV
        if recipients_data:
            headers = list(recipients_data[0].keys())
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                writer.writerows(recipients_data)

        return jsonify({'success': True, 'message': 'Đã lưu danh sách người nhận thành công!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi lưu danh sách: {str(e)}'})

@app.route('/api/import-csv', methods=['POST'])
def import_csv_api():
    """API để import CSV"""
    try:
        if 'csv_file' not in request.files:
            return jsonify({'success': False, 'message': 'Không có file được upload'})

        file = request.files['csv_file']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'Không có file được chọn'})

        # Read CSV content
        content = file.read().decode('utf-8')
        csv_reader = csv.DictReader(content.splitlines())
        recipients_data = list(csv_reader)

        # Validate required fields
        if not recipients_data:
            return jsonify({'success': False, 'message': 'File CSV trống'})

        required_fields = ['email', 'name']
        first_row = recipients_data[0]
        missing_fields = [field for field in required_fields if field not in first_row]

        if missing_fields:
            return jsonify({'success': False, 'message': f'Thiếu các trường bắt buộc: {", ".join(missing_fields)}'})

        # Save to current CSV file
        config = load_config()
        csv_path = config['email']['recipients_csv']

        Path(csv_path).parent.mkdir(exist_ok=True)

        headers = list(first_row.keys())
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(recipients_data)

        return jsonify({'success': True, 'message': f'Import thành công {len(recipients_data)} người nhận!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi import CSV: {str(e)}'})

@app.route('/api/export-csv')
def export_csv_api():
    """API để export CSV"""
    try:
        config = load_config()
        csv_path = config['email']['recipients_csv']

        if not Path(csv_path).exists():
            return "File CSV không tồn tại", 404

        return send_file(csv_path, as_attachment=True, download_name='recipients_export.csv')
    except Exception as e:
        return f"Lỗi export CSV: {str(e)}", 500

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_file('static/favicon.svg', mimetype='image/svg+xml')

@app.route('/api/save-config', methods=['POST'])
def save_config_api():
    """API để lưu cấu hình"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['smtp', 'sender', 'email']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'Thiếu trường {field}'})

        # Create config structure
        config = {
            'smtp': {
                'host': data['smtp'].get('host', ''),
                'port': data['smtp'].get('port', 587),
                'username': data['smtp'].get('username', ''),
                'password': data['smtp'].get('password', '')
            },
            'sender': {
                'name': data['sender'].get('name', ''),
                'email': data['sender'].get('email', '')
            },
            'email': {
                'subject': data['email'].get('subject', 'Hello {{name}}!'),
                'template_path': data['email'].get('template_path', 'templates/default.html'),
                'recipients_csv': data['email'].get('recipients_csv', 'data/recipients.csv')
            },
            'attachments': []
        }

        # Save to config.yaml
        with open('config.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

        return jsonify({'success': True, 'message': 'Cấu hình đã được lưu thành công!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Lỗi lưu cấu hình: {str(e)}'})

@app.route('/download-log')
def download_log():
    """Download the latest log file"""
    try:
        log_file = Path("logs/send_log.txt")
        if not log_file.exists():
            flash('Không tìm thấy file log', 'error')
            return redirect(url_for('index'))
            
        return send_file(
            log_file,
            as_attachment=True,
            download_name=f'send_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt',
            mimetype='text/plain'
        )
    except Exception as e:
        flash(f'Lỗi tải file log: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
