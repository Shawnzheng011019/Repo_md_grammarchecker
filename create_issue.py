# create_issue.py - GitHub issue creation module
from github import Github, Auth
import os
import jwt
from datetime import datetime, timedelta

def generate_jwt(private_key_path, app_id):
    """Generate a JWT for GitHub App authentication"""
    with open(private_key_path, 'r') as f:
        private_key = f.read()
    
    # Generate the JWT
    payload = {
        # Issued at time
        'iat': int(datetime.now().timestamp()),
        # JWT expiration time (10 minutes maximum)
        'exp': int((datetime.now() + timedelta(minutes=9)).timestamp()),
        # GitHub App's identifier
        'iss': app_id
    }
    
    return jwt.encode(payload, private_key, algorithm='RS256')

def get_installation_token(jwt_token, installation_id):
    """Get an installation token using the JWT"""
    import requests
    
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    response = requests.post(
        f'https://api.github.com/app/installations/{installation_id}/access_tokens',
        headers=headers
    )
    
    if response.status_code == 201:
        return response.json()['token']
    else:
        raise Exception(f"Failed to get installation token: {response.status_code} - {response.text}")

def create_github_issue(md_path, analysis_result, app_key_path, repo_name, local_path, app_id, installation_id):
    """Create GitHub issue using GitHub App authentication"""
    try:
        # Generate JWT
        jwt_token = generate_jwt(app_key_path, app_id)
        
        # Get installation token
        installation_token = get_installation_token(jwt_token, installation_id)
        
        # Authenticate with GitHub using the installation token
        auth = Auth.Token(installation_token)
        g = Github(auth=auth)
        
        # Get the repository
        repo = g.get_repo(repo_name)
        
        # Create meaningful issue title
        issue_title = f"Documentation improvement suggestion: {os.path.basename(md_path)}"
        
        # Construct issue body
        rel_path = os.path.relpath(md_path, local_path)
        issue_body = f"""### Document Path
{rel_path}

### Analysis Result
{analysis_result}

### Suggested Action
Please make corresponding modifications and optimizations to the documentation based on the above analysis results.
"""
        
        # Create the issue
        issue = repo.create_issue(
            title=issue_title,
            body=issue_body,
            labels=["documentation", "enhancement"]
        )
        print(f"Issue created: {issue.html_url}")
        return issue
    except Exception as e:
        print(f"Error creating issue: {e}")
        return None