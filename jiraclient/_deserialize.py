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
    Sprint
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
    
def _parse_json_to_issues(response, result_class, attrs):
    issues = []
    for issue in response['issues']:
        issues.append(_map_attrs_values(Issue, ['id', 'key', 'fields'], issue))
    return issues

def _parse_json_to_sprints(response):
    sprints = []
    for value in response['values']:
        sprints.append(_parse_json_to_sprint(value))
    return sprints

def _parse_json_to_sprint(response):
    attrs = ['id', 'state', 'name', 'startDate', 'endDate', 'completeDate', 'goal']
    return _map_attrs_values(Sprint, attrs, response)

