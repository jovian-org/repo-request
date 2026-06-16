"""
Purpose: Build a human-friendly display of the issue form for the approval to read in email notification
"""

import yaml
import sys

with open(sys.argv[1]) as f:
    request = yaml.safe_load(f)

body = f"""## Repository Request

**Repository Name**
{request.get('repo_name', '')}

**Purpose**
{request.get('repo_purpose', '')}

**Owner Team**
{request.get('owner_team', '')}

**Additional Notes**
{request.get('additional_notes') or 'None'}

**Approval Instructions**

To approve this request, reply with:
`/approve`

To reject this request, reply with:
`/reject`

Then provide the reason for rejection below the command.
"""

print(body)