"""
This module contains functions to export data to CSV files
"""

from me.utils import io
from me.metadata.html import HTML
from me.metadata.pdf import PDF


def csv(filename, obj):
    """
    Exports data of an objet to CSV
    """
    if type(obj) is HTML:
        data = _html(obj)
    elif type(obj) is PDF:
        data = _pdf(obj)

    filename = filename.split('.')
    filename[1] = '.csv'
    filename = filename[0] + filename[1]

    io.write(filename, data)


def _pdf(obj):
    meta = ''
    header = ''

    md = obj.metadata

    blacklist = {
        'pdf:unmappedUnicodeCharsPerPage': True,
        'pdf:hasXFA': True,
        'pdf:charsPerPage': True,
        'X-Parsed-By': True,
        'X-TIKA:content_handler': True,
        'X-TIKA:embedded_depth': True,
        'xmpTPg': True
    }

    for key, value in md.items():
        if len(value) > 0:
            # Only add items that are not inside the blacklist dict
            try:
                blacklist[key]
            except KeyError:
                header = header + key + ";"
                meta = meta + str(value) + ";"

    data = header + '\n' + meta
    return data


def _html(obj):
    meta = ''
    header = ''

    md = obj.metadata
    
    for key, value in md.items():
        if len(value) > 0:
            header = header + key + ";"
            meta = meta + str(value) + ";"

    data = header + '\n' + meta
    return data