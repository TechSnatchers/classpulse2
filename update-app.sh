#!/bin/bash
# Update Application Script
# Run this after pushing new code to update the deployed application

set -e

echo "=========================================="
echo "  Updating Learning Platform"
echo "=========================================="

APP_DIR="/var/www/learning-platform"
BACKEND_DIR="$APP_DIR/backend"
FRONTEND_DIR="$APP_DIR/frontend"

# Navigate to app directory
cd $APP_DIR

# Pull latest code
echo ""
echo "Step 1: Pulling latest code..."
if [ -d ".git" ]; then
    git pull
else
    echo "Warning: Not a git repository. Make sure code is updated manually."
    read -p "Press Enter to continue..."
fi

# Update Backend
echo ""
echo "Step 2: Updating backend..."
cd $BACKEND_DIR

# Activate virtual environment
source venv/bin/activate

# Update dependencies
echo "Installing/updating Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Restart backend service
echo "Restarting backend service..."
sudo systemctl restart learning-platform-backend

# Check if backend started successfully
sleep 3
if sudo systemctl is-active --quiet learning-platform-backend; then
    echo "✓ Backend restarted successfully"
else
    echo "✗ Backend failed to start. Checking logs..."
    sudo journalctl -u learning-platform-backend -n 20
    exit 1
fi

# Update Frontend
echo ""
echo "Step 3: Updating frontend..."
cd $FRONTEND_DIR

# Install/update dependencies
echo "Installing/updating npm dependencies..."
npm install

# Build for production
echo "Building frontend..."
npm run build

# Copy to nginx directory
echo "Deploying frontend files..."
sudo cp -r dist/* /var/www/learning-platform-frontend/
sudo chown -R www-data:www-data /var/www/learning-platform-frontend

# Reload nginx
echo "Reloading Nginx..."
sudo systemctl reload nginx

# Completion
echo ""
echo "=========================================="
echo "  Update Complete!"
echo "=========================================="
echo ""
echo "Services status:"
sudo systemctl status learning-platform-backend --no-pager | head -5
echo ""
sudo systemctl status nginx --no-pager | head -5
echo ""
echo "View backend logs: sudo journalctl -u learning-platform-backend -f"
echo ""

