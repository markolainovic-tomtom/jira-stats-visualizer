# JIRA Stats Visualizer

Calculate stats from JIRA issues for a particular team and visualize them.

Current features:

- [Boxplot](https://en.wikipedia.org/wiki/Box_plot): Cycle-time (in days) distribution vs story-points.

## Usage

Install the required packages via:

```python
pip install requirements.txt
```

Then, as an example, run `python example.py`.

Make sure that:

- JIRA URL and JIRA API token are defined as `JIRA_URL` and `JIRA_API_TOKEN` environment variables.
- Have a proper value for `team_code` (equal to the `Team` field value in JIRA issues) in the `config.py` file.

For additional info, you can specify the log level, e.g.:

```python
python example.py --log [info|debug]
```

### Changelog

**v0.1**: Add plottng cycle-time vs story-points and saving the result as a .png image.

## Credits

###### Jira-Dora

A bulk of the code for handling Jira requests has been taken from [here](https://github.com/celeborne/jira-dora).
