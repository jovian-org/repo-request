#!/usr/bin/env python3

# Verifies that the commenter is an authoried approver against config/approvers.yml

import os
import sys
import yaml

commenter = os.environ["COMMENTER"]

with open("config/approvers.yml", "r", encoding="utf-8") as f:      
    # 'r': read, 'w': write, 'a': append
    # Read the file as UTF-8 text where UTF-8 is the standard text encoding used almost everywhere.

    cfg = yaml.safe_load(f)     # Convert YAML into Python objects

users = set(
    cfg.get("approvers", {}).get("users", [])
)

if commenter not in users:
    print(f"Unauthorized approver: {commenter}")
    sys.exit(1)

print(f"Authorized approver: {commenter}")