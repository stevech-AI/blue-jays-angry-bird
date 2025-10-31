# Setting Up New GitHub Repository: blue-jays-angry-bird

## Step 1: Create the Repository on GitHub

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **+** icon in the top right, then select **"New repository"**
3. Repository name: `blue-jays-angry-bird`
4. Description: "Angry Birds game themed with Blue Jays vs Dodgers"
5. Choose **Public** or **Private** (your choice)
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click **"Create repository"**

## Step 2: Update Your Local Repository

After creating the repo on GitHub, run these commands:

```bash
# Add all your changes
git add .

# Commit your changes
git commit -m "Update game with Blue Jays theme, blue birds, and unique player names"

# Remove the old remote
git remote remove origin

# Add the new remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/blue-jays-angry-bird.git

# Push to the new repository
git branch -M main
git push -u origin main
```

## Alternative: If you want to keep both repositories

You can add the new repository as a second remote:

```bash
# Add new remote with a different name
git remote add blue-jays https://github.com/YOUR_USERNAME/blue-jays-angry-bird.git

# Push to the new repository
git push -u blue-jays main
```

## Quick Setup Script

Or run this script (update YOUR_USERNAME first):

```bash
#!/bin/bash
USERNAME="YOUR_USERNAME"  # Change this!
REPO_NAME="blue-jays-angry-bird"

git add .
git commit -m "Update game with Blue Jays theme, blue birds, and unique player names"
git remote remove origin
git remote add origin https://github.com/$USERNAME/$REPO_NAME.git
git branch -M main
git push -u origin main

echo "Done! Your repo is at: https://github.com/$USERNAME/$REPO_NAME"
```

