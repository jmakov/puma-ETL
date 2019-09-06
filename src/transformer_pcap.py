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
import os
import time

from tools import constants
from tools import log
from tools import path
from tools import tshutil
from tools import tsubprocess

THIS_SCRIPT_NAME = os.path.basename(__file__)
SLEEP = 60
logger = logging.getLogger()


def extract_incomming_msgs_for_account(compressed_pcap_fp, feed_name, sender_comp_id):
    tmp_fn = compressed_pcap_fp + "." + constants.FileExtension.TMP

    # construct resulting file name of the form puma-recorder_[feed name]_[acc ID]_[timestamp].pcap.zst
    timestamp = path.get_extractor_pcap_timestamp_from_fp(compressed_pcap_fp)
    res_fp = path.get_transformer_pcap_resulting_fp(feed_name, sender_comp_id, timestamp)

    # With some patterns we might get no results. Since we don't want to produce files with 0 size, we check first
    # if we have any matches.
    pattern = f"'56={sender_comp_id}'"
    check_match_command = f"zstdgrep -m 1 {pattern} {compressed_pcap_fp}"

    if tsubprocess.match_found(check_match_command):
        command = f"zstdcat {compressed_pcap_fp} | " \
                      f"ngrep -I - -O {tmp_fn} -q {pattern} > /dev/null && " \
                      f"zstd -T1 --rm -q -1 {tmp_fn} -o {res_fp}"
        tsubprocess.run_blocking_command(command)
        tshutil.rename_transformer_done(res_fp)


if __name__ == "__main__":
    log.configure_logger(logger, THIS_SCRIPT_NAME)
    secrets_fp = path.get_secrets_path()
    extractor_pcap_staging_path = path.get_extractor_pcap_staging_path()
    transformer_pcap_staging_path = path.get_transformer_pcap_staging_path()
    feed_name_account_data_map = tshutil.get_fix_feed_name_sendercompid_map(secrets_fp)
    pcap_fp_pattern_to_move = extractor_pcap_staging_path + os.sep + "*." \
        + constants.FileExtension.EXTRACTOR_PCAP_DONE

    tshutil.create_dir(transformer_pcap_staging_path)

    while True:
        files_to_transform = tshutil.find_files(pcap_fp_pattern_to_move)
        logger.info(f"Found files to transform: f{files_to_transform}")

        for fp in files_to_transform:
            logger.info(f"Processing: {fp}")
            tshutil.move(fp, transformer_pcap_staging_path)

            fn = fp.split(os.sep)[-1]
            moved_fp = transformer_pcap_staging_path + os.sep + fn
            pretty_fp = path.remove_fp_extension(moved_fp, constants.FileExtension.EXTRACTOR_PCAP_DONE)
            compressed_fp = pretty_fp + "." + constants.FileExtension.ZST_COMPRESSED

            command = f"zstd --rm -T1 -q -1 {moved_fp} -o {compressed_fp}"
            tsubprocess.run_blocking_command(command)

            for feed_name, sender_comp_id in feed_name_account_data_map:
                extract_incomming_msgs_for_account(compressed_fp, feed_name, sender_comp_id)

            tshutil.rename_transformer_done(compressed_fp)
        time.sleep(SLEEP)
