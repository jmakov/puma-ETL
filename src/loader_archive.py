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
            archival_path = sys.argv[1]
            loader_archive_staging_path = path.get_loader_archiver_staging_path()
            loader_backup_staging_path = path.get_loader_backup_staging_path()
        elif len(sys.argv) == 4:
            archival_path = sys.argv[1]
            loader_archive_staging_path = sys.argv[2]
            loader_backup_staging_path = sys.argv[3]
        else:
            raise RuntimeError("Usage: loader_archiver.py [archival abs path] "
                               "([loader_archive_staging_path]) "
                               "([loader_backup_staging_path])")

        feeds_config_fp = path.get_path_feeds_config()
        feed_name_account_data_map = tshutil.get_fix_feed_name_sendercompid_map(feeds_config_fp)
        tshutil.create_dir(loader_archive_staging_path)

        fp_from_loader_backup_staging_path = loader_backup_staging_path + os.sep + "*." \
            + constants.FileExtension.LOADER_BACKUP_DONE.value

        while True:
            files_to_move = tshutil.find_files(fp_from_loader_backup_staging_path)

            for fp in files_to_move:
                tshutil.move(fp, loader_archive_staging_path)

                fn = fp.split(os.sep)[-1]
                moved_fp = loader_archive_staging_path + os.sep + fn

                # prettify file naming
                pretty_fp = path.remove_fp_extension(moved_fp, constants.FileExtension.LOADER_BACKUP_DONE.value)
                os.rename(moved_fp, pretty_fp)

                # extract info from fn so we can save files to backup_path/[feed_name]/[year]-[month]
                feed_name, timestamp = path.parse_transformer_result_fp(pretty_fp, feed_name_account_data_map)

                year_month_dir_path = tshutil.create_loader_dirs(archival_path, feed_name, timestamp)
                tshutil.move(pretty_fp, year_month_dir_path)
            time.sleep(SLEEP)
    except Exception as e:
        print(e, file=sys.stderr)
        logger.exception(e)
