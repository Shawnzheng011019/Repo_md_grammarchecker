import os
import subprocess

def update_repo(repo_url, local_path):
    """Update or clone repository"""
    if os.path.exists(local_path):
        print("Updating repository...")
        subprocess.run(["git", "-C", local_path, "pull"], check=True)
    else:
        print("Cloning repository...")
        subprocess.run(["git", "clone", repo_url], check=True)    