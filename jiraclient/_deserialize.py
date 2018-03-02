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
    Epic
)

def _parse_json_to_class(response, result_class, attrs):
    values = []
    for value in response['values']:
        values.append(_map_attrs_values(result_class, attrs, value))
    return values

def _map_attrs_values(result_class, attrs, values):
    result = result_class()
    for attr in attrs:
        if attr in values:
            setattr(result, attr, values[attr])
    return result
    
def _parse_json_to_issues(response):
    issues = []
    for issue in response['issues']:
        issues.append(_parse_json_to_issue(issue))
    return issues

def _parse_json_to_issue(response):
    issue = Issue()
    issue.id          = response['id']
    issue.key         = response['key']
    issue.summary     = str(response['fields']['summary'])
    issue.description = str(response['fields']['description'])
        
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

    if 'comment' in response['fields']:
        for resp in response['fields']['comment']['comments']:
            comment = Comment()
            comment.id      = resp['id']
            comment.body    = resp['body']
            comment.created = resp['created']
            comment.updated = resp['updated']

            comment.author = User()
            comment.author.name    = resp['author']['name']
            comment.author.email   = resp['author']['emailAddress']
            comment.author.display = resp['author']['displayName']

            issue.comments.append(comment)

    if 'attachment' in response['fields']:
        for resp in response['fields']['attachment']:
            attachment = Attachment()
            attachment.id       = resp['id'] 
            attachment.filename = resp['filename']
            attachment.created  = resp['created']
            attachment.size     = resp['size']
            attachment.mime     = resp['mimeType']
            attachment.content  = resp['content']

            attachment.author = User()
            attachment.author.name    = resp['author']['name']
            attachment.author.email   = resp['author']['emailAddress'] 
            attachment.author.display = resp['author']['displayName'] 
            
            issue.attachments.append(attachment)

    return issue

def _parse_json_to_sprints(response):
    sprints = []
    for value in response['values']:
        sprints.append(_parse_json_to_sprint(value))
    return sprints

def _parse_json_to_sprint(response):
    sprint = Sprint()
    sprint.id    = response['id']
    sprint.state = response['state']
    sprint.name  = response['name']
    sprint.goal  = response['goal']
    
    sprint.board_id      = response['originBoardId']
    sprint.start_date    = response['startDate']
    sprint.end_date      = response['endDate']
    sprint.complete_date = response['completeDate']
    
    return sprint

def _parse_json_to_board(response):
    attrs = ['id', 'name', 'type', 'location']
    return _map_attrs_values(Board, attrs, response)

def _parse_json_to_epic(response):
    attrs = ['id', 'name', 'key', 'summary', 'done']
    return _map_attrs_values(Epic, attrs, response)