#!/usr/bin/env python
import os
import sys

def setup_project():
    """Set up the Calculator Hub project"""
    
    print("🔧 Setting up Calculator Hub...")
    
    # Create directories
    directories = [
        'calculators/management',
        'calculators/management/commands',
        'static/css',
        'static/js',
        'static/images',
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Run Django commands
    commands = [
        'python manage.py makemigrations',
        'python manage.py migrate',
        'python manage.py setup_calculators',
    ]
    
    for command in commands:
        print(f"🚀 Running: {command}")
        os.system(command)
    
    print("✅ Setup complete!")
    print("🌐 Run 'python manage.py runserver' to start the development server")

if __name__ == "__main__":
    setup_project()