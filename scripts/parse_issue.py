"""
Purpose: Parse a GitHub issue body from issue_body.txt into request.yml
"""

import sys
import yaml
import re

EXPECTED_KEYS = [
    "repo_name",
    "repo_purpose",
    "owner_team",
    "additional_notes",
]

LABEL_MAP = {
    "Repository name": "repo_name",
    "Repository purpose": "repo_purpose",
    "Owner team": "owner_team",
    "Additional notes": "additional_notes",
}

NO_RESPONSE_MARKERS = {"_No response_", "No response"}

def normalize_value(value: str) -> str:
    value = value.strip()
    if value in NO_RESPONSE_MARKERS:
        return ""       # Return empty string if no response
    return value


def parse_issue_body(text):
    data = {key: "" for key in EXPECTED_KEYS}

    current_key = None
    buffer = []

    def flush():
        nonlocal current_key, buffer        # Use current_key and buffer from enclosing function
        if current_key is not None:
            data[current_key] = normalize_value("\n".join(buffer))      # Store the value under the current field name
        current_key = None      # Reset current_key and buffer after saving it
        buffer = []

    lines = text.splitlines()       # Break issue body into separate lines to inspect one line at a time

    for raw_line in lines:
        line = raw_line.strip()     # Remove leading and trailing whitespace from the line

        if not line:
            continue        # Skip blank lines

        heading_match = re.match(r"^#{1,6}\s+(.+)$", line)      # Check whether the line is a markdown heading
        if heading_match:
            flush()     # Save the previous field before moving on to the next one
            label = heading_match.group(1).strip()      # Extract the heading text itself
            current_key = LABEL_MAP.get(label)      # Convert the visible label into the stable YAML key
            continue

        if current_key is not None:
            buffer.append(line)     # Collect value lines after a heading

    flush()     # Save the field collected in buffer to the YAML key
    return data


def main():
    if len(sys.argv) != 3:
        print("Usage: parse_issue.py <issue_body.txt> <request.yml>", file=sys.stderr)
        sys.exit(2)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, "r", encoding="utf-8") as f:
        issue_body = f.read()

    request = parse_issue_body(issue_body)

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(request, f, sort_keys=False)

    print(f"Request written to {output_file}")


if __name__ == "__main__":
    main()