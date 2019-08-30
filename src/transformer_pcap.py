"""
Makes operations on pcap files recorded by `extractor.py`:
* extract all traffic with an exchange
* prepare both files for further processing done by loader_*.py scripts

TODO (currently not possible because of ngrep limitation - FIX protocol not supported):
* extract ticks for every exchange
* extract quotes for every exchange

We do this in a couple of steps:
* We move the pcap files from `pcap_staging_path` to `fix_msgs_staging_path`/transformer_pcap (args of `extractor.py`).
The first staging area can be e.g. /tmp (RAM) which is of course limited so we want to move the data from there to a
place with less space restriction e.g. `fix_msgs_staging_path` which has to be a disk because of huge file sizes of
recorded FIX msgs there.
* Extract packets with `ngrep`
"""
import logging
import glob
import os
import shutil
import sys
import shlex
import subprocess
import time

import yaml

from tools import log

THIS_SCRIPT_NAME = os.path.basename(__file__)
SLEEP = 10
logger = logging.getLogger()


def get_acc_identification_data(secrets_fp):
    account_data = []

    with open(secrets_fp) as f:
        content = yaml.load(f, Loader=yaml.FullLoader)

        for feed in content["exchange_feeds"]:
            account_data.append(feed["sender_comp_ID"])

    return account_data


def move_files_to_transformer_pcap_staging_area(files_to_find, new_staging_path):
    files_for_transfer = glob.glob(files_to_find)
    logging.info("Found: " + files_for_transfer)

    for file in files_for_transfer:
        logging.info("Moving file: ") + file
        shutil.move(file, new_staging_path)


def extract_incomming_msgs_for_account(input_pcap_path, acc_no):
    tmp_fn = acc_no + ".pcap"
    res_fn = acc_no + ".pcap.zst"
    command_str = f"zstdcat {input_pcap_path} | " \
                  f"ngrep -I - -O {tmp_fn} -q '56={acc_no}' > /dev/null && " \
                  f"zstd --rm -q -1 {tmp_fn} -o {res_fn}"
    args = shlex.split(command_str)   # determines correct args tokenization

    logger.info(f"Running: {args}")
    subprocess.call(args)

    fin_fn = res_fn + ".transformer_done"
    os.rename(res_fn, fin_fn)


if __name__ == "__main__":
    log.configure_logger(logger, THIS_SCRIPT_NAME)

    if len(sys.argv) != 4:
        secrets_fp = sys.argv[1]
        pcap_staging_fp = sys.argv[2]
        transformer_pcap_staging_path = sys.argv[3]
    else:
        msg = "aUsage: extractor.py [interface name] " \
              "[pcap size (in GiB)] " \
              "[abs path to secrets.yaml] " \
              "[abs path to network staging path] " \
              "[abs path to MsgStorage staging path]"
        print(msg, file=sys.stderr)
        logger.exception("Arg error. Got: " + sys.argv + ", expected: " + msg)
        sys.exit()

    pcap_files_to_find = pcap_staging_fp + os.sep + "*.zst"
    account_data = get_acc_identification_data(secrets_fp)

    while True:
        move_files_to_transformer_pcap_staging_area(pcap_files_to_find, transformer_pcap_staging_path)
        files_for_extraction = glob.glob(transformer_pcap_staging_path)

        for file in files_for_extraction:
            for acc_no in account_data:
                extract_incomming_msgs_for_account(file, acc_no)

        time.sleep(SLEEP)
