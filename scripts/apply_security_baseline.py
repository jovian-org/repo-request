import os
import sys
import requests

from github_auth import get_installation_token


def update_repository_metadata(repo_name: str) -> None:
    """Update simple repository metadata."""

    # Read GitHub App credentials from environment.
    app_id = os.environ["GH_APP_ID"]
    installation_id = os.environ["GH_APP_INSTALLATION_ID"]
    private_key = os.environ["GH_APP_PRIVATE_KEY"]

    # Get a short-lived token for the GitHub App installation.
    token = get_installation_token(app_id, installation_id, private_key)

    owner = "jovianheok"
    url = f"https://api.github.com/repos/{owner}/{repo_name}"

    # Update a few repo fields first.
    response = requests.patch(
        url,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
        },
        json={
            "description": "Repository provisioned by IssueOps",
            "homepage": "https://github.com/jovianheok",
        },
        timeout=30,
    )

    response.raise_for_status()
    print(f"Updated metadata for {owner}/{repo_name}")


def main() -> None:
    """
    Expected usage: python scripts/apply_security_baseline.py issueops-test-repo
    """

    if len(sys.argv) != 2:
        print("Usage: python scripts/apply_security_baseline.py <repository-name>")
        sys.exit(1)

    update_repository_metadata(sys.argv[1])


if __name__ == "__main__":
    main()