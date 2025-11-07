#!/bin/bash

# Auto deploy to praveenpatel.dev

SERVER_IP="139.59.10.76"
SERVER_USER="root"
SERVER_PATH="/var/www/ngo-management"

echo "Starting Automated Deployment to praveenpatel.dev"
echo "=================================================="
echo ""

echo "Step 1: Deploying files to server..."
./deploy_to_server.sh

if [ $? -ne 0 ]; then
    echo "File deployment failed. Please check the error above."
    exit 1
fi

echo ""
echo "Files deployed successfully!"
echo ""

echo "Step 2: Connecting to server and running deployment steps..."
echo ""

ssh ${SERVER_USER}@${SERVER_IP} << 'ENDSSH'
    set -e
    
    echo "Navigating to project directory..."
    cd /var/www/ngo-management
    
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    echo ""
    echo "Step 3: Installing/updating dependencies..."
    pip install -q -r requirements.txt
    echo "Dependencies installed"
    echo ""
    
    echo "Step 4: Running database migrations..."
    python manage.py migrate
    echo "Migrations completed"
    echo ""
    
    echo "Step 5: Hashing existing passwords..."
    python manage.py shell << 'PYTHON_SCRIPT'
from core.models import Admin, RegisteredDonor
from django.contrib.auth.hashers import is_password_usable

admin_count = 0
donor_count = 0

for admin in Admin.objects.all():
    if admin.password_plaintext and not is_password_usable(admin.password_plaintext):
        admin.set_password(admin.password_plaintext)
        admin.save()
        admin_count += 1

for donor in RegisteredDonor.objects.all():
    if donor.password_plaintext and not is_password_usable(donor.password_plaintext):
        donor.set_password(donor.password_plaintext)
        donor.save()
        donor_count += 1

print(f'Hashed {admin_count} admin password(s)')
print(f'Hashed {donor_count} donor password(s)')
PYTHON_SCRIPT
    echo "Passwords hashed"
    echo ""
    
    echo "Step 6: Updating admin credentials..."
    python manage.py shell << 'PYTHON_SCRIPT'
import os
from core.models import Admin
admin_email = os.getenv('ADMIN_EMAIL', 'admin@brightfutures@gmail.com')
admin_password = os.getenv('ADMIN_PASSWORD', 'CHANGE_THIS_PASSWORD')
admin_security_answer = os.getenv('ADMIN_SECURITY_ANSWER', 'CHANGE_THIS_ANSWER')
Admin.objects.filter(email=admin_email).delete()
admin = Admin(
    name='Admin',
    email=admin_email,
    security_question='What is the name of your first pet?',
    security_answer=admin_security_answer
)
admin.set_password(admin_password)
admin.save()
print(f'Admin created: {admin.email}')
PYTHON_SCRIPT
    echo "Admin credentials updated"
    echo ""
    
    echo "Step 7: Updating existing donors with default security questions..."
    python manage.py shell << 'PYTHON_SCRIPT'
from core.models import RegisteredDonor
donors = RegisteredDonor.objects.filter(security_question__isnull=True) | RegisteredDonor.objects.filter(security_question='')
count = 0
for donor in donors:
    donor.security_question = 'What is your favorite color?'
    default_answer = donor.email.split('@')[0].lower()
    donor.security_answer = default_answer
    donor.save()
    count += 1
print(f'Updated {count} donor(s) with default security questions')
PYTHON_SCRIPT
    echo "Donors updated"
    echo ""
    
    echo "Step 8: Collecting static files..."
    python manage.py collectstatic --noinput
    echo "Static files collected"
    echo ""
    
    echo "Step 9: Verifying all accounts..."
    set -a
    source .env 2>/dev/null || true
    set +a
    python verify_all_accounts.py
    echo "Account verification completed"
    echo ""
    
    echo "Step 10: Restarting services..."
    sudo supervisorctl restart ngo-management
    sleep 2
    echo "Gunicorn restarted"
    
    sudo systemctl restart nginx
    sleep 1
    echo "Nginx restarted"
    echo ""
    
    echo "Service Status:"
    sudo supervisorctl status ngo-management | head -1
    sudo systemctl is-active nginx
    echo ""
    
    echo "Deployment Complete!"
ENDSSH

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "Deployment Successful!"
    echo ""
    echo "Next Steps:"
    echo "   1. Visit: https://praveenpatel.dev"
    echo "   2. Test admin login with credentials from .env file"
    echo "   3. Test forgot password functionality"
    echo ""
    echo "Your website is now live with all updates!"
else
    echo ""
    echo "Deployment failed. Please check the errors above."
    exit 1
fi

