"""
"""

import os.path

from lxml import html

# self packages
from me.utils import io


class HTML:
    def __init__(self, uri):
        """
        """
        self.metadata = {}

        if 'http' in uri or 'https' in uri:
            # It is an URL
            pass
        else:
            # It is a file
            data = io.read(os.path.abspath(uri))
            tree = html.fromstring(data)

            title = self.__get_element(tree, '//title/text()')
            self.metadata['page_title'] = title.strip()

            # Get all metatags inside an HTML document
            meta_tags = self.__get_elements(tree, '//meta')
            i = 0

            for meta_tag in meta_tags:
                attributes = meta_tag.attrib
                self.metadata['<meta_' + str(i) + '>'] = attributes
                i = i + 1

    def __str__(self):
        return str(self.metadata)

    def __get_element(self, root, query):
        """
        """
        try:
            e = root.xpath(query)[0]
            return e
        except IndexError:
            return None

    def __get_elements(self, root, query):
        """
        """
        try:
            e = root.xpath(query)
            return e
        except IndexError:
            return None
