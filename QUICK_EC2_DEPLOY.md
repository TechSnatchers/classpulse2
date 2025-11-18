# Quick EC2 Deployment - 5 Minutes ⚡

Fast deployment guide for experienced developers.

## Prerequisites
- Ubuntu 22.04 EC2 instance running
- SSH key configured
- Security Group: ports 22, 80, 443, 3001 open

## Deploy in 5 Commands

```bash
# 1. SSH into EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# 2. Clone/Upload your code
sudo mkdir -p /var/www/learning-platform
sudo chown -R $USER:$USER /var/www/learning-platform
cd /var/www/learning-platform
# Upload code here or git clone

# 3. Make scripts executable
chmod +x ec2-setup.sh deploy-to-ec2.sh

# 4. Run setup (installs all dependencies)
./ec2-setup.sh

# 5. Deploy application
./deploy-to-ec2.sh
```

## What You'll Need to Provide

During `deploy-to-ec2.sh`:
1. **Domain or IP** (press Enter to use EC2 IP)
2. **MongoDB choice:**
   - Option 1: Local (installed by ec2-setup.sh)
   - Option 2: MongoDB Atlas connection string
3. **SSL setup** (y/n)

## After Deployment

Your app runs at:
- Frontend: `http://your-domain`
- Backend: `http://your-domain:3001`
- API Docs: `http://your-domain:3001/docs`

## Update Application

```bash
cd /var/www/learning-platform
git pull
cd backend && source venv/bin/activate && pip install -r requirements.txt
sudo systemctl restart learning-platform-backend
cd ../frontend && npm install && npm run build
sudo cp -r dist/* /var/www/learning-platform-frontend/
sudo systemctl reload nginx
```

## Service Commands

```bash
# Backend
sudo systemctl status learning-platform-backend
sudo systemctl restart learning-platform-backend
sudo journalctl -u learning-platform-backend -f

# Nginx
sudo systemctl status nginx
sudo systemctl restart nginx
```

## Common Issues

**Backend won't start:**
```bash
sudo journalctl -u learning-platform-backend -n 50
```

**Can't access app:**
- Check Security Group (AWS Console)
- Check firewall: `sudo ufw status`
- Test backend: `curl localhost:3001/health`

**MongoDB connection fails:**
- Whitelist EC2 IP in MongoDB Atlas
- Check connection string in `/var/www/learning-platform/backend/.env`

## Architecture

```
Internet → Nginx (80/443) → Frontend (static files)
                          → Backend (3001) → MongoDB
```

## Default Logins

- Student: `student@example.com` / `password123`
- Instructor: `instructor@example.com` / `password123`
- Admin: `admin@example.com` / `password123`

For detailed guide, see: [EC2_DEPLOYMENT_GUIDE.md](./EC2_DEPLOYMENT_GUIDE.md)

