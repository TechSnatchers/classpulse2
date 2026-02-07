#!/bin/bash
# Application Monitoring Script
# Quick health check for all services

echo "=========================================="
echo "  Learning Platform Health Check"
echo "=========================================="
echo ""

# Get server info
if command -v curl &> /dev/null; then
    PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "N/A")
else
    PUBLIC_IP="N/A"
fi

echo "Server: $PUBLIC_IP"
echo "Time: $(date)"
echo ""

# Check Backend Service
echo "----------------------------------------"
echo "Backend Service Status"
echo "----------------------------------------"
if sudo systemctl is-active --quiet learning-platform-backend; then
    echo "✓ Backend service: RUNNING"
    
    # Check if backend is responding
    if curl -s http://localhost:3001/health > /dev/null 2>&1; then
        echo "✓ Backend API: RESPONDING"
        HEALTH=$(curl -s http://localhost:3001/health | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
        echo "  Status: $HEALTH"
    else
        echo "✗ Backend API: NOT RESPONDING"
    fi
else
    echo "✗ Backend service: NOT RUNNING"
    echo ""
    echo "Recent logs:"
    sudo journalctl -u learning-platform-backend -n 10 --no-pager
fi
echo ""

# Check Nginx
echo "----------------------------------------"
echo "Nginx Status"
echo "----------------------------------------"
if sudo systemctl is-active --quiet nginx; then
    echo "✓ Nginx: RUNNING"
    
    # Test nginx configuration
    if sudo nginx -t &> /dev/null; then
        echo "✓ Nginx config: VALID"
    else
        echo "✗ Nginx config: INVALID"
        sudo nginx -t
    fi
else
    echo "✗ Nginx: NOT RUNNING"
fi
echo ""

# Check MongoDB (if running locally)
echo "----------------------------------------"
echo "MongoDB Status (if local)"
echo "----------------------------------------"
if sudo systemctl is-active --quiet mongod 2>/dev/null; then
    echo "✓ MongoDB: RUNNING"
else
    echo "○ MongoDB: Not running locally (using Atlas?)"
fi
echo ""

# Check Disk Usage
echo "----------------------------------------"
echo "Disk Usage"
echo "----------------------------------------"
df -h / | tail -1 | awk '{print "  Used: "$3" / "$2" ("$5")"}'
echo ""

# Check Memory Usage
echo "----------------------------------------"
echo "Memory Usage"
echo "----------------------------------------"
free -h | grep Mem | awk '{print "  Used: "$3" / "$2}'
echo ""

# Check CPU Load
echo "----------------------------------------"
echo "CPU Load"
echo "----------------------------------------"
uptime | awk -F'load average:' '{print "  Load: "$2}'
echo ""

# Check Open Ports
echo "----------------------------------------"
echo "Listening Ports"
echo "----------------------------------------"
echo "Port 3001 (Backend):"
if sudo netstat -tulpn 2>/dev/null | grep -q ":3001 "; then
    echo "  ✓ LISTENING"
    sudo netstat -tulpn 2>/dev/null | grep ":3001 " | head -1
else
    echo "  ✗ NOT LISTENING"
fi
echo ""
echo "Port 80 (HTTP):"
if sudo netstat -tulpn 2>/dev/null | grep -q ":80 "; then
    echo "  ✓ LISTENING"
else
    echo "  ✗ NOT LISTENING"
fi
echo ""

# Recent Backend Logs
echo "----------------------------------------"
echo "Recent Backend Logs (last 5 lines)"
echo "----------------------------------------"
sudo journalctl -u learning-platform-backend -n 5 --no-pager
echo ""

# Recent Nginx Errors
echo "----------------------------------------"
echo "Recent Nginx Errors (if any)"
echo "----------------------------------------"
if [ -f /var/log/nginx/error.log ]; then
    sudo tail -5 /var/log/nginx/error.log 2>/dev/null || echo "No recent errors"
else
    echo "No error log found"
fi
echo ""

echo "=========================================="
echo "  Quick Actions"
echo "=========================================="
echo ""
echo "Restart backend:  sudo systemctl restart learning-platform-backend"
echo "Restart Nginx:    sudo systemctl restart nginx"
echo "View backend logs: sudo journalctl -u learning-platform-backend -f"
echo "View Nginx logs:  sudo tail -f /var/log/nginx/error.log"
echo "Update app:       ./update-app.sh"
echo ""

