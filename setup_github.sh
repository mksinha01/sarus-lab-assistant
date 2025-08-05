#!/bin/bash

# GitHub Repository Setup Script for Sarus Robot
# Run this after creating your repository on GitHub

echo "🤖 Sarus Robot - GitHub Repository Setup"
echo "========================================"

# Get GitHub username and repository name
read -p "Enter your GitHub username: " GITHUB_USERNAME
read -p "Enter repository name (default: sarus-robot): " REPO_NAME

# Use default if empty
if [ -z "$REPO_NAME" ]; then
    REPO_NAME="sarus-robot"
fi

echo ""
echo "Setting up remote repository..."
echo "Repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME"

# Add remote origin
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Rename main branch
git branch -M main

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Repository setup complete!"
echo "🔗 Your repository: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo ""
echo "Next steps:"
echo "1. Add repository description and topics on GitHub"
echo "2. Add collaboration guidelines"
echo "3. Set up GitHub Actions (optional)"
echo "4. Create issues/project boards (optional)"
