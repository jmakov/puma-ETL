import logging
import os
import sys

from tools import constants

logger = logging.getLogger(__name__)


def _get_staging_sub_path(dir_name):
    return get_staging_path() + os.sep + dir_name


def _get_env_var(env_var):
    var = os.getenv(env_var)

    if var is None or var is "":
        msg = f"Not defined: {env_var}"
        logger.exception(msg)
        raise RuntimeError(msg)
    return var


def is_dev_environemnt():
    returned_env_var = os.getenv(constants.Env.DEV_ENV.value)
    return False if returned_env_var is None else True


def get_scripts_path():
    return "scripts" if is_dev_environemnt() else "/opt/puma/puma-ETL/scripts"


def get_network_recorder_postrotate_script_path():
    return get_scripts_path() + os.sep + constants.NETWORK_RECORDER_POSTROTATE_SCRIPT_NAME


def get_network_recorder_command_path():
    return "/opt/gulp/bin/gulp"


def get_puma_recorder_executable_path():
    return "/opt/puma/puma-recorder/bin/puma-recorder"


def get_recorder_log_path():
    return "/var/log/puma/puma-recorder"


def get_etl_log_path():
    return "/var/log/puma/puma-ETL"


def get_secrets_path():
    return _get_env_var(constants.Env.SECRETS_PATH.value)


def get_staging_path():
    return _get_env_var(constants.Env.STAGING_PATH.value)


def get_extractor_pcap_staging_path():
    return _get_staging_sub_path(constants.DirName.EXTRACTOR_STAGING.value)


def get_extractor_staging_msgstorage_path():
    return get_extractor_pcap_staging_path() + os.sep + constants.DirName.MSGSTORAGE.value


def get_transformer_pcap_staging_path():
    return _get_staging_sub_path(constants.DirName.TRANSFORMER_PCAP_STAGING.value)


def get_transformer_msgstorage_staging_path():
    return _get_staging_sub_path(constants.DirName.TRANSFORMER_MSGSTORAGE_STAGING.value)


def get_loader_backup_staging_path():
    return _get_staging_sub_path(constants.DirName.LOADER_BACKUP.value)


def get_loader_archiver_staging_path():
    return _get_staging_sub_path(constants.DirName.LOADER_ARCHIVER.value)


def get_transformer_pcap_resulting_fp(staging_path, feed_name, sender_comp_id, ts):
    return staging_path \
           + os.sep \
           + constants.PCAP_BASE_NAME + constants.FN_FROM_TRANSFORMER_SPLIT \
           + feed_name + constants.FN_FROM_TRANSFORMER_SPLIT \
           + sender_comp_id + constants.FN_FROM_TRANSFORMER_SPLIT \
           + ts + "." \
           + constants.FileExtension.PCAP.value + "." \
           + constants.FileExtension.ZST_COMPRESSED.value


def parse_extractor_pcap_file(fn):
    # we have 2 cases: "pumarecorder_[timestamp].pcap.zst" (from extractor)and
    # "pumarecorder-[feed_name]-[sender.compID]-[timestamp].pcap.zst (from transformer)
    test_split = fn.split(constants.FN_FROM_EXTRACTOR_SPLIT)

    if len(test_split) == 2:
        # we got the first case - raw pcap file
        feed_name = constants.RAW_FILES_DIR_NAME
        _timestamp_rest = test_split[-1]
    else:
        fn_splitted = fn.split(constants.FN_FROM_TRANSFORMER_SPLIT)
        base_name, feed_name, sender_comp_id, _timestamp_rest = fn_splitted

    timestamp = _timestamp_rest.split(".")[0]
    return feed_name, timestamp


def parse_extractor_msgstorage_file(fn, feed_name_account_data_map):
    _feed_info, _, _fix_info_with_ts_and_extensions = fn.split("-")
    _fix_info_with_ts = _fix_info_with_ts_and_extensions.split(".")[0]
    _extended_timestamp = _fix_info_with_ts.split("_")[-1]
    timestamp = _extended_timestamp[:14]    # OnixS FIX lib names a file sometimes with different timestamp precision

    # sender_comp_id can be  "integer" or "feedID.integer". In MsgStorage this is serialized as
    # "integer-..." or "feedID_integer-..."
    _feed_info_split = _feed_info.split("_")

    if len(_feed_info_split) == 1:
        # sender_comp_id is of the form "integer"
        sender_comp_id = _feed_info_split[0]
    else:
        # sender_comp_id is of the form "feedID_integer"
        sender_comp_id = _feed_info_split[0] + "." + _feed_info_split[1]

    # identify feed name from sender_comp_id
    for k, v in feed_name_account_data_map.items():
        if sender_comp_id == v:
            feed_name = k
            break
    else:
        msg = f"Cannot identify feed name from sender_comp_id={sender_comp_id}"
        print(msg, file=sys.stderr)
        logger.exception(msg)
        raise RuntimeError(msg)

    return feed_name, timestamp


def parse_transformer_result_fp(fp_wo_extension, feed_name_account_data_map):
    fn = fp_wo_extension.split(os.sep)[-1]

    if constants.PCAP_BASE_NAME in fn:
        feed_name, timestamp = parse_extractor_pcap_file(fn)
    else:
        feed_name, timestamp = parse_extractor_msgstorage_file(fn, feed_name_account_data_map)

    return feed_name, timestamp


def remove_fp_extension(fp, extension):
    extension_length_including_point = len(extension) + 1
    return fp[:-extension_length_including_point]
