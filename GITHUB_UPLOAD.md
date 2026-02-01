# Upload this project to GitHub

The repo is already initialized with an initial commit on branch `main`. Follow these steps to create the GitHub repo and push.

## Option 1: Create repo on GitHub, then push (recommended)

1. **Create a new repository on GitHub**
   - Go to [https://github.com/new](https://github.com/new)
   - Repository name: e.g. `data-analysis` or `ghd-drug-comparison`
   - Description (optional): e.g. "GHD drug comparison dashboard (McKinsey style)"
   - Choose **Public**
   - Do **not** add a README, .gitignore, or license (they already exist here)
   - Click **Create repository**

2. **Add the remote and push** (replace `YOUR_USERNAME` and `REPO_NAME` with your GitHub username and repo name):

   ```bash
   cd /Users/selim/data-analysis

   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
   git push -u origin main
   ```

   If you use SSH instead:

   ```bash
   git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git
   git push -u origin main
   ```

3. When prompted, sign in to GitHub (or use a personal access token for HTTPS).

## Option 2: Use GitHub CLI (if you install it later)

```bash
# Install: brew install gh   (macOS)
# Then:    gh auth login

cd /Users/selim/data-analysis
gh repo create data-analysis --public --source=. --remote=origin --push
```

## What’s already done

- `.gitignore` added (venv, `__pycache__`, etc.)
- `git init` and first commit on `main`
- All project files are committed (app, drug_comparison, mckinsey_style, README, requirements, etc.)
