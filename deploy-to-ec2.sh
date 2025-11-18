#!/bin/bash
# Main Deployment Script for EC2
# This script deploys both backend and frontend

set -e

echo "=========================================="
echo "  Deploying Learning Platform to EC2"
echo "=========================================="

# Configuration
APP_DIR="/var/www/learning-platform"
BACKEND_DIR="$APP_DIR/backend"
FRONTEND_DIR="$APP_DIR/frontend"
NGINX_CONFIG="/etc/nginx/sites-available/learning-platform"

# Get domain or use IP
echo ""
read -p "Enter your domain name (or press Enter to use EC2 IP): " DOMAIN
if [ -z "$DOMAIN" ]; then
    DOMAIN=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
    echo "Using EC2 IP: $DOMAIN"
fi

# Backend MongoDB Configuration
echo ""
echo "MongoDB Configuration:"
echo "1. Local MongoDB (mongodb://localhost:27017)"
echo "2. MongoDB Atlas (cloud)"
read -p "Choose option (1 or 2): " mongo_option

if [ "$mongo_option" = "2" ]; then
    read -p "Enter MongoDB Atlas connection string: " MONGODB_URL
else
    MONGODB_URL="mongodb://localhost:27017"
fi

# Navigate to app directory
cd $APP_DIR

# Pull latest code (if using git)
if [ -d ".git" ]; then
    echo ""
    echo "Step 1: Pulling latest code from git..."
    git pull origin main || git pull origin master
else
    echo ""
    echo "Warning: Not a git repository. Make sure code is up to date."
fi

# ===================================
# Backend Deployment
# ===================================
echo ""
echo "=========================================="
echo "  Deploying Backend"
echo "=========================================="

cd $BACKEND_DIR

# Create Python virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
echo "Creating backend .env file..."
cat > .env <<EOF
# MongoDB Configuration
MONGODB_URL=$MONGODB_URL
DATABASE_NAME=learning_platform

# Server Configuration
PORT=3001
FRONTEND_URL=http://$DOMAIN

# Domain Configuration
DOMAIN=$DOMAIN
BASE_URL=http://$DOMAIN
EOF

echo "Backend .env file created"

# Create systemd service for backend
echo "Creating systemd service for backend..."
sudo tee /etc/systemd/system/learning-platform-backend.service > /dev/null <<EOF
[Unit]
Description=Learning Platform Backend API
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$BACKEND_DIR
Environment="PATH=$BACKEND_DIR/venv/bin"
ExecStart=$BACKEND_DIR/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start backend service
sudo systemctl daemon-reload
sudo systemctl enable learning-platform-backend
sudo systemctl restart learning-platform-backend

echo "Backend service started"

# ===================================
# Frontend Deployment
# ===================================
echo ""
echo "=========================================="
echo "  Deploying Frontend"
echo "=========================================="

cd $FRONTEND_DIR

# Install npm dependencies
echo "Installing frontend dependencies..."
npm install

# Create production environment file
echo "Creating frontend environment configuration..."
cat > .env.production <<EOF
VITE_API_URL=http://$DOMAIN:3001
EOF

# Build frontend for production
echo "Building frontend for production..."
npm run build

# Copy build to nginx directory
echo "Copying build files to nginx..."
sudo mkdir -p /var/www/learning-platform-frontend
sudo cp -r dist/* /var/www/learning-platform-frontend/
sudo chown -R www-data:www-data /var/www/learning-platform-frontend

# ===================================
# Nginx Configuration
# ===================================
echo ""
echo "=========================================="
echo "  Configuring Nginx"
echo "=========================================="

# Create Nginx configuration
sudo tee $NGINX_CONFIG > /dev/null <<'EOF'
server {
    listen 80;
    server_name SERVER_NAME_PLACEHOLDER;

    # Frontend
    location / {
        root /var/www/learning-platform-frontend;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend health check
    location /health {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }

    # Backend docs
    location /docs {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }

    location /redoc {
        proxy_pass http://localhost:3001;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }
}
EOF

# Replace server name
sudo sed -i "s/SERVER_NAME_PLACEHOLDER/$DOMAIN/g" $NGINX_CONFIG

# Enable the site
sudo ln -sf $NGINX_CONFIG /etc/nginx/sites-enabled/learning-platform

# Remove default nginx site if exists
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
echo "Testing Nginx configuration..."
sudo nginx -t

# Reload nginx
echo "Reloading Nginx..."
sudo systemctl reload nginx

# ===================================
# SSL Setup (Optional)
# ===================================
echo ""
echo "=========================================="
echo "  SSL Setup"
echo "=========================================="
echo ""
read -p "Do you want to setup SSL with Let's Encrypt? (y/n): " setup_ssl

if [ "$setup_ssl" = "y" ]; then
    echo "Setting up SSL..."
    sudo certbot --nginx -d $DOMAIN --non-interactive --agree-tos --register-unsafely-without-email || echo "SSL setup failed. You can run 'sudo certbot --nginx -d $DOMAIN' manually later."
fi

# ===================================
# Completion
# ===================================
echo ""
echo "=========================================="
echo "  Deployment Complete!"
echo "=========================================="
echo ""
echo "Your application is now running at:"
echo "  - Frontend: http://$DOMAIN"
echo "  - Backend API: http://$DOMAIN:3001"
echo "  - API Docs: http://$DOMAIN:3001/docs"
echo ""
echo "Service Management Commands:"
echo "  - Check backend status: sudo systemctl status learning-platform-backend"
echo "  - Restart backend: sudo systemctl restart learning-platform-backend"
echo "  - View backend logs: sudo journalctl -u learning-platform-backend -f"
echo "  - Restart Nginx: sudo systemctl restart nginx"
echo ""
echo "Default login credentials:"
echo "  - Student: student@example.com / password123"
echo "  - Instructor: instructor@example.com / password123"
echo "  - Admin: admin@example.com / password123"
echo ""

