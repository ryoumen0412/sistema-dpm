#!/usr/bin/env python3
"""
Quick test script to verify authentication
"""
import sys
sys.path.append('.')

from app.database import SessionLocal
from app.models.user import User
from app.crud.user import authenticate_user
from passlib.context import CryptContext

def test_auth():
    db = SessionLocal()
    
    try:
        print("🔍 Testing authentication system...")
        
        # Check users in database
        users = db.query(User).all()
        print(f"\n📋 Users in database: {len(users)}")
        for user in users:
            print(f"   - ID: {user.id}, Username: '{user.usr}'")
        
        # Test authentication with correct credentials
        print(f"\n🔐 Testing login with admin/admin123...")
        result = authenticate_user(db, "admin", "admin123")
        
        if result:
            print(f"✅ Authentication successful! User: {result.usr}")
        else:
            print("❌ Authentication failed!")
            
        # Test with wrong password
        print(f"\n🔐 Testing login with wrong password...")
        result = authenticate_user(db, "admin", "wrongpassword")
        
        if result:
            print(f"❌ This should have failed! User: {result.usr}")
        else:
            print("✅ Correctly rejected wrong password")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_auth()
