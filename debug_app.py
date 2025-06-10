#!/usr/bin/env python3
"""
Debug script for Bulk HTML Mailer
Helps identify specific issues causing Internal Server Error
"""

import sys
import traceback
from pathlib import Path

def test_templates_route():
    """Test the templates route specifically"""
    print("🧪 Testing templates route...")
    
    try:
        # Import required modules
        from app import app
        
        # Create test client
        with app.test_client() as client:
            print("✅ App created successfully")
            
            # Test templates route
            response = client.get('/templates')
            print(f"📊 Response status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Templates route works!")
                return True
            else:
                print(f"❌ Templates route failed with status {response.status_code}")
                print(f"Response data: {response.data.decode()}")
                return False
                
    except Exception as e:
        print(f"❌ Error testing templates route: {e}")
        print("📋 Full traceback:")
        traceback.print_exc()
        return False

def test_template_files():
    """Test reading template files"""
    print("\n🧪 Testing template files...")
    
    templates_dir = Path("templates")
    if not templates_dir.exists():
        print("❌ Templates directory doesn't exist")
        return False
    
    template_files = list(templates_dir.glob("*.html"))
    print(f"📁 Found {len(template_files)} template files")
    
    for template_file in template_files:
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"✅ {template_file.name} - {len(content)} chars")
        except Exception as e:
            print(f"❌ {template_file.name} - Error: {e}")
            return False
    
    return True

def test_web_templates():
    """Test web templates"""
    print("\n🧪 Testing web templates...")
    
    web_templates_dir = Path("web_templates")
    if not web_templates_dir.exists():
        print("❌ Web templates directory doesn't exist")
        return False
    
    required_templates = [
        'base.html', 'dashboard.html', 'templates.html', 
        'recipients.html', 'send.html', 'config.html', 'preview.html'
    ]
    
    missing_templates = []
    for template_name in required_templates:
        template_path = web_templates_dir / template_name
        if template_path.exists():
            print(f"✅ {template_name}")
        else:
            print(f"❌ {template_name} - MISSING")
            missing_templates.append(template_name)
    
    return len(missing_templates) == 0

def test_imports():
    """Test all required imports"""
    print("\n🧪 Testing imports...")
    
    try:
        import flask
        print("✅ Flask")
        
        import yaml
        print("✅ PyYAML")
        
        import jinja2
        print("✅ Jinja2")
        
        from pathlib import Path
        print("✅ pathlib")
        
        import csv
        print("✅ csv")
        
        import smtplib
        print("✅ smtplib")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test config loading"""
    print("\n🧪 Testing config...")
    
    try:
        from mailer import load_config
        config = load_config()
        print("✅ Config loaded successfully")
        print(f"📊 Config keys: {list(config.keys())}")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def main():
    """Main debug function"""
    print("🐛 Bulk HTML Mailer Debug Tool")
    print("=" * 40)
    
    # Run all tests
    tests = [
        ("Imports", test_imports),
        ("Template Files", test_template_files),
        ("Web Templates", test_web_templates),
        ("Config", test_config),
        ("Templates Route", test_templates_route),
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            traceback.print_exc()
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DEBUG SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! The app should work.")
    else:
        print("⚠️  Some tests failed. Fix the issues above.")
        print("\n🔧 Suggested fixes:")
        print("1. Run: python fix_app.py")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Check file permissions")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
