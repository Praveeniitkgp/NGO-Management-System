#!/bin/bash

# Setup .env file with production settings
# This script configures the .env file with SECRET_KEY and DEBUG settings

set -e

ENV_FILE=".env"
BACKUP_FILE=".env.backup"

echo "=========================================="
echo "Environment Configuration Setup"
echo "=========================================="
echo ""

# Backup existing .env if it exists
if [ -f "$ENV_FILE" ]; then
    echo "Backing up existing .env file..."
    cp "$ENV_FILE" "$BACKUP_FILE"
    echo "Backup saved to $BACKUP_FILE"
    echo ""
fi

# Generate SECRET_KEY if not provided
if [ -z "$SECRET_KEY" ]; then
    echo "Generating SECRET_KEY..."
    if command -v python3 &> /dev/null; then
        SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    else
        echo "Python3 not found. Please install Python3 or set SECRET_KEY manually."
        exit 1
    fi
fi

# Read existing .env file if it exists
EMAIL_HOST_USER=""
EMAIL_HOST_PASSWORD=""

if [ -f "$ENV_FILE" ]; then
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        [[ "$key" =~ ^#.*$ ]] && continue
        [[ -z "$key" ]] && continue
        
        # Extract values
        if [[ "$key" == "EMAIL_HOST_USER" ]]; then
            EMAIL_HOST_USER="$value"
        elif [[ "$key" == "EMAIL_HOST_PASSWORD" ]]; then
            EMAIL_HOST_PASSWORD="$value"
        fi
    done < "$ENV_FILE"
fi

# If email config not found, prompt user
if [ -z "$EMAIL_HOST_USER" ]; then
    echo "Please enter your email address:"
    read -r EMAIL_HOST_USER
fi

if [ -z "$EMAIL_HOST_PASSWORD" ]; then
    echo "Please enter your email app password:"
    read -r EMAIL_HOST_PASSWORD
fi

# Write new .env file
cat > "$ENV_FILE" << EOF
# Production Settings
DEBUG=False
SECRET_KEY=$SECRET_KEY
ALLOWED_HOSTS=praveenpatel.dev,www.praveenpatel.dev,139.59.10.76,localhost,127.0.0.1

# Email Configuration for OTP Password Reset
EMAIL_HOST_USER=$EMAIL_HOST_USER
EMAIL_HOST_PASSWORD="$EMAIL_HOST_PASSWORD"
EOF

echo "✓ .env file configured successfully!"
echo ""
echo "Configuration:"
echo "  DEBUG=False"
echo "  SECRET_KEY=*** (hidden)"
echo "  ALLOWED_HOSTS=praveenpatel.dev,www.praveenpatel.dev,139.59.10.76,localhost,127.0.0.1"
echo "  EMAIL_HOST_USER=$EMAIL_HOST_USER"
echo ""
echo "Next steps:"
echo "  1. Review the .env file: cat .env"
echo "  2. Run security tests: python test_security.py"
echo "  3. For production server, run: ./configure_ssl.sh"
echo ""

