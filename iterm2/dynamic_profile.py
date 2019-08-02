import os
import shutil
from datetime import datetime
import json
import logging
import sys

default_location = os.getenv("HOME") + "/Library/Application Support/iTerm2/DynamicProfiles/profiles.json"
default_logdir = os.getenv("HOME") + "/logs/iterm"

class DynamicProfile(object):

    @classmethod
    def generate(cls, entries, logdirectory=default_logdir):
        if not os.path.exists(logdirectory):
            os.makedirs(logdirectory)
        profiles = []
        for e in entries:
            if "*" in e.host:
                continue
            profile = {
                "Name": e.host,
                "Guid": e.host,
                "Shortcut": "",
                "Log Directory": logdirectory,
                "Custom Command": "Yes",
                "Command": "ssh " + e.host
            }
            profiles.append(profile)
        return dict(Profiles=profiles)

    @classmethod
    def update(cls, profiles, location=default_location):
        logger = logging.getLogger(__name__)
        if profiles is None:
            logger.error("profiles is null!")
            sys.exit(1)
        if os.path.exists(location):
            backupcopy = location + "." + datetime.now().strftime("%Y-%m-%d_%H%M%S")
            logger.info("backing up {} to {}".format(location, backupcopy))
            shutil.copyfile(location, backupcopy)
        logger.info("writing out {}".format(location))
        with open(location, 'w') as fh:
            fh.write(json.dumps(profiles, indent=2))
            os.remove(backupcopy)
