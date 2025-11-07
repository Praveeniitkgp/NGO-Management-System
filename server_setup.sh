#!/bin/bash

# Server setup script

set -e

echo "Setting up NGO Management System on server..."

echo "Installing system packages..."
apt update
apt install -y python3 python3-pip python3-venv nginx supervisor git postgresql postgresql-contrib

PROJECT_DIR="/var/www/ngo-management"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

if [ ! -f .env ]; then
    echo ".env file not found!"
    echo "Creating .env template..."
    cat > .env << 'ENVEOF'
# Production Settings
DEBUG=False
SECRET_KEY=CHANGE_THIS_TO_RANDOM_SECRET_KEY
ALLOWED_HOSTS=139.59.10.76

# Database (PostgreSQL)
DB_NAME=ngomanagement
DB_USER=django
DB_PASSWORD=CHANGE_THIS_PASSWORD

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
ENVEOF
    echo ".env template created. Please edit it with your actual values:"
    echo "   nano .env"
    echo ""
    read -p "Press Enter after you've edited .env file..."
fi

if grep -q "CHANGE_THIS_TO_RANDOM_SECRET_KEY" .env; then
    echo "Generating SECRET_KEY..."
    SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    sed -i "s/SECRET_KEY=CHANGE_THIS_TO_RANDOM_SECRET_KEY/SECRET_KEY=$SECRET_KEY/" .env
    echo "SECRET_KEY generated and saved"
fi

set -a
source .env
set +a

echo "Running database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Configuring Supervisor..."
cat > /etc/supervisor/conf.d/ngo-management.conf << 'SUPEREOF'
[program:ngo-management]
command=/var/www/ngo-management/venv/bin/gunicorn ngomanagement.wsgi:application --bind 127.0.0.1:8000
directory=/var/www/ngo-management
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/ngo-management.log
stderr_logfile=/var/log/ngo-management-error.log
SUPEREOF

supervisorctl reread
supervisorctl update
supervisorctl start ngo-management

echo "Configuring Nginx..."
cat > /etc/nginx/sites-available/ngo-management << 'NGINXEOF'
server {
    listen 80;
    server_name 139.59.10.76;

    location /static/ {
        alias /var/www/ngo-management/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINXEOF

ln -sf /etc/nginx/sites-available/ngo-management /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

echo "Configuring firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "   1. Verify .env file has correct values"
echo "   2. Check application status: supervisorctl status ngo-management"
echo "   3. Check logs: tail -f /var/log/ngo-management.log"
echo "   4. Visit: http://139.59.10.76"
echo ""

