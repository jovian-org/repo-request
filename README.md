# GitHub-recognized Directory and their uses

.github/workflows/ -> GitHub Actions automation
.github/ISSUE_TEMPLATE/ -> Issue Forms and Issue Templates
.github/PULL_REQUEST_TEMPLATE.md -> Default Pull Request template
.github/CODEOWNERS -> Automatic reviewer assignment
.github/dependabot.yml -> Automated dependency updates
.github/FUNDING.yml -> Sponsorship links for open-source projects
.github/SECURITY.md -> Tells researchers how to report vulnerabilities and security support policy
.github/SUPPORT.md -> Explains where to ask questions and how to get help
.github/CONTRIBUTING.md -> Displayed when users create Issues or Pull Requests


# GitHub Workflow File

Has 3 main parts
    1. name: human-readable name shown in GitHub Actions
    2. on: defines the event that triggers the workflow
    3. jobs: the work to perform

Independent event-driven workflows
    Each one runs only when its own trigger matches


# GitHub Workflow Job

run -> tell GitHub exactly what command to execute
uses -> tell GitHub to execute a prebuilt Action

# Command-Line Tool
git clone ...
docker build ...
python parse_issue.py ...

# API

Application Programming Interface is a way for one program to ask another program to do something. E.g. instead of clicking buttons in the GitHub website, your code sends a request to GitHub.


# REST API

REST is a style of web API where everything is accessed through URLs and HTTP methods. Each resource (repository, issue, pull request, label, user) has a URL.


# HTTP Methods

GET = Read
e.g. GET /repos/jovianheok/repo-requests/issues/23 = Give me Issue #23

POST = Create
e.g. POST /repos/jovianheok/repo-requests/issues/23/labels = Add/create labels on Issue #23

PATCH = Update
e.g. PATCH /repos/jovianheok/repo-requests/issues/23 = Update Issue #23

DELETE = Remove
e.g. DELETE /repos/jovianheok/repo-requests/issues/23/labels/needs-changes = Remove the label needs-changes


# SHEBANG
A shebang tells the operating system which interpreter should run a script when the script is executed directly e.g. #!/usr/bin/python3


# TRIGGER FOR EACH WORKFLOW
request-validation: 
    User creates issue
    User edits issue
    User reopens issue

request-approval:
    Comment created on an issue

repo-provision:
    Label added to an issue


# ISSUE CREATION PROCESS

1. User clicks "New Issue"
2. GitHub reads .github/ISSUE_TEMPLATE/repo-request.yml
3. GitHub generates the Repository Request form
4. User fills in required fields (repo name, visibility, owner team, etc.)
5. User submits the form
6. GitHub creates a normal Issue with the form responses in the issue body and stores it as Markdown


# ISSUE PARSING and VALIDATION WORKFLOW (request-validation.yml)

1. When an Issue is opened, GitHub starts validate-request.yml workflow
2. Workflow extracts the issue body
3. Workflow runs the parser (parse_issue.py) which inputs issue_body.txt and outputs request.yml as structured data
4. Workflow runs the validator (validate_request.py) which reads request.yml and compares it against config/policy.yml to mark as 'pending-approval' or 'needs-changes'
5. If 'pending-approval', it will create an Issue Comment to mention the approval
6. If 'need-changes', it will create an Issue Comment to notify the requestor of the errors.


# ISSUE APPROVAL PROCESS (request-approval.yml)

1. Workflow receives a 'pending-approval' request and notifies approver
2. Approver comments which creates an Issue Comment (each comment starts a workflow)
3. If Issue Comment == /approve or /reject, GitHub starts request-approval.yml workflow
4. Workflow verifies approver against config/approvers.yml
5. Workflow verifies Issue's state to ensure it is 'pending-approval'
6. If Comment = /approve AND User is approver AND Issue is pending-approval, 'approved' label is applied
7. If Comment = /reject AND User is approver, 'rejected' label is applied


# REPO PROVISION PROCESS (repo-provision.yml)

1.
2.
3.
4.

