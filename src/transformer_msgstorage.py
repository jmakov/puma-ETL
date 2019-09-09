import logging
import os
import time
import sys

from tools import constants
from tools import log
from tools import path
from tools import tshutil
from tools import tsubprocess

THIS_SCRIPT_NAME = os.path.basename(__file__)
SLEEP = 60
logger = logging.getLogger()


def filter_msgs(fp_to_filter, original_fp, pattern, resulting_fp_extension):
    res_fp = original_fp + "." + resulting_fp_extension + "." + constants.FileExtension.ZST_COMPRESSED.value

    # With some patterns we might get no results. Since we don't want to produce files with 0 size, we check first
    # if we have any matches.
    check_match_command = f"zstdgrep -m 1 '{pattern} {fp_to_filter}"

    if tsubprocess.match_found(check_match_command):
        command = f"zstdgrep '{pattern}' {fp_to_filter} | zstd -q -T1 -1 -o {res_fp}"
        tsubprocess.run_command_with_pipes(command)
        tshutil.rename_transformer_done(res_fp)


def delete_extractor_msgstore_redundant_files(fp_pattern):
    logger.info("Deleting redundant files")

    files_to_delete = tshutil.find_files(fp_pattern)

    for fp in files_to_delete:
        os.remove(fp)


if __name__ == "__main__":
    try:
        log.configure_logger(logger, THIS_SCRIPT_NAME)
        secrets_fp = path.get_secrets_path()
        extractor_msgstorage_staging_path = path.get_extractor_staging_msgstorage_path()
        transformer_msgstorage_staging_path = path.get_transformer_msgstorage_staging_path()
        msgs_fp_pattern_to_move = extractor_msgstorage_staging_path + os.sep + "*." \
            + constants.FileExtension.EXTRACTOR_MSGSTORAGE_DONE.value
        files_to_delete_pattern = extractor_msgstorage_staging_path + os.sep + "*." \
            + constants.FileExtension.EXTRACTOR_MSGSTORAGE_REDUNDANT_FILES.value

        tshutil.create_dir(transformer_msgstorage_staging_path)

        while True:
            files_to_transform = tshutil.find_files(msgs_fp_pattern_to_move)
            logger.info(f"Found files to transform: f{files_to_transform}")

            for fp in files_to_transform:
                logger.info(f"Processing: {fp}")
                tshutil.move(fp, transformer_msgstorage_staging_path)

                fn = fp.split(os.sep)[-1]
                target_fp = transformer_msgstorage_staging_path + os.sep + fn
                pretty_fp = path.remove_fp_extension(target_fp, constants.FileExtension.EXTRACTOR_MSGSTORAGE_DONE.value)
                compressed_fp = pretty_fp + "." + constants.FileExtension.ZST_COMPRESSED.value

                command = f"zstd --rm -q -1 {target_fp} -o {compressed_fp}"
                tsubprocess.run_blocking_command(command)

                filter_msgs(compressed_fp, pretty_fp, constants.FIXMsgField.TICK, constants.FileExtension.TICKS.value)
                filter_msgs(compressed_fp, pretty_fp, constants.FIXMsgField.QUOTE, constants.FileExtension.QUOTES.value)
                filter_msgs(compressed_fp, pretty_fp, constants.FIXMsgField.FIN_INSTRUMENT_LIST.value,
                            constants.FileExtension.FIN_INSTRUMENTS_LIST.value)

                # mark compressed original as processed so we can include it in the next stage
                tshutil.rename_transformer_done(compressed_fp)

            delete_extractor_msgstore_redundant_files(files_to_delete_pattern)
            time.sleep(SLEEP)
    except Exception as e:
        print(e, file=sys.stderr)
        logger.exception(e)
