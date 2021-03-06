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
    
    def test_get_board(self):
        client = JiraClient(self.host, self.username, self.password)
        boards = client.get_boards()
        board  = client.get_board(boards[0].id)
        self.assertIsNotNone(board)

    def test_get_epics(self):
        client = JiraClient(self.host, self.username, self.password)
        boards = client.get_boards()
        epics  = client.get_epics(boards[2].id)
        self.assertIsNotNone(epics)
        self.assertGreater(len(epics), 0)

    def test_get_epic(self):
        client = JiraClient(self.host, self.username, self.password)
        epic   = client.get_epic(27275)
        self.assertIsNotNone(epic)

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

    def test_get_sprint(self):
        client = JiraClient(self.host, self.username, self.password)

        sprint_id = 14
        sprint = client.get_sprint(sprint_id)

        self.assertIsNotNone(sprint)

    def test_get_issues_for_active_sprint(self):
        client = JiraClient(self.host, self.username, self.password)
        
        board_id = 14
        sprint = client.get_active_sprint(board_id)
        issues = client.get_issues_for_sprint(board_id, sprint.id)

        self.assertIsNotNone(issues)
        self.assertGreater(len(issues), 0)

    def test_download_attachment(self):
        client = JiraClient(self.host, self.username, self.password)
        issue = client.get_issue(22618)

        if len(issue.attachments) > 0:
            for attachment in issue.attachments:
                with open('./tests/tmp/{}'.format(attachment.filename), 'wb') as f:
                    f.write(client.download_attachment(attachment.id, attachment.filename))

    def test_search(self):
        client = JiraClient(self.host, self.username, self.password)
        issues = client.search(
            'project = Contoso AND status != Closed AND issuetype in (Story, Task, Bug) ORDER BY Rank ASC')

        self.assertIsNotNone(issues)
        self.assertGreater(len(issues), 0)

    def test_get_issue(self):
        client = JiraClient(self.host, self.username, self.password)
        issue  = client.get_issue(30284)
        self.assertIsNotNone(issue)

if __name__ == '__main__':
    unittest.main()