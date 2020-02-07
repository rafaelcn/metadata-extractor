"""
This module has IO utilities functions
"""

import os


def write(filename, data):
    f = open(filename, 'w+')
    f.write(data)


def read(filename):
    """
    """

    data = ''

    with open(os.path.abspath(filename)) as f:
        for line in f:
            data += line

    return data
