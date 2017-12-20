#!/usr/bin/env python

from sshconfig.sshconfig import parse_ssh_config
from iterm2.dynamic_profile import DynamicProfile

entries = parse_ssh_config()
profiles = DynamicProfile.generate(entries)
DynamicProfile.update(profiles)
