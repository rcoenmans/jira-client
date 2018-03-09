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

import sys
import os

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name='jira-client',
        version='0.0.5',
        description='Jira client',
        long_description=open('README.md', 'r').read(),
        license='MIT License',
        author='Robbie Coenmans',
        author_email='robbie.coenmans@outlook.com',
        url='https://github.com/rcoenmans/jira-client',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',

            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.0',
            'Programming Language :: Python :: 3.1',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3 :: Only',

            'License :: OSI Approved :: MIT License',
        ],
        zip_safe=False,
        packages=find_packages(),
        install_requires=['requests'] + (['futures'] if sys.version_info < (3, 0) else [])
    )