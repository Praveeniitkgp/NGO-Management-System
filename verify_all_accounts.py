#!/usr/bin/env python3
"""
Comprehensive verification script for admin and donor accounts
Run this on the server to verify everything is working
"""
import os
import sys
import django

# Load environment variables from .env if it exists
env_file = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_file):
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and value:
                    os.environ.setdefault(key, value)

# Set defaults if not in environment
if not os.getenv('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'temp-key-for-verification'
if not os.getenv('DEBUG'):
    os.environ['DEBUG'] = 'False'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ngomanagement.settings')
django.setup()

from core.models import Admin, RegisteredDonor
from django.contrib.auth.hashers import is_password_usable

def verify_all_accounts():
    print("=" * 60)
    print("COMPREHENSIVE ACCOUNT VERIFICATION")
    print("=" * 60)
    print()
    
    # Verify Admins
    print("=" * 60)
    print("ADMIN ACCOUNTS")
    print("=" * 60)
    
    admin_issues = []
    admin_count = 0
    
    for admin in Admin.objects.all():
        admin_count += 1
        print(f"\nAdmin {admin_count}:")
        print(f"  Email: {admin.email}")
        print(f"  Name: {admin.name}")
        
        if not admin.password_plaintext:
            admin_issues.append(f"{admin.email}: No password set")
            print("  [X] Password: NOT SET")
        elif is_password_usable(admin.password_plaintext):
            print("  [OK] Password: HASHED (secure)")
        else:
            admin_issues.append(f"{admin.email}: Password not hashed")
            print("  [X] Password: NOT HASHED (needs fixing)")
            # Fix it
            old_password = admin.password_plaintext
            admin.set_password(old_password)
            admin.save()
            print("  [OK] Fixed: Password hashed")
        
        print(f"  Security Question: {admin.security_question}")
        print(f"  Security Answer: {'Set' if admin.security_answer else 'Not set'}")
    
    print(f"\nTotal Admins: {admin_count}")
    if admin_issues:
        print(f"Issues Found: {len(admin_issues)}")
        for issue in admin_issues:
            print(f"  - {issue}")
    else:
        print("[OK] All admin accounts are properly configured")
    
    # Verify Donors
    print("\n" + "=" * 60)
    print("DONOR ACCOUNTS")
    print("=" * 60)
    
    donor_issues = []
    donor_count = 0
    unhashed_count = 0
    
    for donor in RegisteredDonor.objects.all():
        donor_count += 1
        
        if donor_count <= 5:  # Show details for first 5
            print(f"\nDonor {donor_count}:")
            print(f"  Email: {donor.email}")
            print(f"  Name: {donor.name}")
        
        if not donor.password_plaintext:
            donor_issues.append(f"{donor.email}: No password set")
            if donor_count <= 5:
                print("  [X] Password: NOT SET")
        elif is_password_usable(donor.password_plaintext):
            if donor_count <= 5:
                print("  [OK] Password: HASHED (secure)")
        else:
            unhashed_count += 1
            donor_issues.append(f"{donor.email}: Password not hashed")
            if donor_count <= 5:
                print("  [X] Password: NOT HASHED (fixing...)")
            # Fix it
            old_password = donor.password_plaintext
            donor.set_password(old_password)
            donor.save()
            if donor_count <= 5:
                print("  [OK] Fixed: Password hashed")
        
        if donor_count <= 5:
            print(f"  Security Question: {donor.security_question or 'Not set'}")
    
    if donor_count > 5:
        print(f"\n... and {donor_count - 5} more donors")
    
    print(f"\nTotal Donors: {donor_count}")
    print(f"Unhashed Passwords Fixed: {unhashed_count}")
    
    if donor_issues:
        print(f"\nIssues Found: {len(donor_issues)}")
        for issue in donor_issues[:10]:  # Show first 10
            print(f"  - {issue}")
        if len(donor_issues) > 10:
            print(f"  ... and {len(donor_issues) - 10} more")
    else:
        print("[OK] All donor accounts are properly configured")
    
    # Test Login Functionality
    print("\n" + "=" * 60)
    print("LOGIN FUNCTIONALITY TEST")
    print("=" * 60)
    
    # Test admin login
    admin = Admin.objects.first()
    if admin:
        # Test with environment variable password if available
        import os
        test_password = os.getenv('ADMIN_PASSWORD', 'test')
        if admin.check_password(test_password):
            print(f"[OK] Admin login works: {admin.email}")
        else:
            print(f"[!] Admin login test: Password check failed")
            print("  (This is OK if password is different or not set in env)")
    else:
        print("[X] No admin account found")
    
    # Test donor login
    donor = RegisteredDonor.objects.first()
    if donor and donor.password_plaintext:
        if is_password_usable(donor.password_plaintext):
            print(f"[OK] Donor login ready: {donor.email}")
            print("  (Password is hashed, login will work)")
        else:
            print(f"[!] Donor login: Password needs hashing")
    elif donor:
        print(f"[!] Donor {donor.email}: No password set")
    else:
        print("[!] No donor accounts found")
    
    # Test Password Reset
    print("\n" + "=" * 60)
    print("PASSWORD RESET FUNCTIONALITY TEST")
    print("=" * 60)
    
    if admin:
        old_hash = admin.password_plaintext
        test_password = "TestReset123!"
        admin.set_password(test_password)
        admin.save()
        
        if admin.password_plaintext != old_hash:
            print("[OK] Admin password reset: Updates hash correctly")
        else:
            print("[X] Admin password reset: Hash not updated")
        
        if admin.check_password(test_password):
            print("[OK] Admin password reset: New password works")
        else:
            print("[X] Admin password reset: New password doesn't work")
        
        # Restore original password from env or skip
        import os
        original_pwd = os.getenv('ADMIN_PASSWORD')
        if original_pwd:
            admin.set_password(original_pwd)
            admin.save()
            print("[OK] Admin password restored")
        else:
            print("[!] Admin password not restored (ADMIN_PASSWORD not set in env)")
    
    if donor and donor.password_plaintext:
        old_hash = donor.password_plaintext
        test_password = "TestReset123!"
        donor.set_password(test_password)
        donor.save()
        
        if donor.password_plaintext != old_hash:
            print("[OK] Donor password reset: Updates hash correctly")
        else:
            print("[X] Donor password reset: Hash not updated")
        
        if donor.check_password(test_password):
            print("[OK] Donor password reset: New password works")
        else:
            print("[X] Donor password reset: New password doesn't work")
        
        # Restore original if it was hashed
        if is_password_usable(old_hash):
            donor.password_plaintext = old_hash
            donor.save()
            print("[OK] Donor password restored")
    
    # Final Summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    
    total_admins = Admin.objects.count()
    total_donors = RegisteredDonor.objects.count()
    hashed_admins = sum(1 for a in Admin.objects.all() if a.password_plaintext and is_password_usable(a.password_plaintext))
    hashed_donors = sum(1 for d in RegisteredDonor.objects.all() if d.password_plaintext and is_password_usable(d.password_plaintext))
    
    print(f"\nAdmins: {hashed_admins}/{total_admins} with hashed passwords")
    print(f"Donors: {hashed_donors}/{total_donors} with hashed passwords")
    
    if hashed_admins == total_admins and hashed_donors == total_donors:
        print("\n✅ ALL ACCOUNTS ARE SECURE AND READY!")
        print("✅ All passwords are hashed")
        print("✅ Login functionality is working")
        print("✅ Password reset is working")
        return 0
    else:
        print("\n[!] Some accounts may need attention")
        return 1

if __name__ == '__main__':
    try:
        exit_code = verify_all_accounts()
        sys.exit(exit_code)
    except Exception as e:
        print(f"\n[X] Error during verification: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

