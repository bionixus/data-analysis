# Upload this project to GitHub

The repo is already initialized with commits on branch `main`. Follow one option below.

## Option 1: GitHub CLI (recommended — you have `gh` installed)

**1. Log in to GitHub (one-time):**

```bash
gh auth login
```

Choose: GitHub.com → HTTPS → Yes (authenticate Git) → Login with a web browser. Complete the sign-in in your browser.

**2. Create the repo and push from this folder:**

```bash
cd /Users/selim/data-analysis
gh repo create data-analysis --public --source=. --remote=origin --description "GHD drug comparison dashboard (Streamlit, McKinsey style)" --push
```

This creates **https://github.com/YOUR_USERNAME/data-analysis** and pushes `main`. Use a different name if you prefer, e.g. `gh repo create ghd-drug-comparison --public --source=. --remote=origin --push`.

---

## Option 2: Create repo on GitHub in the browser, then push

1. **Create a new repository on GitHub**
   - Go to [https://github.com/new](https://github.com/new)
   - Repository name: e.g. `data-analysis` or `ghd-drug-comparison`
   - Description (optional): "GHD drug comparison dashboard (McKinsey style)"
   - Choose **Public**
   - Do **not** add a README, .gitignore, or license (they already exist here)
   - Click **Create repository**

2. **Add the remote and push** (replace `YOUR_USERNAME` and `REPO_NAME` with your GitHub username and repo name):

   ```bash
   cd /Users/selim/data-analysis
   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
   git push -u origin main
   ```

   If you use SSH:

   ```bash
   git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git
   git push -u origin main
   ```

3. When prompted, sign in to GitHub (or use a personal access token for HTTPS).

---

## What’s already done

- `.gitignore` added (venv, `__pycache__`, etc.)
- Git initialized with commits on `main`
- Project files committed (app.py, drug_comparison, mckinsey_style, README, requirements, etc.)
