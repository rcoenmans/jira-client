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

# Initialize the Jira client
client = JiraClient("contoso.atlassian.net", "username", "password")

# Get all the boards
boards = client.get_boards()

# Iterate through the list of boards
for board in boards:
    print(board.name)
```

Returns the board for the given board identifier. This board will only be returned if you have permission to view it.
```python
board_id = 12345
board = client.get_board(board_id)

print(board.name)
```

## Epics
Returns all epics from the board, for the given board identifier. This only includes epics that you have permission to view. Note, if you don't have permission to view the board, no epics will be returned at all.
```python
# Connect to Jira
client = JiraClient("contoso.atlassian.net", "username", "password")

# Specify a board id, start index and max results
board_id = 12345
start_at = 0
max_results = 50

# Get the (first 50) epics
epics = client.get_epics(board_id, start_at, max_results)

# Iterate the list of epics
for epic in epics:
    print(epic.name)
```