#!/bin/bash

# Upload code to server

SERVER_IP="139.59.10.76"
SERVER_USER="root"
SERVER_PATH="/var/www/ngo-management"

echo "Starting deployment to DigitalOcean server..."
echo "Server: ${SERVER_USER}@${SERVER_IP}"
echo ""

if [ -f .env ]; then
    echo "WARNING: .env file detected locally"
    echo "   This will NOT be uploaded (it's in .gitignore)"
    echo "   Make sure to create .env on the server manually"
    echo ""
fi

EXCLUDE_LIST=(
    ".env"
    ".env.local"
    "venv/"
    "__pycache__/"
    "*.pyc"
    "*.pyo"
    "*.pyd"
    ".git/"
    "db.sqlite3"
    "*.log"
    ".DS_Store"
    "node_modules/"
    ".vscode/"
    ".idea/"
)

EXCLUDE_ARGS=""
for item in "${EXCLUDE_LIST[@]}"; do
    EXCLUDE_ARGS="$EXCLUDE_ARGS --exclude=$item"
done

echo "Uploading files (excluding sensitive data)..."
echo ""

ssh ${SERVER_USER}@${SERVER_IP} "mkdir -p ${SERVER_PATH}"

rsync -avz --progress \
    $EXCLUDE_ARGS \
    --exclude='.git' \
    --exclude='*.sqlite3' \
    --exclude='*.log' \
    ./ ${SERVER_USER}@${SERVER_IP}:${SERVER_PATH}/

if [ $? -eq 0 ]; then
    echo ""
    echo "Files uploaded successfully!"
    echo ""
    echo "Next steps on the server:"
    echo "   1. SSH to server: ssh ${SERVER_USER}@${SERVER_IP}"
    echo "   2. Create .env file: cd ${SERVER_PATH} && nano .env"
    echo "   3. Setup virtual environment: python3 -m venv venv"
    echo "   4. Install dependencies: source venv/bin/activate && pip install -r requirements.txt"
    echo "   5. Run migrations: python manage.py migrate"
    echo "   6. Collect static files: python manage.py collectstatic --noinput"
    echo "   7. Setup Gunicorn and Nginx (see DEPLOY.md)"
    echo ""
else
    echo ""
    echo "Upload failed. Please check the error above."
    exit 1
fi

