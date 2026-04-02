# Git Push Guide for DDR Report Generator

## Prerequisites

### 1. Install Git
- **Windows**: Download from https://git-scm.com/download/win
- **Mac**: `brew install git`
- **Linux**: `sudo apt-get install git`

### 2. Configure Git (First Time Only)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Step-by-Step: Push to GitHub

### Option A: Create New Repository on GitHub

1. Go to https://github.com/new
2. Enter repository name: `ddr-report-generator`
3. Add description: "AI-Powered Building Diagnostic Report Generator"
4. Choose Public or Private
5. **DO NOT** initialize with README (we have one)
6. Click "Create repository"

### Option B: Push Existing Local Repository

```bash
# Navigate to project directory
cd c:\Users\vaibh\Downloads\ddr_system

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: DDR Report Generator with Ollama LLM integration"

# Add remote repository (replace USERNAME/REPO with your details)
git remote add origin https://github.com/YOUR_USERNAME/ddr-report-generator.git

# Rename branch to main (GitHub default)
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## Step-by-Step: Push to GitLab

### If using GitLab instead:

```bash
cd c:\Users\vaibh\Downloads\ddr_system
git init
git add .
git commit -m "Initial commit: DDR Report Generator with Ollama LLM integration"
git remote add origin https://gitlab.com/YOUR_USERNAME/ddr-report-generator.git
git branch -M main
git push -u origin main
```

---

## Project Files Being Pushed

```
ddr_system/
├── app.py                    # Main Flask application
├── docx_generator.py         # DOCX report generation
├── pdf_generator.py          # PDF report generation
├── requirements.txt          # Python dependencies
├── .env                      # Configuration (add to .gitignore)
├── .env.example              # Example configuration
├── .gitignore                # Git ignore rules
├── README.md                 # Updated project documentation
├── templates/
│   └── index.html           # Web UI
├── static/
│   ├── css/                 # Stylesheets
│   └── js/                  # JavaScript
├── uploads/                 # (auto-created, ignored)
└── outputs/                 # (auto-created, ignored)
```

---

## What's Ignored (Not Pushed)

The `.gitignore` file excludes:
- ✗ `__pycache__/` - Python cache
- ✗ `venv/` - Virtual environment
- ✗ `.venv/` - Virtual environment
- ✗ `.env` - Sensitive configuration
- ✗ `uploads/` - Temporary files
- ✗ `outputs/` - Generated files
- ✗ `.idea/` - IDE files
- ✗ `*.log` - Log files

---

## Getting SSH Keys (Advanced)

For passwordless pushing:

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Accept default location (press Enter)
# Enter passphrase (or leave empty for no password)

# Copy public key to clipboard
cat ~/.ssh/id_ed25519.pub
```

Then add the key to GitHub:
1. Go to https://github.com/settings/keys
2. Click "New SSH key"
3. Paste your public key
4. Click "Add SSH key"

Use SSH URL when pushing:
```bash
git remote add origin git@github.com:YOUR_USERNAME/ddr-report-generator.git
```

---

## Useful Git Commands

```bash
# Check status
git status

# View commit history
git log

# Add specific file
git add app.py

# View changes before committing
git diff

# Amend last commit
git commit --amend

# Push to repository
git push origin main

# Pull updates from repository
git pull origin main

# Create new branch
git checkout -b feature-name

# Switch branch
git checkout main

# Merge branch
git merge feature-name
```

---

## After First Push

For subsequent updates:

```bash
# Make changes to files
# ...

# Stage changes
git add .

# Commit
git commit -m "Describe your changes"

# Push
git push origin main
```

---

## Troubleshooting

### Remote origin already exists
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/ddr-report-generator.git
```

### Authentication failed
- Use personal access token instead of password (GitHub requires this now)
- Generate token: https://github.com/settings/tokens

### Large files
- If uploads/ or outputs/ contain large files, ensure they're in .gitignore
- Check: `git ls-files | grep uploads` (should be empty)

---

## Next Steps

1. **Create GitHub account** (if you don't have one): https://github.com/signup
2. **Install Git** on your computer
3. **Follow the steps above** to push your project
4. **Share the repository link** with collaborators

---

## Questions?

- Git documentation: https://git-scm.com/doc
- GitHub help: https://docs.github.com
- GitLab help: https://docs.gitlab.com
