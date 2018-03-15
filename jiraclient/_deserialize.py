# -----------------------------------------------------------------------------
# The MIT License (MIT)
# Copyright (c) 2018 Robbie Coenmans
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------

from .models import (
    Project,
    Board,
    Issue,
    Sprint,
    Attachment,
    User,
    Comment,
    Epic,
    Worklog,
    Component
)

def _parse_json_to_class(response, result_class, attrs):
    values = []
    for value in response['values']:
        values.append(_map_attrs_values(result_class, attrs, value))
    return values

def _get_attr_value(attr, values, default=None):
    if attr in values:
        return values[attr]
    else:
        return default

def _map_attrs_values(result_class, attrs, values):
    result = result_class()
    for attr in attrs:
        if attr in values:
            setattr(result, attr, _get_attr_value(attr, values))
    return result

def _parse_json_to_issues(response):
    issues = []
    for issue in response['issues']:
        issues.append(_parse_json_to_issue(issue))
    return issues

def _parse_json_to_issue(response):
    issue = Issue()
    issue.id          = _get_attr_value('id', response)
    issue.key         = _get_attr_value('key', response)
    issue.summary     = _get_attr_value('summary', response['fields'])
    issue.description = _get_attr_value('description', response['fields'])
    issue.labels      = _get_attr_value('labels', response['fields'], [])

    issue.type        = response['fields']['issuetype']['name']
    issue.status      = response['fields']['status']['name']
    
    issue.created     = response['fields']['created']
    issue.updated     = response['fields']['updated']

    issue.creator = User()
    issue.creator.name    = response['fields']['creator']['name']
    issue.creator.email   = response['fields']['creator']['emailAddress']
    issue.creator.display = response['fields']['creator']['displayName']

    issue.reporter = User()
    issue.reporter.name    = response['fields']['reporter']['name']
    issue.reporter.email   = response['fields']['reporter']['emailAddress']
    issue.reporter.display = response['fields']['reporter']['displayName']

    if response['fields']['priority']:
        issue.priority = response['fields']['priority']['name']

    if response['fields']['assignee']:
        issue.assignee = User()
        issue.assignee.name    = response['fields']['assignee']['name']
        issue.assignee.email   = response['fields']['assignee']['emailAddress']
        issue.assignee.display = response['fields']['assignee']['displayName']

    if 'project' in response['fields']: 
        if response['fields']['project']:
            issue.project = _parse_json_to_project(response['fields']['project'])

    if 'epic' in response['fields']:
        if response['fields']['epic']:
            issue.epic = _parse_json_to_epic(response['fields']['epic'])
    
    if 'closedSprints' in response['fields']:
        for resp in response['fields']['closedSprints']:
            issue.closed_sprints.append(_parse_json_to_sprint(resp)) 

    if 'sprint' in response['fields']:
        if response['fields']['sprint']:
            issue.sprint = _parse_json_to_sprint(response['fields']['sprint'])

    if 'comment' in response['fields']:
        for resp in response['fields']['comment']['comments']:
            issue.comments.append(_parse_json_to_comment(resp))

    if 'attachment' in response['fields']:
        for resp in response['fields']['attachment']:
            issue.attachments.append(_parse_json_to_attachement(resp))

    if 'worklog' in response['fields']:
        for resp in response['fields']['worklog']['worklogs']:
            issue.worklog.append(_parse_json_to_worklog(resp))

    if 'components' in response['fields']:
        for resp in response['fields']['components']:
            issue.components.append(_parse_json_to_component(resp))

    for key, value in response['fields'].items():
        if key.startswith('customfield_'):
            issue.custom[key] = value
            
    return issue

def _parse_json_to_sprints(response):
    sprints = []
    for value in response['values']:
        sprints.append(_parse_json_to_sprint(value))
    return sprints

def _parse_json_to_sprint(response):
    sprint = Sprint()
    sprint.id    = _get_attr_value('id', response)
    sprint.state = _get_attr_value('state', response)
    sprint.name  = _get_attr_value('name', response)
    sprint.goal  = _get_attr_value('goal', response)
    
    sprint.board_id      = _get_attr_value('originBoardId', response)
    sprint.start_date    = _get_attr_value('startDate', response)
    sprint.end_date      = _get_attr_value('endDate', response)
    sprint.complete_date = _get_attr_value('completeDate', response)
    return sprint

def _parse_json_to_board(response):
    attrs = ['id', 'name', 'type', 'location']
    return _map_attrs_values(Board, attrs, response)

def _parse_json_to_epic(response):
    attrs = ['id', 'name', 'key', 'summary', 'done']
    return _map_attrs_values(Epic, attrs, response)

def _parse_json_to_project(response):
    attrs = ['id', 'key', 'name']
    return _map_attrs_values(Project, attrs, response)

def _parse_json_to_attachement(response):
    attachment = Attachment()
    attachment.id       = response['id'] 
    attachment.filename = response['filename']
    attachment.created  = response['created']
    attachment.size     = response['size']
    attachment.mime     = response['mimeType']
    attachment.content  = response['content']

    attachment.author = User()
    attachment.author.name    = response['author']['name']
    attachment.author.email   = response['author']['emailAddress'] 
    attachment.author.display = response['author']['displayName']
    return attachment

def _parse_json_to_comment(response):
    comment = Comment()
    comment.id      = response['id']
    comment.body    = response['body']
    comment.created = response['created']
    comment.updated = response['updated']

    comment.author = User()
    comment.author.name    = response['author']['name']
    comment.author.email   = response['author']['emailAddress']
    comment.author.display = response['author']['displayName']
    return comment

def _parse_json_to_worklog(response):
    worklog = Worklog()
    worklog.id = response['id']

    worklog.issue_id = response['issueId']
    worklog.updated  = response['updated']
    worklog.comment  = response['comment']
    
    worklog.author = User()
    worklog.author.name    = response['author']['name']
    worklog.author.display = response['author']['displayName'] 
    return worklog

def _parse_json_to_component(response):
    attrs = ['id', 'name', 'description']
    return _map_attrs_values(Component, attrs, response)