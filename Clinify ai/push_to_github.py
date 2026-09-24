"""
CareTranslate AI - GitHub Push Helper
Uses pure-Python Dulwich (no git.exe required).
Usage:
    python push_to_github.py <YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>
or set GITHUB_TOKEN environment variable and run:
    python push_to_github.py
"""
import sys
import os
import dulwich.porcelain as porcelain
from dulwich.repo import Repo

def main():
    token = os.environ.get("GITHUB_TOKEN")
    if len(sys.argv) > 1:
        token = sys.argv[1].strip()

    if not token:
        print("\n=======================================================")
        print("CareTranslate AI - Push to GitHub")
        print("=======================================================")
        print("Please provide a GitHub Personal Access Token (PAT) with repo scope.")
        print("How to generate one:")
        print("1. Go to https://github.com/settings/tokens?type=beta or https://github.com/settings/tokens")
        print("2. Generate a token with 'repo' permissions")
        print("3. Run: python push_to_github.py <YOUR_TOKEN>\n")
        sys.exit(1)

    repo_dir = os.path.dirname(os.path.abspath(__file__))
    repo = Repo(repo_dir)
    remote_url = f"https://oauth2:{token}@github.com/poornisha07/Care-Translate-AI.git"
    
    print(f"Connecting to https://github.com/poornisha07/Care-Translate-AI.git...")
    try:
        porcelain.push(repo, remote_url, "refs/heads/main", force=True)
        print(" Successfully pushed all CareTranslate AI files to https://github.com/poornisha07/Care-Translate-AI !")
    except Exception as e:
        print(f" Push failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
