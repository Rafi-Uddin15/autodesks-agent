# 🐙 How to Upload to GitHub

Since **Git** is not installed on your computer, I cannot automate the upload for you. Here is how to do it manually.

## Step 1: Restart Terminal
**Git has been installed!** 🎉

However, your current terminal doesn't see it yet.
1.  **Close this terminal** (or VS Code).
2.  **Open it again**.
3.  Type `git --version` to confirm it works.

## Step 2: Create a Repository
1.  Go to [GitHub.com](https://github.com) and sign in.
2.  Click the **+** icon in the top right -> **New repository**.
3.  Name it `autodesk-agent`.
4.  Click **Create repository**.

## Step 3: Upload Your Code
Open your terminal in the `autodesk` folder and run these commands one by one:

```bash
# 1. Initialize Git
git init

# 2. Add all files
git add .

# 3. Save the changes
git commit -m "Initial commit of AutoDesk Agent"

# 4. Link to your new GitHub repo (Replace URL with yours!)
git remote add origin https://github.com/YOUR_USERNAME/autodesk-agent.git

# 5. Upload
git push -u origin main
```

## Step 4: Show it Off!
Add the link to your new repo on your **LinkedIn** or **Portfolio**.
