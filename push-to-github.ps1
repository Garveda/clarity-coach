# Push Clarity Coach to GitHub - Quick Script
# 
# BEFORE RUNNING THIS SCRIPT:
# 1. Go to https://github.com/new
# 2. Create a new repository named "clarity-coach"
# 3. Do NOT initialize with README, .gitignore, or license
# 4. Replace YOUR-USERNAME below with your actual GitHub username
# 5. Run this script

# Configuration
$GITHUB_USERNAME = "Garveda"  # ⚠️ CHANGE THIS!
$REPO_NAME = "clarity-coach"

# Navigate to project
Set-Location "C:\Users\admin\Desktop\Sonstiges\HMS_PROJEKT\clarity-coach\clarity-coach-main"

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Clarity Coach - GitHub Push Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if remote already exists
$remoteExists = git remote -v | Select-String "origin"

if ($remoteExists) {
    Write-Host "✓ Remote 'origin' already exists" -ForegroundColor Yellow
    Write-Host "  Current remote: $remoteExists" -ForegroundColor Gray
    Write-Host ""
    $response = Read-Host "Do you want to update it? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        git remote remove origin
        Write-Host "✓ Removed old remote" -ForegroundColor Green
    } else {
        Write-Host "✗ Keeping existing remote" -ForegroundColor Yellow
    }
}

if (-not $remoteExists -or $response -eq "y" -or $response -eq "Y") {
    # Check if username was changed
    if ($GITHUB_USERNAME -eq "YOUR-USERNAME") {
        Write-Host "⚠️  ERROR: Please edit this script and change YOUR-USERNAME to your GitHub username!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Edit line 11 of this script:" -ForegroundColor Yellow
        Write-Host '  $GITHUB_USERNAME = "your-actual-username"' -ForegroundColor Yellow
        Write-Host ""
        pause
        exit 1
    }

    # Add remote
    $remoteUrl = "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    Write-Host "Adding remote: $remoteUrl" -ForegroundColor Cyan
    git remote add origin $remoteUrl
    Write-Host "✓ Remote added" -ForegroundColor Green
    Write-Host ""
}

# Rename branch to main
Write-Host "Renaming branch to 'main'..." -ForegroundColor Cyan
git branch -M main
Write-Host "✓ Branch renamed" -ForegroundColor Green
Write-Host ""

# Show status
Write-Host "Current status:" -ForegroundColor Cyan
git status
Write-Host ""

# Push to GitHub
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Ready to push to GitHub!" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to push, or Ctrl+C to cancel..."
pause

Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "  ✓ SUCCESS! Project pushed to GitHub!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "View your repository at:" -ForegroundColor Cyan
    Write-Host "  https://github.com/$GITHUB_USERNAME/$REPO_NAME" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Add repository description and topics" -ForegroundColor Gray
    Write-Host "  2. Enable Issues and Discussions" -ForegroundColor Gray
    Write-Host "  3. Share with others!" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Red
    Write-Host "  ✗ Push failed!" -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "  1. Repository doesn't exist - create it at https://github.com/new" -ForegroundColor Gray
    Write-Host "  2. Authentication failed - you may need a Personal Access Token" -ForegroundColor Gray
    Write-Host "  3. Wrong username - check line 11 of this script" -ForegroundColor Gray
    Write-Host ""
    Write-Host "See GITHUB_SETUP.md for detailed help" -ForegroundColor Cyan
    Write-Host ""
}

pause
