# Jira Client
This project provides a client library for working with Jira boards/issues/tasks.

## Installation
```
pip install jira-client
```

## Boards
Returns all boards. This only includes boards that you have permission to view.
```python
from jiraclient.jiraclient import JiraClient

client = JiraClient("contoso.atlassian.net", "username", "password")
boards = client.get_boards()

for board in boards:
    print(board.name)
```