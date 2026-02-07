# Refresh PATH environment variable
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "✅ PATH refreshed" -ForegroundColor Green
Write-Host ""
Write-Host "Testing AWS CLI..." -ForegroundColor Yellow

try {
    $version = aws --version
    Write-Host "✅ AWS CLI is working: $version" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next: Run 'aws configure' to set up credentials" -ForegroundColor Cyan
} catch {
    Write-Host "❌ AWS CLI still not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please:" -ForegroundColor Yellow
    Write-Host "   1. Close and reopen PowerShell" -ForegroundColor White
    Write-Host "   2. Or restart your computer" -ForegroundColor White
    Write-Host ""
    Write-Host "Then run: aws --version" -ForegroundColor Cyan
}

