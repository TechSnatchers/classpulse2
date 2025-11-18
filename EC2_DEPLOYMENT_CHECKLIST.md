# EC2 Deployment Checklist ✅

Use this checklist to ensure a smooth deployment to AWS EC2.

## Pre-Deployment Checklist

### AWS Setup
- [ ] AWS account created
- [ ] EC2 instance launched (Ubuntu 22.04 LTS)
- [ ] Instance type: t2.medium or larger
- [ ] Storage: At least 20GB
- [ ] SSH key pair created/downloaded
- [ ] Elastic IP assigned (optional but recommended)

### Security Group Configuration
- [ ] Port 22 (SSH) - open to your IP
- [ ] Port 80 (HTTP) - open to 0.0.0.0/0
- [ ] Port 443 (HTTPS) - open to 0.0.0.0/0
- [ ] Port 3001 (Backend API) - open to 0.0.0.0/0

### Database Setup
Choose one:
- [ ] MongoDB Atlas account created and cluster setup
- [ ] OR plan to use local MongoDB on EC2

If using MongoDB Atlas:
- [ ] Database user created
- [ ] Connection string obtained
- [ ] IP whitelist configured (0.0.0.0/0 for dev, or specific IP)

### Domain Setup (Optional)
- [ ] Domain name purchased
- [ ] DNS A record pointing to EC2 IP
- [ ] DNS propagated (check with: `nslookup yourdomain.com`)

### Local Preparation
- [ ] Code is in git repository OR ready to upload via SCP
- [ ] All local tests passing
- [ ] Environment variables documented

## Deployment Checklist

### Initial Connection
- [ ] SSH into EC2 instance: `ssh -i key.pem ubuntu@ec2-ip`
- [ ] Test internet connectivity: `ping google.com`
- [ ] Update system: `sudo apt update`

### Code Upload
Choose one method:
- [ ] Git clone from repository
- [ ] SCP from local machine
- [ ] Upload via SFTP client

Code location: `/var/www/learning-platform`

### Run Setup Script
- [ ] Navigate to project directory
- [ ] Make script executable: `chmod +x ec2-setup.sh`
- [ ] Run setup: `./ec2-setup.sh`
- [ ] Choose MongoDB installation option when prompted
- [ ] Wait for completion (5-10 minutes)

### Run Deployment Script
- [ ] Make script executable: `chmod +x deploy-to-ec2.sh`
- [ ] Run deployment: `./deploy-to-ec2.sh`
- [ ] Provide domain name or press Enter for IP
- [ ] Choose MongoDB option (local or Atlas)
- [ ] Provide MongoDB Atlas connection string (if using Atlas)
- [ ] Choose SSL setup (y/n)
- [ ] Wait for completion (5-10 minutes)

### Verify Deployment

#### Backend Checks
- [ ] Backend service running: `sudo systemctl status learning-platform-backend`
- [ ] Backend health check: `curl localhost:3001/health`
- [ ] Backend API accessible: `curl http://your-domain:3001/health`
- [ ] API docs accessible: Open `http://your-domain:3001/docs` in browser

#### Frontend Checks
- [ ] Nginx running: `sudo systemctl status nginx`
- [ ] Nginx config valid: `sudo nginx -t`
- [ ] Frontend accessible: Open `http://your-domain` in browser
- [ ] Frontend loads without errors (check browser console)

#### Full Application Test
- [ ] Can access login page
- [ ] Can register new user
- [ ] Can login with default credentials
- [ ] API calls work (check browser Network tab)
- [ ] No console errors

### SSL Setup (If Chosen)
- [ ] Certbot installed
- [ ] SSL certificate obtained
- [ ] HTTPS accessible: `https://your-domain`
- [ ] Auto-renewal setup: `sudo certbot renew --dry-run`

## Post-Deployment Checklist

### Security Hardening
- [ ] Change default user passwords in the application
- [ ] Restrict SSH to your IP only (Security Group)
- [ ] Setup fail2ban: `sudo apt install fail2ban`
- [ ] Enable firewall: `sudo ufw enable`
- [ ] Review MongoDB security (strong password, IP whitelist)

### Monitoring Setup
- [ ] Run health check: `./monitor-app.sh`
- [ ] Setup CloudWatch (optional)
- [ ] Configure log rotation (auto-configured)
- [ ] Setup backup script (optional)

### Documentation
- [ ] Document the EC2 IP / Domain
- [ ] Document MongoDB connection details
- [ ] Document admin credentials (securely)
- [ ] Note any custom configurations made

### Team Sharing
- [ ] Share application URL with team
- [ ] Share admin credentials (securely)
- [ ] Share SSH access (if needed)
- [ ] Document update process

## Maintenance Checklist

### Regular Tasks
- [ ] Monitor disk space: `df -h`
- [ ] Monitor memory: `free -h`
- [ ] Check application logs: `sudo journalctl -u learning-platform-backend -f`
- [ ] Update system packages: `sudo apt update && sudo apt upgrade`
- [ ] Check SSL certificate expiry: `sudo certbot certificates`

### Update Checklist
When deploying new code:
- [ ] SSH into EC2
- [ ] Run: `./update-app.sh`
- [ ] Verify services restarted
- [ ] Test application functionality
- [ ] Check logs for errors

### Backup Checklist
- [ ] Backup MongoDB (export or Atlas backup)
- [ ] Create EC2 snapshot
- [ ] Backup environment files (.env)
- [ ] Document backup location

## Troubleshooting Checklist

### If Backend Not Working
- [ ] Check service status: `sudo systemctl status learning-platform-backend`
- [ ] Check logs: `sudo journalctl -u learning-platform-backend -n 50`
- [ ] Check .env file exists: `cat /var/www/learning-platform/backend/.env`
- [ ] Test MongoDB connection
- [ ] Check port 3001: `sudo netstat -tulpn | grep 3001`
- [ ] Restart service: `sudo systemctl restart learning-platform-backend`

### If Frontend Not Working
- [ ] Check Nginx status: `sudo systemctl status nginx`
- [ ] Check Nginx config: `sudo nginx -t`
- [ ] Check files exist: `ls /var/www/learning-platform-frontend/`
- [ ] Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
- [ ] Restart Nginx: `sudo systemctl restart nginx`

### If Can't Connect to Application
- [ ] Check Security Group in AWS Console
- [ ] Check UFW firewall: `sudo ufw status`
- [ ] Test locally: `curl localhost:80`
- [ ] Check DNS: `nslookup your-domain.com`
- [ ] Check if services are listening: `sudo netstat -tulpn`

### If MongoDB Connection Fails
- [ ] Verify connection string in .env
- [ ] Check IP whitelist in MongoDB Atlas
- [ ] Test connection: `mongo "your-connection-string"`
- [ ] Check local MongoDB: `sudo systemctl status mongod`

## Emergency Contacts & Resources

### Important Files
- Backend .env: `/var/www/learning-platform/backend/.env`
- Nginx config: `/etc/nginx/sites-available/learning-platform`
- Systemd service: `/etc/systemd/system/learning-platform-backend.service`

### Important Commands
```bash
# View all services
sudo systemctl status learning-platform-backend nginx

# Restart everything
sudo systemctl restart learning-platform-backend nginx

# View logs
sudo journalctl -u learning-platform-backend -f
sudo tail -f /var/log/nginx/error.log

# Quick health check
./monitor-app.sh
```

### Documentation References
- Full Guide: [EC2_DEPLOYMENT_GUIDE.md](./EC2_DEPLOYMENT_GUIDE.md)
- Quick Guide: [QUICK_EC2_DEPLOY.md](./QUICK_EC2_DEPLOY.md)
- AWS EC2 Docs: https://docs.aws.amazon.com/ec2/
- MongoDB Atlas: https://docs.atlas.mongodb.com/

## Success Criteria

Your deployment is successful when:
- ✅ Backend health endpoint returns `{"status":"ok"}`
- ✅ Frontend loads in browser without errors
- ✅ Can register and login users
- ✅ API calls work from frontend to backend
- ✅ SSL certificate active (if configured)
- ✅ Services auto-start on reboot
- ✅ Logs are accessible and clean

## Sign-Off

- [ ] All checklist items completed
- [ ] Application tested and working
- [ ] Team notified
- [ ] Documentation updated

**Deployed by:** _______________
**Date:** _______________
**Version:** _______________

---

## Notes

Add any deployment-specific notes or customizations here:

```
[Your notes]
```

