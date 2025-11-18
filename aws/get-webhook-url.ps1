# Get the API Gateway webhook URL for your Lambda function

Write-Host "🔍 Finding your Zoom webhook URL..." -ForegroundColor Cyan
Write-Host ""

$functionName = "zoom_webhook"
$region = "eu-north-1"

try {
    # Get function configuration
    Write-Host "📋 Getting Lambda function details..." -ForegroundColor Yellow
    $functionConfig = aws lambda get-function-configuration `
        --function-name $functionName `
        --region $region `
        --output json | ConvertFrom-Json
    
    Write-Host "✅ Function found: $($functionConfig.FunctionName)" -ForegroundColor Green
    Write-Host "   Runtime: $($functionConfig.Runtime)" -ForegroundColor Gray
    Write-Host "   Last Modified: $($functionConfig.LastModified)" -ForegroundColor Gray
    Write-Host ""
    
    # Get API Gateway triggers
    Write-Host "🔗 Finding API Gateway endpoint..." -ForegroundColor Yellow
    
    # List all API Gateways
    $apis = aws apigateway get-rest-apis --region $region --output json | ConvertFrom-Json
    
    if ($apis.items.Count -eq 0) {
        Write-Host "⚠️  No API Gateway found" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "💡 You need to:" -ForegroundColor Cyan
        Write-Host "   1. Go to API Gateway console" -ForegroundColor White
        Write-Host "   2. Create API or find existing one" -ForegroundColor White
        Write-Host "   3. Connect it to your Lambda function" -ForegroundColor White
        Write-Host ""
        exit 1
    }
    
    Write-Host "📡 Found $($apis.items.Count) API Gateway(s)" -ForegroundColor Green
    Write-Host ""
    
    # For each API, try to find the webhook endpoint
    foreach ($api in $apis.items) {
        Write-Host "Checking API: $($api.name) (ID: $($api.id))" -ForegroundColor Gray
        
        # Get resources
        $resources = aws apigateway get-resources `
            --rest-api-id $api.id `
            --region $region `
            --output json | ConvertFrom-Json
        
        foreach ($resource in $resources.items) {
            if ($resource.pathPart -eq "webhook" -or $resource.path -like "*webhook*") {
                $webhookUrl = "https://$($api.id).execute-api.$region.amazonaws.com/prod$($resource.path)"
                
                Write-Host ""
                Write-Host "✅ Webhook URL found!" -ForegroundColor Green
                Write-Host ""
                Write-Host "📋 Your Zoom Webhook URL:" -ForegroundColor Cyan
                Write-Host "   $webhookUrl" -ForegroundColor White
                Write-Host ""
                Write-Host "🔗 Use this URL in Zoom Marketplace:" -ForegroundColor Yellow
                Write-Host "   1. Go to: https://marketplace.zoom.us/" -ForegroundColor White
                Write-Host "   2. Your App → Event Subscriptions" -ForegroundColor White
                Write-Host "   3. Add Event Subscription" -ForegroundColor White
                Write-Host "   4. Endpoint URL: $webhookUrl" -ForegroundColor White
                Write-Host ""
                exit 0
            }
        }
    }
    
    Write-Host ""
    Write-Host "⚠️  Webhook endpoint not found in API Gateway" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "💡 Manual steps:" -ForegroundColor Cyan
    Write-Host "   1. Go to API Gateway console" -ForegroundColor White
    Write-Host "   2. Find your API" -ForegroundColor White
    Write-Host "   3. Look for the endpoint URL in 'Stages' → 'prod'" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Make sure:" -ForegroundColor Yellow
    Write-Host "   1. AWS CLI is configured: aws configure" -ForegroundColor White
    Write-Host "   2. You have permissions to access Lambda and API Gateway" -ForegroundColor White
    Write-Host ""
}

