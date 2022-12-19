# JIRA Stats Visualizer

Just run `python main.py`.

Make sure your JIRA URL and API token are defined as `JIRA_URL` and `JIRA_API_TOKEN` environment variables.

For additional info, you can specify the log level, e.g.:

```python
python main.py --log [info|debug]
```

### Changelog

**v0.1**: Add plottng cycle-time vs story-points and saving the result as a .png image.

## Credits

###### Jira-Dora

A bulk of the code for handling Jira requests has been taken from Jira-dora repo. You can see it [here](https://github.com/celeborne/jira-dora).
