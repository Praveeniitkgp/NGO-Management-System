#!/usr/bin/env python3
"""
Security Testing Script
Tests login and password reset functionality
"""
import os
import sys

# Set environment variables before Django setup
if not os.getenv('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'test-secret-key-for-testing-only'
if not os.getenv('DEBUG'):
    os.environ['DEBUG'] = 'True'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ngomanagement.settings')

import django
django.setup()

from core.models import Admin, RegisteredDonor
from django.contrib.auth.hashers import is_password_usable

def test_password_hashing():
    """Test that passwords are properly hashed"""
    print("=" * 60)
    print("Testing Password Hashing")
    print("=" * 60)
    
    admin_count = 0
    donor_count = 0
    unhashed_admins = []
    unhashed_donors = []
    
    for admin in Admin.objects.all():
        if admin.password_plaintext:
            if is_password_usable(admin.password_plaintext):
                admin_count += 1
            else:
                unhashed_admins.append(admin.email)
    
    for donor in RegisteredDonor.objects.all():
        if donor.password_plaintext:
            if is_password_usable(donor.password_plaintext):
                donor_count += 1
            else:
                unhashed_donors.append(donor.email)
    
    print(f"\n[OK] Hashed Admin Passwords: {admin_count}")
    print(f"[OK] Hashed Donor Passwords: {donor_count}")
    
    if unhashed_admins:
        print(f"\n[!] WARNING: {len(unhashed_admins)} admin(s) with unhashed passwords:")
        for email in unhashed_admins:
            print(f"  - {email}")
    
    if unhashed_donors:
        print(f"\n[!] WARNING: {len(unhashed_donors)} donor(s) with unhashed passwords:")
        for email in unhashed_donors[:5]:  # Show first 5
            print(f"  - {email}")
        if len(unhashed_donors) > 5:
            print(f"  ... and {len(unhashed_donors) - 5} more")
    
    return len(unhashed_admins) == 0 and len(unhashed_donors) == 0

def test_login_functionality():
    """Test login functionality"""
    print("\n" + "=" * 60)
    print("Testing Login Functionality")
    print("=" * 60)
    
    test_results = []
    
    # Test admin login
    try:
        admin = Admin.objects.first()
        if admin:
            test_password = "TestPassword123!"
            admin.set_password(test_password)
            admin.save()
            
            if admin.check_password(test_password):
                print("[OK] Admin password check works correctly")
                test_results.append(True)
            else:
                print("[X] Admin password check failed")
                test_results.append(False)
            
            if not admin.check_password("WrongPassword"):
                print("[OK] Admin password rejection works correctly")
                test_results.append(True)
            else:
                print("[X] Admin password rejection failed")
                test_results.append(False)
    except Exception as e:
        print(f"[X] Admin login test failed: {e}")
        test_results.append(False)
    
    # Test donor login
    try:
        donor = RegisteredDonor.objects.first()
        if donor:
            test_password = "TestPassword123!"
            donor.set_password(test_password)
            donor.save()
            
            if donor.check_password(test_password):
                print("[OK] Donor password check works correctly")
                test_results.append(True)
            else:
                print("[X] Donor password check failed")
                test_results.append(False)
            
            if not donor.check_password("WrongPassword"):
                print("[OK] Donor password rejection works correctly")
                test_results.append(True)
            else:
                print("[X] Donor password rejection failed")
                test_results.append(False)
    except Exception as e:
        print(f"[X] Donor login test failed: {e}")
        test_results.append(False)
    
    return all(test_results)

def test_password_reset():
    """Test password reset functionality"""
    print("\n" + "=" * 60)
    print("Testing Password Reset Functionality")
    print("=" * 60)
    
    test_results = []
    
    try:
        admin = Admin.objects.first()
        if admin:
            old_password_hash = admin.password_plaintext
            new_password = "NewPassword123!"
            
            admin.set_password(new_password)
            admin.save()
            
            if admin.password_plaintext != old_password_hash:
                print("[OK] Admin password reset updates hash")
                test_results.append(True)
            else:
                print("[X] Admin password reset did not update hash")
                test_results.append(False)
            
            if admin.check_password(new_password):
                print("[OK] Admin can login with new password")
                test_results.append(True)
            else:
                print("[X] Admin cannot login with new password")
                test_results.append(False)
            
            if not admin.check_password("OldPassword"):
                print("[OK] Admin cannot login with old password")
                test_results.append(True)
            else:
                print("[X] Admin can still login with old password")
                test_results.append(False)
    except Exception as e:
        print(f"[X] Admin password reset test failed: {e}")
        test_results.append(False)
    
    try:
        donor = RegisteredDonor.objects.first()
        if donor:
            old_password_hash = donor.password_plaintext
            new_password = "NewPassword123!"
            
            donor.set_password(new_password)
            donor.save()
            
            if donor.password_plaintext != old_password_hash:
                print("[OK] Donor password reset updates hash")
                test_results.append(True)
            else:
                print("[X] Donor password reset did not update hash")
                test_results.append(False)
            
            if donor.check_password(new_password):
                print("[OK] Donor can login with new password")
                test_results.append(True)
            else:
                print("[X] Donor cannot login with new password")
                test_results.append(False)
    except Exception as e:
        print(f"[X] Donor password reset test failed: {e}")
        test_results.append(False)
    
    return all(test_results)

def test_environment_variables():
    """Test that required environment variables are set"""
    print("\n" + "=" * 60)
    print("Testing Environment Variables")
    print("=" * 60)
    
    from django.conf import settings
    
    test_results = []
    
    # Check SECRET_KEY
    if settings.SECRET_KEY and settings.SECRET_KEY != 'django-insecure-ngoms-dev-key-change-in-production':
        print("[OK] SECRET_KEY is set and not using default")
        test_results.append(True)
    else:
        print("[!] SECRET_KEY is using default or not set properly")
        test_results.append(False)
    
    # Check DEBUG
    if not settings.DEBUG:
        print("[OK] DEBUG is set to False (production mode)")
        test_results.append(True)
    else:
        print("[!] DEBUG is set to True (development mode)")
        test_results.append(False)
    
    # Check security settings
    if not settings.DEBUG:
        if hasattr(settings, 'SECURE_SSL_REDIRECT') and settings.SECURE_SSL_REDIRECT:
            print("[OK] SECURE_SSL_REDIRECT is enabled")
            test_results.append(True)
        else:
            print("[!] SECURE_SSL_REDIRECT is not enabled")
            test_results.append(False)
        
        if hasattr(settings, 'SESSION_COOKIE_SECURE') and settings.SESSION_COOKIE_SECURE:
            print("[OK] SESSION_COOKIE_SECURE is enabled")
            test_results.append(True)
        else:
            print("[!] SESSION_COOKIE_SECURE is not enabled")
            test_results.append(False)
    
    return all(test_results)

def main():
    """Run all security tests"""
    print("\n" + "=" * 60)
    print("NGO Management System - Security Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("Password Hashing", test_password_hashing()))
    results.append(("Login Functionality", test_login_functionality()))
    results.append(("Password Reset", test_password_reset()))
    results.append(("Environment Variables", test_environment_variables()))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for test_name, result in results:
        status = "[OK] PASS" if result else "[X] FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("[OK] All security tests passed!")
        return 0
    else:
        print("[X] Some security tests failed. Please review the output above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

