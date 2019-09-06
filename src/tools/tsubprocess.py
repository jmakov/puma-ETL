import logging
import shlex
import subprocess

logger = logging.getLogger(__name__)


def run_blocking_command(command):
    args = shlex.split(command)  # determines correct args tokenization

    logger.info(f"Running: {args}")
    subprocess.call(args)


def check_output(command):
    args = shlex.split(command)  # determines correct args tokenization

    logger.info(f"Running: {args}")
    return subprocess.check_output(args)


def match_found(check_match_command):
    try:
        subprocess.check_output(check_match_command)
        return True
    except subprocess.CalledProcessError as e:
        logging.info(f"Nothing found for: {check_match_command}: e")
        return False
