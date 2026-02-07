# PowerShell script using AWS CLI (no AWS PowerShell module required)

Write-Host "🚀 Deploying Zoom Webhook Infrastructure to AWS..." -ForegroundColor Cyan
Write-Host ""

# Check if AWS CLI is installed
try {
    $null = aws --version 2>$null
} catch {
    Write-Host "❌ AWS CLI is not installed. Please install it first." -ForegroundColor Red
    Write-Host "   Download from: https://aws.amazon.com/cli/" -ForegroundColor Yellow
    exit 1
}

# Get parameters
$BackendApiUrl = Read-Host "Enter your backend API URL (e.g., https://your-backend.com)"
$ZoomSecret = Read-Host "Enter Zoom webhook secret token" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($ZoomSecret)
$ZoomSecretPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Set stack name and region
$StackName = "zoom-webhook-stack"
$Region = if ($env:AWS_REGION) { $env:AWS_REGION } else { "us-east-1" }

Write-Host ""
Write-Host "📦 Creating CloudFormation stack..." -ForegroundColor Yellow

# Create the parameters JSON file
$parametersJson = @"
[
  {
    "ParameterKey": "BackendApiUrl",
    "ParameterValue": "$BackendApiUrl"
  },
  {
    "ParameterKey": "ZoomWebhookSecretToken",
    "ParameterValue": "$ZoomSecretPlain"
  }
]
"@

$parametersFile = "parameters.json"
$parametersJson | Out-File -FilePath $parametersFile -Encoding UTF8

try {
    # Create stack
    aws cloudformation create-stack `
        --stack-name $StackName `
        --template-body file://cloudformation/zoom-webhook-stack.yaml `
        --parameters file://$parametersFile `
        --capabilities CAPABILITY_NAMED_IAM `
        --region $Region
    
    Write-Host "⏳ Waiting for stack creation (this may take a few minutes)..." -ForegroundColor Yellow
    aws cloudformation wait stack-create-complete `
        --stack-name $StackName `
        --region $Region
    
    # Get webhook URL
    $webhookUrl = aws cloudformation describe-stacks `
        --stack-name $StackName `
        --region $Region `
        --query "Stacks[0].Outputs[?OutputKey=='WebhookUrl'].OutputValue" `
        --output text
    
    # Clean up parameters file
    Remove-Item $parametersFile -ErrorAction SilentlyContinue
    
    Write-Host ""
    Write-Host "✅ Deployment complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Webhook URL: $webhookUrl" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🔗 Use this URL in your Zoom app webhook configuration:" -ForegroundColor Yellow
    Write-Host "   $webhookUrl" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host ""
    Write-Host "❌ Error deploying stack: $_" -ForegroundColor Red
    Remove-Item $parametersFile -ErrorAction SilentlyContinue
    exit 1
}

