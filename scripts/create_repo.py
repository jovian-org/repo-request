"""
Create a new private GitHub repository from a request file or repo name.
"""

import sys      # for exiting with a status code
from pathlib import Path        # for filesystem paths
from typing import Any, Dict, Tuple # type hints

import requests     # for sending HTTP requests to GitHub
import yaml     # for reading request.yml file

from github_auth import GitHubAuthError, get_github_headers

GITHUB_API_URL = "https://api.github.com/user/repos"    # GitHub endpoint to create repo under authenticcated user


class RepoProvisionError(RuntimeError):
    """Raised when repository provisioning fails."""


def load_request_data(arg: str) -> Dict[str, Any]:
    """
    Load request data from a YAML file path or treat the argument as a raw repo name.
    """
    candidate = Path(arg)

    if candidate.exists() and candidate.is_file():
        with candidate.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        if not isinstance(data, dict):
            raise RepoProvisionError("Request YAML must contain a mapping/object.")
        return data

    return {"repo_name": arg}


def extract_repo_name(request: Dict[str, Any]) -> str:
    """
    Extract and validate the repository name from the request payload.
    """
    repo_name = request.get("repo_name")
    if not isinstance(repo_name, str) or not repo_name.strip():
        raise RepoProvisionError("Missing required field: repo_name")
    return repo_name.strip()


def create_repository(repo_name: str) -> Tuple[str, str]:
    """
    Create the repository and return (html_url, full_name).
    """
    headers = get_github_headers()      # headers to attach to the API request
    payload = {
        "name": repo_name,      # uses the repo name from the request
        "private": True,        # create a private repository
        "auto_init": True,      # create an initial commit and README
    }

    try:
        response = requests.post(       # Send an HTTP POST request to create
            GITHUB_API_URL,    # GitHub endpoint for creating repo
            headers=headers,    # attach authentication headers
            json=payload,       # send the payload as JSON
            timeout=30      # wait at most 30 seconds
            )
        response.raise_for_status()     # Raise an exception if there is an error
    except requests.HTTPError as exc:       # Catch GitHub API errors
        detail = ""
        try:
            detail = response.json().get("message", "")
        except Exception:
            detail = response.text.strip()
        raise RepoProvisionError(
            f"GitHub API rejected repository creation for '{repo_name}'. {detail}"
        ) from exc
    except requests.RequestException as exc:        # Catch lower-level problems
        raise RepoProvisionError(f"Failed to contact GitHub API: {exc}") from exc

    data = response.json()
    html_url = data.get("html_url")
    full_name = data.get("full_name")

    if not html_url or not full_name:
        raise RepoProvisionError("GitHub API response did not include repository details.")

    return html_url, full_name


def main() -> None:
    if len(sys.argv) != 2:
        raise RepoProvisionError("Usage: python scripts/create_repo.py request.yml")

    request = load_request_data(sys.argv[1])
    repo_name = extract_repo_name(request)
    html_url, _ = create_repository(repo_name)
    print(html_url)


if __name__ == "__main__":
    main()
