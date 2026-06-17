"""
Purpose: Check that a request from request.yml has all the required fields stated in config/policy
"""

import sys           # Access command-line arguments and exit codes
import yaml          # Read and parse YAML files
import re            # Regular expression matching
from pathlib import Path  # Object-oriented file path handling

def load_yaml(path):
    """
    Purpose: Load a YAML file and return it as a Python dictionary/object.
    """
    with open(path, "r", encoding="utf-8") as f:        # safe_load converts YAML into Python objects safely
        return yaml.safe_load(f)
    

def validate_request(request, policy):
    """
    Purpose: Validate a repository request against the repository policy.
    """
    errors = []

    required_fields = [
        "repo_name",
        "repo_purpose",
    ]
    for field in required_fields:
        if not request.get(field):      # Check that all required fields are present in the request
            errors.append(f"Missing required field: {field}")
    if errors:
        return False, errors
    
    repo_name = request["repo_name"]
    pattern = policy["repository"]["naming"]["pattern"]
    if not re.match(pattern, repo_name):        # Validate repo name
        errors.append(f"Repository name '{repo_name}' does not match naming policy")

    return len(errors) == 0, errors     # Validation succeeds if no errors were collected


def main():
    """
    Purpose: Main program entry point
    """
    if len(sys.argv) != 3:
        print(
            "Usage: validate_request.py <request.yml> <policy.yml>",
            file=sys.stderr
        )
        sys.exit(2)     # Exit code 2 = command usage error

    request_path = Path(sys.argv[1])        # Convert command-line arguments into Path objects
    policy_path = Path(sys.argv[2])

    request = load_yaml(request_path)       # Load YAML files into Python dictionaries
    policy = load_yaml(policy_path)

    ok, errors = validate_request(request, policy)      # Run validation

    if ok:      # Validation passed
        print("PASS")
        sys.exit(0)     # Exit code 0 = success

    else:       # Validation failed
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)     # Exit code 1 = validation failure


if __name__ == "__main__":      # Execute main() only when this file is run directly
    main()