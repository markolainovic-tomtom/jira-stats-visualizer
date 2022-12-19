import time

from jira_facade import JiraFacade

from config import jira_url, api_token, team_code
from utils import init_argparser, save_cycle_times_stats_image


if __name__ == "__main__":
    init_argparser()
    jira = JiraFacade(jira_url=jira_url,
                      api_token=api_token,
                      team_code=team_code)
    save_cycle_times_stats_image(
        jira_client=jira, story_points=2, months_ago=6)
    time.sleep(1)
    save_cycle_times_stats_image(
        jira_client=jira, story_points=3, months_ago=6)
    time.sleep(1)
    save_cycle_times_stats_image(
        jira_client=jira, story_points=5, months_ago=6)
