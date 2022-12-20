import argparse
import logging

from jira_facade import JiraFacade
from box_plotter import BoxPlotter


def init_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log",
        default="warning",
        help=(
            "Provide logging level. "
            "Example --log debug', default='warning'"),
    )
    options = parser.parse_args()
    levels = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }
    level = levels.get(options.log.lower())
    if level is None:
        raise ValueError(
            f"log level given: {options.log}"
            f" -- must be one of: {' | '.join(levels.keys())}")
    logging.basicConfig(level=level)
    logger = logging.getLogger(__name__)


def save_cycle_time_boxplot(jira_client: JiraFacade, story_points, months_ago, ylims):
    issues = jira_client.fetch_issues(story_points, months_ago)
    logging.info(
        f"Number of {story_points} SP issues in the past {months_ago} months: {len(issues)}.")
    cycle_times = jira_client.get_cycle_times(issues)
    logging.info(f"Cycle times in days: {cycle_times}.")
    plotter = BoxPlotter(cycle_times)
    plotter.plot(
        title=f"Cycle time for {story_points}SP issues", ylabel="Days", ylims=ylims)
