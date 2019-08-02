#!/usr/bin/env python3
import sys
import os
import logging

sys.path.append(os.getenv("HOME") + "/git-personal/sshconfig")
from sshconfig.sshconfig import parse_ssh_config
from iterm2.dynamic_profile import DynamicProfile

def setup_logging(level=logging.INFO):
    out_handler = logging.StreamHandler(sys.stdout)
    fmtstr = "%(asctime)s %(levelname)s [%(funcName)s:%(lineno)d] %(message)s"
    formatter = logging.Formatter(fmtstr)
    out_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(out_handler)
    logger.setLevel(level)


if os.getenv("DEBUG", 0) == "1":
    setup_logging(logging.DEBUG)

entries = parse_ssh_config()
profiles = DynamicProfile.generate(entries)
DynamicProfile.update(profiles)
