#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module Docstring
"""

__author__ = "Richard Sugg"
__version__ = "v0.0.0"
__license__ = "SAS"

import logging
import argparse
from io import StringIO
import re
import sys
import os

from datetime import datetime

def parse_ssh_config(config=os.getenv("HOME") + "/.ssh/config"):
    entries = []
    with open(config, 'r') as fh:
        entry = None
        for line in fh:

            if re.search("^\s+$", line) or re.search("^\s*#", line):
                continue

            m = re.match("^\s*Host\s+(.+)$", line)
            if m:
                if entry:
                    entries.append(entry)
                entry = SshConfigEntry(host=m.group(1).strip(), options=dict())
                continue

            m = re.match("^\s*(.+?)\s+(.+)$", line)
            if m:
                entry.add_option(m.group(1), m.group(2).strip())
                continue

            m = re.match("^\s*(.+?)\s*=\s*(.+)$", line)
            if m:
                entry.add_option(m.group(1), m.group(2).strip())
                continue
        if entry:
            entries.append(entry)
    return entries


class SshConfigEntry(object):

    def __init__(self, host, options=dict()):
        self.host = host
        self.options = options

    def __str__(self):
        out = StringIO()
        out.write("Host {}\n".format(self.host))
        for k, v in self.options.items():
            out.write("    {} {}\n".format(k, v))
        out.write("\n")
        s = out.getvalue()
        out.close()
        return s

    def __eq__(self, other):
        if self.host != other.host:
            return False
        return self.options == other.options

    def add_option(self, name, value):
        self.options[name] = value


def parseargs():
    """Parser command line arguments"""
    parser = argparse.ArgumentParser(description="program description")
    parser.add_argument("-o", "--option", help="add option")
    parser.add_argument("-b", "--boolean", action="store_true", help="boolean option")
    parser.add_argument("-f", "--logfilename", help="logfile name", default=None)
    parser.add_argument("-n", "--nolog", action="store_true", help="turn off logging", default=False)
    return parser.parse_args()


def init_logging(filename=None):
    """Initialize logging"""
    handlers = [logging.StreamHandler()]
    if filename:
        handlers.append(logging.FileHandler(filename=filename))
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(module)s %(funcName)s,%(lineno)s %(name)s %(message)s',
        handlers=handlers
    )


def main():
    args = parseargs()
    starttime = datetime.now()
    print("{}".format(args))
    if not args.nolog:
        init_logging(args.logfilename)
    l = logging.getLogger(__name__)
    l.info("### starting")

    duration = datetime.now() - starttime
    l.info("### finished in {}s".format(duration))
    return 0


if __name__ == "__main__":
    sys.exit(main())


