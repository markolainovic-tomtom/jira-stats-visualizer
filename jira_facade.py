from typing import List
import logging
import datetime

from atlassian import Jira
from dateutil import parser


from config import timezone


class JiraException(RuntimeError):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return self.msg


class JiraFacade:
    # fields needed for this report - these are embedded in the json returned from Jira
    # there are many, but these are the ones we're concerned with
    FIELDS = ["key", "summary", "resolution", "issuetype",
              "created", "resolutiondate", "status", "changelog"]

    def __init__(self, jira_url: str, api_token: str, team_code) -> None:
        self.jira = Jira(url=jira_url, token=api_token, cloud=False)
        self.team_code = team_code

    def fetch_all_issues(self, story_points: int = 3, months_ago: int = 6) -> List[str]:
        cls = self.__class__
        query = f"""
        team = {self.team_code}
         AND issuetype = 'User Story'
         AND 'Story Points' = {story_points}
         AND resolved > startOfDay(-{months_ago}M)
         AND status = Done
         AND resolution = Done
         ORDER BY created DESC
        """

        # Jira limits response data to 100 issues, so this provides pagination workaround.
        issues_per_query = 100
        issues = []

        # Get the total number of issues in the results set.
        logging.info(f"Sending query: {query}.")
        res = self.jira.jql(jql=query, limit=0)
        if type(res) is not dict:
            raise JiraException(
                "The response from JIRA is not a valid dictionary.. Check your authentication credentials.")
        total_issues_count = res["total"]
        logging.info(f"Query returned {total_issues_count} issues.")

        # Use floor division + 1 to calculate the number of requests needed to get all issues.
        for query_number in range(0, (total_issues_count // issues_per_query) + 1):
            res = self.jira.jql(jql=query, limit=issues_per_query,
                                start=query_number * issues_per_query,
                                fields=cls.FIELDS, expand="changelog")

            # Append each subsequent query to the list, specifically, only values for the "issues" key.
            issues.extend(res["issues"])

        return issues

    @classmethod
    def get_cycle_times(cls, issues: list) -> str:
        cycletime_delta: datetime.timedelta = datetime.timedelta(0)
        skipped: int = 0

        cycle_times = []
        for issue in issues:
            in_progress_timestamp = cls._get_issue_element(
                issue, issue_type="In Progress", return_oldest=True)
            completed_timestamp = cls._get_issue_element(
                issue, issue_type="Done", return_oldest=False)
            if in_progress_timestamp and completed_timestamp:
                cycletime_delta = completed_timestamp - in_progress_timestamp
                cycle_times.append(cycletime_delta.days)
            else:
                skipped += 1

        if skipped > 0:
            logging.info(f"""
            Skipped issues: {skipped}.
            (Skipped issues are the issues that went from "Created", or "Backlog", to "Done" without ever being "In Progress".)
            """)

        return cycle_times

    def _get_issue_element(issue: dict, issue_type: str, return_oldest: datetime) -> datetime:
        """
        Collect and order the timestamps when an issue is transitioned from one state to "Done".
        Use the most recent transition for calculations.
        """
        if return_oldest:
            date_track = datetime.datetime.strptime("2999-12-31", "%Y-%m-%d")
        else:
            date_track = datetime.datetime.strptime("1970-01-01", "%Y-%m-%d")
        date_track = timezone.localize(date_track)

        # timestamps are nested in the JSON structure, here we drill down into their location
        # and check to see whether the status is commensurate with what we're looking for, ie
        # history item set to "In Progress", "Done", or "Ready to Release"
        for history in issue["changelog"]["histories"]:
            for item in history["items"]:
                to_string = item["toString"]
                if to_string == issue_type:
                    this_ts = parser.parse(history["created"])
                    if return_oldest:
                        if this_ts < date_track:
                            date_track = this_ts
                    else:
                        if this_ts > date_track:
                            date_track = this_ts
        if date_track.year == 2999 or date_track.year == 1970:
            return None
        return date_track
