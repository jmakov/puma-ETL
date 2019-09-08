import logging
import os
import sys
import time

from tools import constants
from tools import log
from tools import path
from tools import tshutil

THIS_SCRIPT_NAME = os.path.basename(__file__)
SLEEP = 60
logger = logging.getLogger()

if __name__ == "__main__":
    try:
        log.configure_logger(logger, THIS_SCRIPT_NAME)

        if len(sys.argv) == 2:
            backup_path = sys.argv[1]
        else:
            msg = "Usage: loader.py [backup abs path]"
            print(msg, file=sys.stderr)
            logger.exception(msg)
            sys.exit()

        transformer_pcap_staging_path = path.get_transformer_pcap_staging_path()
        transformer_msgstorage_staging_path = path.get_transformer_msgstorage_staging_path()
        loader_backup_staging_path = path.get_loader_backup_staging_path()
        secrets_fp = path.get_secrets_path()
        feed_name_account_data_map = tshutil.get_fix_feed_name_sendercompid_map(secrets_fp)
        fp_from_transformer_pcap = transformer_pcap_staging_path + os.sep + "*." \
            + constants.FileExtension.TRANSFORMER_DONE.value
        fp_from_transformer_msgstorage = transformer_msgstorage_staging_path + os.sep + "*." \
            + constants.FileExtension.TRANSFORMER_DONE.value

        tshutil.create_dir(loader_backup_staging_path)

        files_to_move = tshutil.find_files(fp_from_transformer_pcap)
        files_to_move += tshutil.find_files(fp_from_transformer_msgstorage)

        while True:
            for fp in files_to_move:
                tshutil.move(fp, loader_backup_staging_path)

                fn = fp.split(os.sep)[-1]
                moved_fp = loader_backup_staging_path + os.sep + fn

                # prettify file naming
                pretty_fp = path.remove_fp_extension(moved_fp, constants.FileExtension.TRANSFORMER_DONE.value)
                os.rename(moved_fp, pretty_fp)

                # extract info from fn so we can save files to backup_path/[feed_name]/[year]-[month]
                feed_name, timestamp = path.parse_transformer_result_fp(pretty_fp, feed_name_account_data_map)

                year_month_dir_path = tshutil.create_loader_dirs(backup_path, feed_name, timestamp)
                tshutil.copy(pretty_fp, year_month_dir_path)
                tshutil.rename_loader_backup_done(pretty_fp)
            time.sleep(SLEEP)
    except Exception as e:
        print(e, file=sys.stderr)
        logger.exception(e)
