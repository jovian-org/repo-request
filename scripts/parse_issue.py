# Parse a GitHub issue body into request.yml

import sys
import yaml


def parse_issue_body(text):
    """
    Convert key:value lines from the issue body into a dictionary.
    """
    
    data = {}

    for line in text.splitlines():
        line = line.strip()

        # Ignore blank lines
        if not line:
            continue

        # Ignore malformed lines
        if ":" not in line:
            continue

        # Split only on the first colon
        key, value = line.split(":", 1)

        data[key.strip()] = value.strip()

    return data


def main():
    """
    Expected usage:
        python parse_issue.py issue_body.txt request.yml
    """

    if len(sys.argv) != 3:
        print(
            "Usage: parse_issue.py <issue_body.txt> <request.yml>",
            file=sys.stderr
        )
        sys.exit(2)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Read issue body extracted from GitHub
    with open(input_file, "r", encoding="utf-8") as f:
        issue_body = f.read()

    # Convert issue text into a dictionary
    request = parse_issue_body(issue_body)

    # Write structured YAML for the validator
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            request,
            f,
            sort_keys=False
        )

    print(f"Request written to {output_file}")


if __name__ == "__main__":
    main()