#!/usr/bin/python3
#
#
# Rafael Campos Nunes <rafaelnunes@engineer.com>
#
#

import os
import sys
import argparse

# metadata extractor library
from me import settings
from me.extractor import extract


def create_parser():
    parser = argparse.ArgumentParser(description="""
        Metadata extractor extracts meta tags from documents. Currently there
        are only two formats implemented, the PDF and the HTML.""")

    parser.add_argument('-d',
                        '--dir',
                        help='Directory from where the software will use to read files',
                        default='')

    parser.add_argument('-o',
                        '--output',
                        help='After processing, sends all files to this directory')

    parser.add_argument('-p',
                        '--parser',
                        help="""Specify a./cl parse to act upon the files. If no 
                        parse is set it will use all available parsers""",
                        nargs='?',
                        default="all")

    parser.add_argument('-lp',
                        '--list-parsers',
                        help='List all available parsers',
                        action='store_true')

    parser.add_argument('--debug',
                        help="""Enable debug messsages""",
                        action='store_true')

    return parser


def main():
    parser = create_parser()

    if len(sys.argv) < 2:
        parser.parse_args(['-h'])
    else:
        args = parser.parse_args()

        if args.list_parsers:
            for p in settings.PARSERS:
                print(p.__name__)

            sys.exit()

        # If no directory is provided, show usage and exit
        if args.dir is None:
            parser.parse_args(['-h'])
        else:
            folder = os.path.abspath(args.dir)

    if args.parser == "all":
        for p in settings.PARSERS:
            p(args.dir)
    elif args.parser == "pdf":
        extract.pdf(folder, args.output)
    elif args.parser == "html":
        extract.html(folder, args.output)


if __name__ == "__main__":
    main()
