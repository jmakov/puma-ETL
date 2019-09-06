import glob
import logging
import os
import shutil
import time

import yaml

from tools import constants

logger = logging.getLogger(__name__)


def find_files(fn_template):
    found_files = glob.glob(fn_template)
    logging.info(f"For: {fn_template}, found: {found_files}")
    return found_files


def get_base_name(fp):
    return fp.split(os.sep)[-1]


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def rename_transformer_done(fp):
    fin_fn = fp + "." + constants.FileExtension.TRANSFORMER_DONE.value
    os.rename(fp, fin_fn)


def rename_loader_backup_done(fp):
    fin_fn = fp + "." + constants.FileExtension.TRANSFORMER_DONE.value
    os.rename(fp, fin_fn)


def get_fix_feed_name_sendercompid_map(secrets_fp):
    feed_name_account_data_map = {}

    with open(secrets_fp) as f:
        content = yaml.load(f, Loader=yaml.FullLoader)

        for feed in content["exchange_feeds"]:
            feed_name_account_data_map[feed["name"]] = feed["sended_comp_ID"]

    return feed_name_account_data_map


def move(fp_in, fp_out):
    logger.info(f"Moving: {fp_in} to {fp_out}")
    shutil.move(fp_in, fp_out)


def copy(fp_in, fp_out):
    logger.info(f"Copying: {fp_in} to {fp_out}")
    shutil.copy(fp_in, fp_out)


def create_loader_dirs(loader_target_dir_path, feed_name, timestamp):
    feed_name_dir_path = loader_target_dir_path + os.sep + feed_name
    create_dir(feed_name_dir_path)

    # parse timestamp
    parsed_timestamp = time.strptime(timestamp, "%Y%m%d%H%M%S")
    year_month_dir_path = feed_name_dir_path + os.sep + parsed_timestamp.tm_year + "-" + parsed_timestamp.tm_mon
    create_dir(year_month_dir_path)

    return year_month_dir_path
