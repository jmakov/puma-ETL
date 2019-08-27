import logging
import os


logger = logging.getLogger(__name__)
NETWORK_RECORDER_POSTROTATE_SCRIPT_NAME = "network_recorder_postrotate.sh"


def is_dev_environemnt():
    returned_env_var = os.getenv("PUMA_DEV_ENV")
    logger.info(returned_env_var)
    return False if returned_env_var is None else True


def get_scripts_path():
    return "scripts" if is_dev_environemnt() else "/opt/puma/puma-ETL/bin"


def get_network_recorder_postrotate_script_path():
    return get_scripts_path() + os.sep + NETWORK_RECORDER_POSTROTATE_SCRIPT_NAME


def get_network_recorder_command_path():
    return "/opt/gulp/bin/gulp"


def get_puma_recorder_executable_path():
    return "/opt/puma/puma-recorder/bin/puma-recorder"


def get_recorder_log_path():
    return "/var/log/puma/puma-recorder"


def get_etl_log_path():
    return "/var/log/puma/puma-ETL"
