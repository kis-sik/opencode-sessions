# Publishing Instructions

## Step 1: Configure GitHub Authentication

### Option A: SSH Keys (Recommended)
```bash
# Generate SSH key if you don't have one
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add SSH key to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy the output and add to GitHub: https://github.com/settings/keys
```

### Option B: Personal Access Token
```bash
# Create token at: https://github.com/settings/tokens
# Select "repo" scope

# Push with token
git push https://<TOKEN>@github.com/kis-sik/opencode-sessions.git main
```

## Step 2: Push to GitHub

```bash
cd ~/tech/opencode-sessions

# Set remote
git remote add origin https://github.com/kis-sik/opencode-sessions.git

# Push code
git push -u origin main

# Create tag
git tag v1.0.0
git push origin v1.0.0
```

## Step 3: Update README URLs

Edit `README.md` and replace:
- `https://raw.githubusercontent.com/yourusername/opencode-sessions/main/`
- `https://github.com/yourusername/opencode-sessions.git`

With:
- `https://raw.githubusercontent.com/kis-sik/opencode-sessions/main/`
- `https://github.com/kis-sik/opencode-sessions.git`

## Step 4: Publish to npm (Optional)

```bash
# Login to npm
npm login

# Update package.json with correct repository URL
# Then publish
npm publish
```

## Repository is Ready

The repository contains:
- ✅ `opencode-sessions` - Main Python script
- ✅ `opencode-sessions.fish` - Fish autocompletion
- ✅ `opencode-sessions-plugin.js` - OpenCode plugin
- ✅ `package.json` - npm configuration
- ✅ `LICENSE` - MIT License
- ✅ `README.md` - Documentation
- ✅ `.gitignore` - Ignored files

Once published, users can install with:
```bash
curl -sL https://raw.githubusercontent.com/kis-sik/opencode-sessions/main/opencode-sessions | python3 - --install
```