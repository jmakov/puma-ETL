"""
Starts recording markets and saves the recorded network traffic.
We do this by parsing the secrets.yaml file to get feed names (for starting the markets recorder) and network ports (so
tcpdump knows what network traffic to filter).
"""
import logging
import os
import subprocess
import shlex
import sys
import time

import yaml

from tools import constants
from tools import log
from tools import path
from tools import tshutil

THIS_SCRIPT_NAME = os.path.basename(__file__)
logger = logging.getLogger()


if __name__ == "__main__":
    try:
        log.configure_logger(logger, THIS_SCRIPT_NAME)

        if len(sys.argv) == 3:
            interface_name = sys.argv[1]
            pcap_file_size = sys.argv[2]
        else:
            msg = "Usage: extractor.py [interface name] [pcap size (in GiB)]"
            print(msg, file=sys.stderr)
            logger.exception(msg)
            sys.exit()

        feeds_config_fp = path.get_path_feeds_config()
        postrotate_script_path = path.get_network_recorder_postrotate_script_path()
        recorder_executable_path = path.get_puma_recorder_executable_path()
        extractor_staging_path = path.get_extractor_pcap_staging_path()
        msg_storage_path = path.get_extractor_staging_msgstorage_path()
        process_list = []
        quote_feed_names = []
        quote_feed_hosts = []

        tshutil.create_dir(msg_storage_path)

        # parse secrets yaml file to get feed names and hosts
        with open(feeds_config_fp) as f:
            content = yaml.load(f, Loader=yaml.FullLoader)

            for feed in content["exchange_feeds"]:
                quote_feed_names.append(feed["name"])
                quote_feed_hosts.append(feed["host"])

        # for tcpdump filter expression we don't want duplicate ports
        unique_hosts = [str(i) for i in set(quote_feed_hosts)]

        filter_expression = "host " + " or host ".join(unique_hosts)
        logger.info(f"filter expression: {filter_expression}")

        # Start network recording. We'll filter network traffic by destination host ports.
        # network_recording_command_flags = f'-t ' \
        #                                   f'-r 1024 ' \
        #                                   f'-C {pcap_file_size} ' \
        #                                   f'-n {constants.PCAP_BASE_NAME} ' \
        #                                   f'-o {extractor_staging_path} ' \
        #                                   f'-i {interface_name} ' \
        #                                   f'-Z {postrotate_script_path} ' \
        #                                   f'-f "{filter_expression}"'
        # network_recording_command = path.get_network_recorder_command_path() + " " + network_recording_command_flags
        # logger.info(f"Starting: {network_recording_command}")
        # args = shlex.split(network_recording_command)   # determines correct args tokenization
        # p = subprocess.Popen(args)
        # process_list.append(p)
        #
        # # wait for buffers of network_recording_command to init
        # time.sleep(5)

        # connect to exchanges and brokers
        for feed_name in quote_feed_names:
            logger.info(f"Starting: {feed_name}")

            # we have to set working dir (cwd) since Onyx FIX lib automatically creates MsgStorage directory and we want
            # to have it in the recorder log folder
            p = subprocess.Popen([recorder_executable_path, feed_name], cwd=extractor_staging_path)
            process_list.append(p)

        logger.info("All processes running")
    except Exception as e:
        print(e, file=sys.stderr)
        logger.exception(e)
