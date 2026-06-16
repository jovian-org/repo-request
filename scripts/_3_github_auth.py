"""
Purpose: Read GH_PAT, check that it exists and turn into GitHub API headers that create_repo.py will use
"""

import os       # Import Python's environment-access moduble to read GH_PAT

class GitHubAuthError(RuntimeError): # inherits RuntimeError
    """Raised when GitHub auth configuration is missing or invalid."""
    pass


def get_github_token() -> str:
    token = os.getenv("GH_PAT", "").strip()

    if not token:
        raise GitHubAuthError("Missing GH_PAT environment variable")        # Raise custom error if GH_PAT is missing or empty

    return token


def get_github_headers() -> dict[str, str]:
    token = get_github_token()

    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }