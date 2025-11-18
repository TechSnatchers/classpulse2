# Setup ngrok Authentication

## Step 1: Sign Up for ngrok Account

1. Go to: https://dashboard.ngrok.com/signup
2. Sign up (it's free!)
3. You can use email or GitHub/Google to sign up

## Step 2: Get Your Authtoken

1. After signing up, go to: https://dashboard.ngrok.com/get-started/your-authtoken
2. You'll see your authtoken (looks like: `2abc123def456ghi789jkl012mno345pqr678stu901vwx234yz`)
3. **Copy it!**

## Step 3: Install Authtoken

In your terminal, type:

```powershell
ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
```

Replace `YOUR_AUTHTOKEN_HERE` with the actual token you copied.

Example:
```powershell
ngrok config add-authtoken 2abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

## Step 4: Verify It Works

Now try again:
```powershell
ngrok http 3001
```

It should work now! You'll see:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:3001
```

## Quick Steps Summary:

1. ✅ Sign up: https://dashboard.ngrok.com/signup
2. ✅ Get token: https://dashboard.ngrok.com/get-started/your-authtoken
3. ✅ Install: `ngrok config add-authtoken YOUR_TOKEN`
4. ✅ Run: `ngrok http 3001`

## Free Tier:

ngrok free tier includes:
- 1 tunnel
- Random subdomain (changes each time)
- Perfect for testing!

For production, you might want a paid plan with static domain.

