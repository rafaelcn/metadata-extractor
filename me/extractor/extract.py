"""
Contains basic functions to list and set up a parser to each file format
"""

import os

# metadata extractor library

from me import settings
from me.utils import export
from me.metadata.pdf import PDF
from me.metadata.html import HTML


def pdf(folder, output):
    """
    """
    filenames = __list(folder)

    for filename in filenames:
        if filename.split('.')[1] == 'pdf':
            p = PDF(os.path.join(folder, filename))

            if settings.DEBUG:
                print(p)
                print("\n\n")

            export.csv(os.path.join(output, (filename + '.csv')), p)


def html(folder, output):
    filenames = __list(folder)

    for filename in filenames:
        if filename.split('.')[1] == 'html':
            h = HTML(os.path.join(folder, filename))
            print(h)

            export.csv(os.path.join(output, (filename + '.csv')), h)


def __list(folder):
    """
    """
    (_, _, filenames) = next(os.walk(folder))
    return filenames
