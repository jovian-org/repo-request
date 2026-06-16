"""
Purpose: Verify that the person who commented /approve belongs to an allowed GitHub approver team defined in config/approvers.yml
"""

import os
import sys
import yaml
import requests

commenter = os.environ["COMMENTER"]
org = os.environ["ORG_NAME"]
token = os.environ["GH_PAT"]

with open("config/approvers.yml", "r", encoding="utf-8") as f:      # Load approver teams from config/approvers.yml
    config = yaml.safe_load(f)

teams = config["approvers"]["teams"]

headers = {
    "Authorization": f"Bearer {token}",     # Authenticate GitHub API requests using the PAT
    "Accept": "application/vnd.github+json",        # Request responses in GitHub JSON format
    "X-GitHub-Api-Version": "2022-11-28",       # Use a fixed GitHub REST API version
}

for team in teams:      # Check whether the commenter belongs to any allowed approver team
    
    url = (                                                 
        f"https://api.github.com/orgs/{org}/teams/"
        f"{team}/memberships/{commenter}"
    )

    response = requests.get(url, headers=headers)       # # GET /orgs/{org}/teams/{team}/memberships/{username} sends an authenticated request to check if the commenter belongs to the specified approver team

    if response.status_code == 200:     # 200 means GitHub found a membership record
        if response.json().get("state") == "active":        # success only if membership record is found and is active
            print(
                f"Authorized approver: "
                f"{commenter} (team={team})"
            )
            sys.exit(0)

print(f"Unauthorized approver: {commenter}")
sys.exit(1)     # fail the workflow step if no matching team membership found