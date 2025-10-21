#!/usr/bin/env python3
"""
Setup script for Consensus API to CSV Exporter
This script helps new users set up their environment file.
"""

import os
import shutil

def setup_environment():
    """Set up the environment file from the example."""
    
    print("🔧 Setting up Consensus API to CSV Exporter")
    print("=" * 50)
    
    # Check if .env already exists
    if os.path.exists('.env'):
        response = input("⚠️  .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Copy .env.example to .env
    if os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file from template")
    else:
        print("❌ .env.example file not found!")
        return
    
    print("\n📝 Next steps:")
    print("1. Edit the .env file with your API credentials:")
    print("   - API_KEY: Your Consensus API key")
    print("   - API_SECRET: Your API secret")
    print("   - API_EMAIL: Your email address")
    print("\n2. Install dependencies:")
    print("   python -m pip install -r requirements.txt")
    print("\n3. Run the application:")
    print("   python main.py")
    
    print("\n🔒 Security reminder:")
    print("   Never commit the .env file to version control!")
    print("   It contains sensitive API credentials.")

if __name__ == "__main__":
    setup_environment()