#!/usr/bin/env python3
"""
Test script to check if the Flask app can start without errors
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    try:
        print("Testing imports...")
        
        import flask
        print("✅ Flask imported")
        
        import yaml
        print("✅ PyYAML imported")
        
        import jinja2
        print("✅ Jinja2 imported")
        
        # Test app import
        sys.path.insert(0, os.getcwd())
        import app
        print("✅ App module imported")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_directories():
    """Test if required directories exist"""
    required_dirs = [
        "web_templates",
        "templates", 
        "static",
        "static/css",
        "static/js",
        "data",
        "logs"
    ]
    
    print("\nTesting directories...")
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"✅ {directory}")
        else:
            print(f"❌ {directory} - missing")
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"✅ {directory} - created")

def test_templates():
    """Test if required templates exist"""
    required_templates = [
        "web_templates/base.html",
        "web_templates/dashboard.html",
        "web_templates/templates.html",
        "web_templates/recipients.html",
        "web_templates/send.html",
        "web_templates/config.html",
        "web_templates/preview.html"
    ]
    
    print("\nTesting templates...")
    missing_templates = []
    for template in required_templates:
        if Path(template).exists():
            print(f"✅ {template}")
        else:
            print(f"❌ {template} - missing")
            missing_templates.append(template)
    
    return len(missing_templates) == 0

def test_config():
    """Test if config file exists or can be created"""
    config_file = Path("config.yaml")
    
    print("\nTesting config...")
    if config_file.exists():
        print("✅ config.yaml exists")
        try:
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            print("✅ config.yaml is valid YAML")
            return True
        except Exception as e:
            print(f"❌ config.yaml is invalid: {e}")
            return False
    else:
        print("⚠️  config.yaml not found - will be created on first run")
        return True

def main():
    """Main test function"""
    print("🧪 Testing Bulk HTML Mailer Setup")
    print("=" * 40)
    
    # Run tests
    imports_ok = test_imports()
    test_directories()
    templates_ok = test_templates()
    config_ok = test_config()
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    print(f"Imports: {'✅' if imports_ok else '❌'}")
    print(f"Templates: {'✅' if templates_ok else '❌'}")
    print(f"Config: {'✅' if config_ok else '❌'}")
    
    if imports_ok and templates_ok and config_ok:
        print("\n🎉 All tests passed! App should start successfully.")
        print("Run: python app.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
