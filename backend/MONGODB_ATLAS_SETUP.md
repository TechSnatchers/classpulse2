# MongoDB Atlas Setup Guide

This guide will help you set up MongoDB Atlas for the Learning Platform backend.

## Step 1: Create MongoDB Atlas Account

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up for a free account (M0 Free Tier)
3. Create a new cluster (choose the free tier)

## Step 2: Configure Database User

1. Go to **Database Access** in the left sidebar
2. Click **Add New Database User**
3. Choose **Password** authentication
4. Create a username and password (save these!)
5. Set user privileges to **Read and write to any database**
6. Click **Add User**

## Step 3: Whitelist IP Address

1. Go to **Network Access** in the left sidebar
2. Click **Add IP Address**
3. For development, click **Allow Access from Anywhere** (0.0.0.0/0)
   - ⚠️ **Security Note:** For production, use specific IP addresses
4. Click **Confirm**

## Step 4: Get Connection String

1. Go to **Database** → Click **Connect** on your cluster
2. Choose **Connect your application**
3. Select **Python** and version **3.6 or later**
4. Copy the connection string

Your connection string should look like:
```
mongodb+srv://<username>:<password>@cluster.mongodb.net/?appName=Cluster0
```

## Step 5: Configure Backend

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and replace the connection string:
   ```
   MONGODB_URL=mongodb+srv://shawmi3030_db_user:YOUR_PASSWORD@m0.zcjoclr.mongodb.net/?appName=M0
   DATABASE_NAME=learning_platform
   ```

3. Replace `YOUR_PASSWORD` with your actual database user password

## Step 6: Test Connection

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Test the connection:
   ```bash
   python main.py
   ```

   You should see:
   ```
   🔗 Connecting to MongoDB Atlas...
   ✅ Connected to MongoDB Atlas: learning_platform
   ```

## Troubleshooting

### Connection Timeout
- Check that your IP address is whitelisted in Network Access
- Verify your connection string is correct

### Authentication Failed
- Double-check your username and password
- Make sure you're using the database user password, not your Atlas account password

### DNS Resolution Error
- Make sure you're using `mongodb+srv://` (not `mongodb://`)
- Check your internet connection

## Security Best Practices

1. **Never commit `.env` file to git** (it's already in `.gitignore`)
2. **Use environment-specific passwords** for development/production
3. **Restrict IP access** in production (don't use 0.0.0.0/0)
4. **Rotate passwords** regularly
5. **Use MongoDB Atlas encryption** for sensitive data

## Free Tier Limits

MongoDB Atlas M0 (Free) includes:
- 512 MB storage
- Shared RAM and vCPU
- No credit card required
- Perfect for development and small projects

For production, consider upgrading to M10 or higher.

