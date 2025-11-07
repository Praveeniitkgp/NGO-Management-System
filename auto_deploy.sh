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
    
    echo "Step 5: Updating admin credentials..."
    python manage.py shell << 'PYTHON_SCRIPT'
from core.models import Admin
Admin.objects.filter(email='admin@brightfutures@gmail.com').delete()
admin = Admin.objects.create(
    name='Admin',
    email='admin@brightfutures@gmail.com',
    password_plaintext='Myadminme@110',
    security_question='What is the name of your first pet?',
    security_answer='memyself'
)
print(f'Admin created: {admin.email}')
print(f'   Security Answer: {admin.security_answer}')
PYTHON_SCRIPT
    echo "Admin credentials updated"
    echo ""
    
    echo "Step 6: Updating existing donors with default security questions..."
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
    
    echo "Step 7: Collecting static files..."
    python manage.py collectstatic --noinput
    echo "Static files collected"
    echo ""
    
    echo "Step 8: Restarting services..."
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
    echo "   2. Test admin login:"
    echo "      Email: admin@brightfutures@gmail.com"
    echo "      Password: Myadminme@110"
    echo "   3. Test forgot password (security answer: memyself)"
    echo ""
    echo "Your website is now live with all updates!"
else
    echo ""
    echo "Deployment failed. Please check the errors above."
    exit 1
fi

