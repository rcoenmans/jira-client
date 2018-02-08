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

import unittest

from jiraclient.jiraclient import JiraClient

class JiraClientTest(unittest.TestCase):
    def setUp(self):
        file = open('./tests/jira_settings.txt', 'r')
        self.host = file.readline().rstrip()
        self.username = file.readline().rstrip()
        self.password = file.readline().rstrip()
        file.close()

    def test_get_boards(self):
        client = JiraClient(self.host, self.username, self.password)
        boards = client.get_boards()
        self.assertIsNotNone(boards)
        self.assertGreater(len(boards), 0)
    
    def test_get_projects_for_board(self):
        client = JiraClient(self.host, self.username, self.password)
        
        boards = client.get_boards()
        self.assertIsNotNone(boards)
        self.assertGreater(len(boards), 0)

        projects = client.get_projects_for_board(boards[0].id)
        self.assertIsNotNone(projects)
        self.assertGreater(len(projects), 0)

    def test_get_issues_for_board(self):
        client = JiraClient(self.host, self.username, self.password)
        board_id = 14
        issues = client.get_issues_for_board(board_id)

        self.assertIsNotNone(issues)
        self.assertGreater(len(issues), 0)

    def test_get_sprints_for_board(self):
        client = JiraClient(self.host, self.username, self.password)
        
        board_id = 14
        sprints = client.get_sprints_for_board(board_id)

        self.assertIsNotNone(sprints)        

    def test_get_active_sprint(self):
        client = JiraClient(self.host, self.username, self.password)

        board_id = 14
        sprint = client.get_active_sprint(board_id)

        self.assertIsNotNone(sprint)

    def test_get_issues_for_active_sprint(self):
        client = JiraClient(self.host, self.username, self.password)
        
        board_id = 14
        sprint = client.get_active_sprint(board_id)
        issues = client.get_issues_for_sprint(board_id, sprint.id)

        self.assertIsNotNone(issues)
        self.assertGreater(len(issues), 0)

    def test_search_issues(self):
        client = JiraClient(self.host, self.username, self.password)
        issues = client.search_issues(
            'project = KAUR AND status != Closed AND issuetype in (Story, Task, Bug) ORDER BY Rank ASC')

        self.assertIsNotNone(issues)
        self.assertGreater(len(issues), 0)

    def test_get_issue(self):
        client = JiraClient(self.host, self.username, self.password)
        issue  = client.get_issue('KAUR-1931')

        self.assertIsNotNone(issue)