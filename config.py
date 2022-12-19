import os
import sys
import pytz

# Credentials for Jira.
jira_url = os.getenv("JIRA_URL")
if jira_url is None:
    print("Please set the JIRA_URL environment variable.")
    sys.exit(1)
api_token = os.getenv("JIRA_API_TOKEN")
if api_token is None:
    print("Please set the JIRA_API_TOKEN environment variable.")
    sys.exit(1)

# Localization for timestamps in Jira issues.
timezone = pytz.timezone("America/New_York")

# Team code
team_code = 2035
