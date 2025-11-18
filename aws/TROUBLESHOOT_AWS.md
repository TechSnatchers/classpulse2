# Troubleshooting AWS Console Access Issues

## "Security verification failure" Error

This error usually means AWS needs to verify your identity. Here are solutions:

### Solution 1: Reload the Page
- Simply refresh/reload the page (F5 or Ctrl+R)
- Clear browser cache and cookies for AWS
- Try a different browser

### Solution 2: Verify Your AWS Account
1. Check your email for AWS verification messages
2. Verify your phone number if prompted
3. Complete any pending account verification steps

### Solution 3: Use AWS CLI Instead (Recommended)
You can create credentials using AWS CLI without the console:

```powershell
# Install AWS CLI if not already installed
# Then configure with credentials you already have
aws configure
```

### Solution 4: Create IAM User via CLI
If you have root/admin access via CLI:

```powershell
# Create IAM user
aws iam create-user --user-name zoom-webhook-user

# Create access key
aws iam create-access-key --user-name zoom-webhook-user

# Attach policies
aws iam attach-user-policy --user-name zoom-webhook-user --policy-arn arn:aws:iam::aws:policy/CloudFormationFullAccess
aws iam attach-user-policy --user-name zoom-webhook-user --policy-arn arn:aws:iam::aws:policy/AWSLambda_FullAccess
aws iam attach-user-policy --user-name zoom-webhook-user --policy-arn arn:aws:iam::aws:policy/AmazonAPIGatewayAdministrator
```

### Solution 5: Contact AWS Support
If the issue persists:
- Go to: https://console.aws.amazon.com/support/
- Or use the "Contact AWS Customer Support" link in the error

### Alternative: Use Existing Credentials
If you already have AWS credentials from a previous setup:
- Use those credentials with `aws configure`
- No need to create new ones

## Quick Test

After resolving the issue, test your access:

```powershell
aws sts get-caller-identity
```

This should return your AWS account information if credentials are working.

