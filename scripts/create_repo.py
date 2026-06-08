# Create a private repository using a GitHub App.

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

# Helper for GitHub App authentication.
from github_auth import get_installation_token

load_dotenv()

def create_repository(repo_name: str) -> str:
    """Create a private GitHub repository and return its URL."""

    # Read GitHub App credentials from environment variables.
    app_id = os.environ["GH_APP_ID"]
    installation_id = os.environ["GH_APP_INSTALLATION_ID"]
    private_key = os.environ["GH_APP_PRIVATE_KEY"]

    # Read the PEM key from file.
    with open(Path(private_key), "r", encoding="utf-8") as f:
        private_key = f.read()

    # Get a temporary token for the App installation.
    token = get_installation_token(app_id, installation_id, private_key)

    # Create the repository under the authenticated account.
    response = requests.post(
        "https://api.github.com/user/repos",
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
        },
        json={
            "name": repo_name,
            "private": True,
            "auto_init": True,
        },
        timeout=30,
    )

    print(response.status_code)
    print(response.text)
    print(response.headers.get("X-Accepted-GitHub-Permissions"))

    # Stop immediately if GitHub rejects the request.
    response.raise_for_status()

    # Return the repository URL from the API response.
    return response.json()["html_url"]


def main() -> None:
    """
    Expected usage: python scripts/create_repo.py issueops-test-repo
    """

    # Expect exactly one argument: the repository name.
    if len(sys.argv) != 2:
        print("Usage: python scripts/create_repo.py <repository-name>")
        sys.exit(1)

    repo_url = create_repository(sys.argv[1])
    print(repo_url)


if __name__ == "__main__":
    main()