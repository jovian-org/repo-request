#!/usr/bin/env python3
# Use Python 3 from the current environment when executing this script

# Checks that a request has all the required fields stated in the policy.

import sys           # Access command-line arguments and exit codes
import yaml          # Read and parse YAML files
import re            # Regular expression matching
from pathlib import Path  # Object-oriented file path handling

def load_yaml(path):
    """
    Load a YAML file and return it as a Python dictionary/object.
    """
    with open(path, "r", encoding="utf-8") as f:
        # safe_load converts YAML into Python objects safely
        return yaml.safe_load(f)
    

def validate_request(request, policy):
    """
    Validate a repository request against the repository policy.
    """
    errors = []

    # Check that all required fields are present in the request
    required_fields = [
        "repo_name",
        "business_purpose",
        "owner_team",
        "visibility",
        "data_classification"
    ]
    for field in required_fields:
        if not request.get(field):
            errors.append(f"Missing required field: {field}")
    if errors:
        return False, errors
    
    # Validate repo name
    repo_name = request["repo_name"]
    pattern = policy["repository"]["naming"]["pattern"]
    if not re.match(pattern, repo_name):
        errors.append(
            f"Repository name '{repo_name}' does not match naming policy"
        )

    # Validate repo visibility
    allowed_visibility = policy["repository"]["visibility"]["allowed"]
    if request["visibility"] not in allowed_visibility:
        errors.append(
            f"Visibility '{request['visibility']}' is not allowed"
        )

    # Validate owner team if the policy requires one
    if policy["repository"]["owner_team_allowlist"]:
        # Get list of allowed owner teams if configured
        # If not present in the YAML, default to []
        allowed_teams = policy["repository"].get("owner_team_allowlist", [])
        # Only validate if a whitelist exists (empty list means "accept any team")
        if allowed_teams and request["owner_team"] not in allowed_teams:
            errors.append(
                f"Owner team '{request['owner_team']}' is not recognized"
            )

    # Validation succeeds if no errors were collected
    return len(errors) == 0, errors


def main():
    """
    Main program entry point.

    Expected usage:
        python validate_request.py request.yml policy.yml
    
    sys.argv contains:
        sys.argv[0] = script name
        sys.argv[1] = request YAML
        sys.argv[2] = policy YAML

    Therefore total length should be 3
    """
    if len(sys.argv) != 3:
        print(
            "Usage: validate_request.py <request.yml> <policy.yml>",
            file=sys.stderr
        )
        # Exit code 2 = command usage error
        sys.exit(2)

    # Convert command-line arguments into Path objects
    request_path = Path(sys.argv[1])
    policy_path = Path(sys.argv[2])

    # Load YAML files into Python dictionaries
    request = load_yaml(request_path)
    policy = load_yaml(policy_path)

    # Run validation
    ok, errors = validate_request(request, policy)

    # Validation passed
    if ok:
        print("PASS")
        # Exit code 0 = success
        sys.exit(0)

    # Validation failed
    else:
        print("FAIL")
        # Print each validation error
        for err in errors:
            print(f"- {err}")
        # Exit code 1 = validation failure
        sys.exit(1)


# Execute main() only when this file is run directly
if __name__ == "__main__":
    main()