# PowerShell deployment script for Zoom webhook AWS infrastructure

Write-Host "🚀 Deploying Zoom Webhook Infrastructure to AWS..." -ForegroundColor Cyan
Write-Host ""

# Check if AWS CLI is installed
try {
    $null = Get-Command aws -ErrorAction Stop
} catch {
    Write-Host "❌ AWS CLI is not installed. Please install it first." -ForegroundColor Red
    Write-Host "   Download from: https://aws.amazon.com/cli/" -ForegroundColor Yellow
    exit 1
}

# Get parameters
$BackendApiUrl = Read-Host "Enter your backend API URL (e.g., https://your-backend.com)"
$ZoomSecret = Read-Host "Enter Zoom webhook secret token" -AsSecureString
$ZoomSecretPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($ZoomSecret)
)

# Set stack name and region
$StackName = "zoom-webhook-stack"
$Region = if ($env:AWS_REGION) { $env:AWS_REGION } else { "us-east-1" }

Write-Host ""
Write-Host "📦 Creating CloudFormation stack..." -ForegroundColor Yellow

# Create stack
$createStackParams = @{
    StackName = $StackName
    TemplateBody = Get-Content -Path "cloudformation\zoom-webhook-stack.yaml" -Raw
    Parameters = @(
        @{
            ParameterKey = "BackendApiUrl"
            ParameterValue = $BackendApiUrl
        },
        @{
            ParameterKey = "ZoomWebhookSecretToken"
            ParameterValue = $ZoomSecretPlain
        }
    )
    Capabilities = @("CAPABILITY_NAMED_IAM")
    Region = $Region
}

try {
    New-CFNStack @createStackParams | Out-Null
    
    Write-Host "⏳ Waiting for stack creation (this may take a few minutes)..." -ForegroundColor Yellow
    Wait-CFNStack -StackName $StackName -Region $Region
    
    # Get webhook URL
    $stack = Get-CFNStack -StackName $StackName -Region $Region
    $webhookUrl = ($stack.Outputs | Where-Object { $_.OutputKey -eq "WebhookUrl" }).OutputValue
    
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
    Write-Host ""
    Write-Host "💡 Alternative: Use AWS CLI directly:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "aws cloudformation create-stack \`" -ForegroundColor Gray
    Write-Host "  --stack-name $StackName \`" -ForegroundColor Gray
    Write-Host "  --template-body file://cloudformation/zoom-webhook-stack.yaml \`" -ForegroundColor Gray
    Write-Host "  --parameters ParameterKey=BackendApiUrl,ParameterValue=$BackendApiUrl ParameterKey=ZoomWebhookSecretToken,ParameterValue=$ZoomSecretPlain \`" -ForegroundColor Gray
    Write-Host "  --capabilities CAPABILITY_NAMED_IAM" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

