# Installing AWS CLI on Windows

## Quick Installation

### Method 1: Using MSI Installer (Recommended)

1. **Download AWS CLI:**
   - Go to: https://awscli.amazonaws.com/AWSCLIV2.msi
   - Or visit: https://aws.amazon.com/cli/

2. **Run the installer:**
   - Double-click the downloaded `.msi` file
   - Follow the installation wizard
   - Choose "Install for all users" or "Install for current user"

3. **Verify installation:**
   ```powershell
   aws --version
   ```

4. **Configure AWS credentials:**
   ```powershell
   aws configure
   ```
   You'll need:
   - AWS Access Key ID
   - AWS Secret Access Key
   - Default region (e.g., `us-east-1`)
   - Default output format (e.g., `json`)

### Method 2: Using PowerShell (Alternative)

```powershell
# Download installer
Invoke-WebRequest -Uri "https://awscli.amazonaws.com/AWSCLIV2.msi" -OutFile "$env:TEMP\AWSCLIV2.msi"

# Install silently
Start-Process msiexec.exe -ArgumentList "/i $env:TEMP\AWSCLIV2.msi /quiet" -Wait

# Verify
aws --version
```

### Method 3: Using Chocolatey (If you have it)

```powershell
choco install awscli
```

## Getting AWS Credentials

1. **Sign in to AWS Console:** https://console.aws.amazon.com/
2. **Go to IAM (Identity and Access Management)**
3. **Create a user** (or use existing):
   - Go to "Users" → "Add users"
   - Enable "Programmatic access"
   - Attach policies: `CloudFormationFullAccess`, `LambdaFullAccess`, `APIGatewayAdministrator`
4. **Save credentials:**
   - Access Key ID
   - Secret Access Key
   - ⚠️ **Important:** Save these securely - you won't see the secret key again!

## Configure AWS CLI

After installation, configure it:

```powershell
aws configure
```

Enter:
- **AWS Access Key ID:** Your access key
- **AWS Secret Access Key:** Your secret key
- **Default region name:** `us-east-1` (or your preferred region)
- **Default output format:** `json`

## Verify Setup

```powershell
# Test connection
aws sts get-caller-identity

# Should return your AWS account info
```

## Alternative: Use AWS Console (No CLI Required)

If you prefer not to install AWS CLI, you can deploy using AWS Console:

1. Go to **CloudFormation** in AWS Console
2. Click **Create stack** → **With new resources**
3. Upload the template: `aws/cloudformation/zoom-webhook-stack.yaml`
4. Enter parameters manually
5. Create stack

See `ZOOM_WEBHOOK_SETUP.md` for detailed instructions.

