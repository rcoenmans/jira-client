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

import requests
import json

from ._http import HTTPRequest
from ._http.httpclient import _HTTPClient

from ._auth import _get_auth_header
from .models import (
    Board,
    Project,
    Epic,
    Sprint,
    Issue
)
from ._deserialize import (
    _parse_json_to_class,
    _parse_json_to_issues,
    _parse_json_to_issue,
    _parse_json_to_board,
    _parse_json_to_epic
)

class JiraClient(object):
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password

        self._http_client = _HTTPClient(
            protocol = 'HTTPS',
            session  = requests.Session(),
            timeout  = 30,
        )

    def set_proxy(self, host, port, user, password):
        self._http_client.set_proxy(host, port, user, password)

    def set_session_token(self, session_id, token):
        self._http_client.set_session_token(session_id, token)

    # GET /rest/agile/latest/board
    def get_boards(self):
        request = HTTPRequest()
        request.method = 'GET'
        request.path = '/rest/agile/latest/board'
        return self._perform_request(request, _parse_json_to_class, Board, ['id', 'name', 'type', 'location'])

    # GET /rest/agile/latest/board/{boardId}
    def get_board(self, board_id):
        request = HTTPRequest()
        request.method = 'GET'
        request.path = '/rest/agile/latest/board/{}'.format(board_id)
        return self._perform_request(request, _parse_json_to_board)

    # GET /rest/agile/latest/board/{boardId}/project
    def get_projects_for_board(self, board_id):
        request = HTTPRequest()
        request.method = 'GET'
        request.path = '/rest/agile/latest/board/{}/project'.format(board_id)
        return self._perform_request(request, _parse_json_to_class, Project, ['id', 'name', 'key', 'projectTypeKey'])

    # GET /rest/agile/latest/board/{boardId}/epic
    def get_epics(self, board_id, start_at=0, max_results=50):
        request = HTTPRequest()
        request.method = 'GET'
        request.path = '/rest/agile/latest/board/{}/epic'.format(board_id)
        request.query = 'startAt={}&maxResults={}'.format(start_at, max_results)
        return self._perform_request(request, _parse_json_to_class, Epic, ['id', 'name', 'key', 'summary', 'done'])

    # GET /rest/agile/latest/epic/{epicIdOrKey}
    def get_epic(self, epic_id_or_key):
        request = HTTPRequest()
        request.method = 'GET'
        request.path = '/rest/agile/latest/epic/{}'.format(epic_id_or_key)
        return self._perform_request(request, _parse_json_to_epic)

    # GET /rest/agile/latest/board/{boardId}/backlog
    def get_issues_for_board(self, board_id, start_at=0, max_results=50):
        request = HTTPRequest()
        request.method = 'GET'
        request.path = '/rest/agile/latest/board/{}/backlog'.format(board_id)
        request.query = 'startAt={}&maxResults={}'.format(start_at, max_results)
        return self._perform_request(request, _parse_json_to_issues)

    # GET /rest/agile/latest/board/{boardId}/sprint
    def get_sprints_for_board(self, board_id):
        request = HTTPRequest()
        request.method = 'GET'
        request.path = '/rest/agile/latest/board/{}/sprint'.format(board_id)
        return self._perform_request(request, _parse_json_to_class, Sprint, ['id', 'state', 'name', 'startDate', 'endDate', 'completeDate', 'goal'])

    def get_active_sprint(self, board_id):
        sprints = self.get_sprints_for_board(board_id)
        for sprint in sprints:
            if sprint.state == 'active':
                return sprint
        return None

    # GET /rest/agile/latest/board/{boardId}/sprint/{sprintId}/issue
    def get_issues_for_sprint(self, board_id, sprint_id, start_at=0, max_results=50):
        request = HTTPRequest()
        request.method = 'GET'
        request.path = '/rest/agile/latest/board/{}/sprint/{}/issue'.format(board_id, sprint_id)
        request.query = 'startAt={}&maxResults={}'.format(start_at, max_results)        
        return self._perform_request(request, _parse_json_to_issues)

    # GET /rest/api/2/search?jql={jql}
    def search_issues(self, jql, start_at=0, max_results=50):
        request = HTTPRequest()
        request.method = 'GET'
        request.path = '/rest/api/2/search'
        request.query = 'jql={}&startAt={}&maxResults={}'.format(jql, start_at, max_results)        
        return self._perform_request(request, _parse_json_to_issues)

    # GET /rest/api/2/issue/{id_or_key}
    def get_issue(self, id_or_key):
        request = HTTPRequest()
        request.method = 'GET'
        request.path = '/rest/api/2/issue/{}'.format(id_or_key)        
        return self._perform_request(request, _parse_json_to_issue)

    def _perform_request(self, request, parser=None, result_class=None, attrs=[]):
        request.host = self.host
        request.headers = {
            'cache-control': 'no-cache, must-revalidate',
            'accept': 'application/json'
        }

        if self.username and self.password:
            request.headers['authorization'] = _get_auth_header(self.username, self.password)

        response = self._http_client.perform_request(request)
        result = json.loads(response.body.decode('UTF-8'))

        if parser:
            if result_class:
                return parser(result, result_class, attrs)
            else:
                return parser(result)
        else:
            return result