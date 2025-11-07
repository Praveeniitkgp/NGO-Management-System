#!/bin/bash

# SSL Certificate Configuration Script
# This script configures SSL certificates using Let's Encrypt

set -e

echo "=========================================="
echo "SSL Certificate Configuration"
echo "=========================================="
echo ""

DOMAIN="praveenpatel.dev"
EMAIL="${SSL_EMAIL:-your-email@example.com}"

echo "Domain: $DOMAIN"
echo "Email: $EMAIL"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Install certbot if not already installed
if ! command -v certbot &> /dev/null; then
    echo "Installing Certbot..."
    apt update
    apt install -y certbot python3-certbot-nginx
fi

# Check if nginx is installed
if ! command -v nginx &> /dev/null; then
    echo "Nginx is not installed. Please install nginx first."
    exit 1
fi

# Ensure nginx configuration is ready
echo "Checking Nginx configuration..."
if [ ! -f /etc/nginx/sites-available/ngo-management ]; then
    echo "Nginx configuration file not found. Please run server_setup.sh first."
    exit 1
fi

# Test nginx configuration
echo "Testing Nginx configuration..."
nginx -t

# Obtain SSL certificate
echo ""
echo "Obtaining SSL certificate for $DOMAIN..."
certbot --nginx \
    -d $DOMAIN \
    -d www.$DOMAIN \
    --non-interactive \
    --agree-tos \
    --email $EMAIL \
    --redirect

# Set up automatic renewal
echo ""
echo "Setting up automatic certificate renewal..."
systemctl enable certbot.timer
systemctl start certbot.timer

# Test renewal
echo ""
echo "Testing certificate renewal..."
certbot renew --dry-run

echo ""
echo "=========================================="
echo "SSL Configuration Complete!"
echo "=========================================="
echo ""
echo "Your site should now be accessible at:"
echo "  https://$DOMAIN"
echo "  https://www.$DOMAIN"
echo ""
echo "Certificate will auto-renew via certbot.timer"
echo ""

