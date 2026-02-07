#!/bin/bash
# EC2 Initial Setup Script for Learning Platform
# Run this script on a fresh Ubuntu EC2 instance

set -e

echo "=========================================="
echo "  Learning Platform EC2 Setup"
echo "=========================================="

# Update system packages
echo ""
echo "Step 1: Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install Node.js (v18.x LTS)
echo ""
echo "Step 2: Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify Node.js installation
echo "Node.js version: $(node --version)"
echo "npm version: $(npm --version)"

# Install Python 3.10+
echo ""
echo "Step 3: Installing Python..."
sudo apt install -y python3 python3-pip python3-venv

# Verify Python installation
echo "Python version: $(python3 --version)"
echo "pip version: $(pip3 --version)"

# Install Nginx
echo ""
echo "Step 4: Installing Nginx..."
sudo apt install -y nginx

# Install PM2 (Process Manager for Node.js)
echo ""
echo "Step 5: Installing PM2..."
sudo npm install -g pm2

# Install Git
echo ""
echo "Step 6: Installing Git..."
sudo apt install -y git

# Create application directory
echo ""
echo "Step 7: Creating application directory..."
sudo mkdir -p /var/www/learning-platform
sudo chown -R $USER:$USER /var/www/learning-platform

# Setup firewall
echo ""
echo "Step 8: Configuring firewall..."
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw allow 3001/tcp    # Backend API
sudo ufw allow 5173/tcp    # Vite dev (if needed)
echo "y" | sudo ufw enable

# Install MongoDB (optional - for local database)
echo ""
echo "Step 9: Do you want to install MongoDB locally? (y/n)"
read -p "Press y for local MongoDB or n to use MongoDB Atlas: " install_mongo

if [ "$install_mongo" = "y" ]; then
    echo "Installing MongoDB..."
    curl -fsSL https://www.mongodb.org/static/pgp/server-6.0.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/mongodb-6.gpg
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
    sudo apt update
    sudo apt install -y mongodb-org
    sudo systemctl start mongod
    sudo systemctl enable mongod
    echo "MongoDB installed and started"
else
    echo "Skipping MongoDB installation - will use MongoDB Atlas"
fi

# Install certbot for SSL (Let's Encrypt)
echo ""
echo "Step 10: Installing Certbot for SSL..."
sudo apt install -y certbot python3-certbot-nginx

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Clone your repository to /var/www/learning-platform"
echo "2. Run the deployment script: ./deploy-to-ec2.sh"
echo ""
echo "System Information:"
echo "- Node.js: $(node --version)"
echo "- npm: $(npm --version)"
echo "- Python: $(python3 --version)"
echo "- Nginx: $(nginx -v 2>&1)"
echo "- PM2: $(pm2 --version)"
echo ""

