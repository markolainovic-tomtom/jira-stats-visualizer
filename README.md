# JIRA Stats Visualizer

Calculate stats from JIRA issues and visualize them.

Current features:

- [Boxplot](https://en.wikipedia.org/wiki/Box_plot): Cycle-time (in days) distribution vs story-points.

## Usage

As an example, run `python main.py`.

Make sure that JIRA URL and API token are defined as `JIRA_URL` and `JIRA_API_TOKEN` environment variables.

For additional info, you can specify the log level, e.g.:

```python
python main.py --log [info|debug]
```

### Changelog

**v0.1**: Add plottng cycle-time vs story-points and saving the result as a .png image.

## Credits

###### Jira-Dora

A bulk of the code for handling Jira requests has been taken from [here](https://github.com/celeborne/jira-dora).
