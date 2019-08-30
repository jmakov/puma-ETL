import logging
import os
import subprocess
import shlex
import sys
import time

import yaml

from tools import log
from tools import path

THIS_SCRIPT_NAME = os.path.basename(__file__)
logger = logging.getLogger()


if __name__ == "__main__":
    log.configure_logger(logger, THIS_SCRIPT_NAME)

    if len(sys.argv) != 6:
        secrets_path = sys.argv[3]
        pcap_staging_path = sys.argv[4]
        fix_msgs_staging_path = sys.argv[5]
    else:
        msg = "aUsage: extractor.py [interface name] " \
              "[pcap size (in GiB)] " \
              "[abs path to secrets.yaml] " \
              "[abs path to network staging path] " \
              "[abs path to MsgStorage staging path]"
        print(msg, file=sys.stderr)
        logger.exception("Arg error. Got: " + sys.argv + ", expected: " + msg)
        sys.exit()