#!/usr/bin/env python3
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ngomanagement.settings')

import django
django.setup()

from core.models import Admin, RegisteredDonor
from django.contrib.auth.hashers import is_password_usable

def hash_existing_passwords():
    print("Starting password hashing migration...")
    
    admin_count = 0
    donor_count = 0
    
    for admin in Admin.objects.all():
        current_password = admin.password_plaintext
        if current_password and not is_password_usable(current_password):
            admin.set_password(current_password)
            admin.save()
            admin_count += 1
            print(f"Hashed password for admin: {admin.email}")
    
    for donor in RegisteredDonor.objects.all():
        current_password = donor.password_plaintext
        if current_password and not is_password_usable(current_password):
            donor.set_password(current_password)
            donor.save()
            donor_count += 1
            print(f"Hashed password for donor: {donor.email}")
    
    print(f"\nMigration complete!")
    print(f"Hashed {admin_count} admin password(s)")
    print(f"Hashed {donor_count} donor password(s)")

if __name__ == '__main__':
    hash_existing_passwords()

