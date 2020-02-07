"""
This module abstracts a PDF document, containing the data and the metadada of
the respective PDF document.
"""

import os

from tika import parser


class PDF:
    """
    The PDF class abstracts a PDF document which parses its content and
    metadata.
    """

    def __init__(self, filename):
        raw = parser.from_file(filename)

        self.name = os.path.basename(filename)
        self.content = raw['content']
        self.metadata = raw['metadata']

    def __str__(self):
        return str(self.metadata)
