# PowerShell script to install AWS CLI on Windows

Write-Host "📥 Installing AWS CLI..." -ForegroundColor Cyan
Write-Host ""

# Check if already installed
try {
    $version = aws --version 2>$null
    Write-Host "✅ AWS CLI is already installed: $version" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next step: Configure AWS credentials" -ForegroundColor Yellow
    Write-Host "Run: aws configure" -ForegroundColor White
    exit 0
} catch {
    Write-Host "AWS CLI not found. Proceeding with installation..." -ForegroundColor Yellow
}

# Download AWS CLI installer
$installerUrl = "https://awscli.amazonaws.com/AWSCLIV2.msi"
$installerPath = "$env:TEMP\AWSCLIV2.msi"

Write-Host "📥 Downloading AWS CLI installer..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath -UseBasicParsing
    Write-Host "✅ Download complete" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to download installer: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Manual installation:" -ForegroundColor Yellow
    Write-Host "   1. Download from: https://awscli.amazonaws.com/AWSCLIV2.msi" -ForegroundColor White
    Write-Host "   2. Run the installer" -ForegroundColor White
    exit 1
}

Write-Host ""
Write-Host "🔧 Installing AWS CLI (this may take a minute)..." -ForegroundColor Yellow

# Install silently
try {
    Start-Process msiexec.exe -ArgumentList "/i `"$installerPath`" /quiet /norestart" -Wait -NoNewWindow
    Write-Host "✅ Installation complete!" -ForegroundColor Green
} catch {
    Write-Host "❌ Installation failed: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Try manual installation:" -ForegroundColor Yellow
    Write-Host "   Double-click: $installerPath" -ForegroundColor White
    exit 1
}

# Clean up
Remove-Item $installerPath -ErrorAction SilentlyContinue

# Refresh PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host ""
Write-Host "✅ AWS CLI installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Close and reopen PowerShell (to refresh PATH)" -ForegroundColor White
Write-Host "   2. Run: aws configure" -ForegroundColor White
Write-Host "   3. Enter your AWS credentials" -ForegroundColor White
Write-Host ""
Write-Host "💡 Get AWS credentials from AWS Console IAM section" -ForegroundColor Yellow
Write-Host ""
