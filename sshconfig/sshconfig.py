#!/usr/bin/env python
# -*- coding: utf-8 -*-

from io import StringIO
import re
import os

from datetime import datetime


def parse_ssh_config(config=os.getenv("HOME") + "/.ssh/config"):
    entries = []
    with open(config, "r") as fh:
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
