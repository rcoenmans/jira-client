# Jira Client
This project provides a client library for working with Jira boards, epics, sprints and issues.

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
# Initialize the Jira client
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

## Sprints
Returns the sprints for a given board identifier.
```python
client = JiraClient("contoso.atlassian.net", "username", "password")
        
board_id = 12345
sprints = client.get_sprints_for_board(board_id)

# Iterate the list of sprints
for sprint in sprints:
    print('{}: {} - {}'.format(sprint.name, sprint.start_date, sprint.end_date))
```
Returns the active sprint for a given board identifier.
```python
client = JiraClient("contoso.atlassian.net", "username", "password")
        
board_id = 12345
active_sprint = client.get_active_sprint(board_id)
print(active_sprint.goal)
```
Returns the sprint for a given sprint identifier.
```python
client = JiraClient("contoso.atlassian.net", "username", "password")
        
sprint_id = 123
sprint = client.get_sprint(sprint_id)
print(sprint.name)
```