# PowerShell script to setup GitHub repository for Sarus Robot

Write-Host "🤖 Sarus Robot - GitHub Repository Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Get GitHub username and repository name
$githubUsername = Read-Host "Enter your GitHub username"
$repoName = Read-Host "Enter repository name (default: sarus-robot)"

# Use default if empty
if ([string]::IsNullOrEmpty($repoName)) {
    $repoName = "sarus-robot"
}

Write-Host ""
Write-Host "Setting up remote repository..." -ForegroundColor Yellow
Write-Host "Repository: https://github.com/$githubUsername/$repoName" -ForegroundColor Blue

try {
    # Add remote origin
    git remote add origin "https://github.com/$githubUsername/$repoName.git"
    Write-Host "✅ Remote origin added" -ForegroundColor Green

    # Rename main branch
    git branch -M main
    Write-Host "✅ Branch renamed to main" -ForegroundColor Green

    # Push to GitHub
    Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
    git push -u origin main
    Write-Host "✅ Code pushed to GitHub!" -ForegroundColor Green

    Write-Host ""
    Write-Host "✅ Repository setup complete!" -ForegroundColor Green
    Write-Host "🔗 Your repository: https://github.com/$githubUsername/$repoName" -ForegroundColor Blue
    
} catch {
    Write-Host "❌ Error occurred: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Please make sure you've created the repository on GitHub first!" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Add repository description and topics on GitHub"
Write-Host "2. Add collaboration guidelines"
Write-Host "3. Set up GitHub Actions (optional)"
Write-Host "4. Create issues/project boards (optional)"
