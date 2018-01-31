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

class Board(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.type = None
        self.location = None

    def __str__(self):
        return '{} {}'.format(self.id, self.name)

class Issue(object):
    def __init__(self):
        self.id = None
        self.key = None
        self.fields = {}

    def __str__(self):
        return '{} {}'.format(self.id, self.key)

class Sprint(object):
    def __init__(self):
        self.id = None
        self.state = None
        self.name = None
        self.startDate = None
        self.endDate = None
        self.completeDate = None
        self.goal = None

    def __str__(self):
        return '{} {} ({})'.format(self.id, self.name, self.state)

class Project(object):
    def __init__(self):
        self.id = None
        self.key = None
        self.name = None
        self.projectTypeKey = None