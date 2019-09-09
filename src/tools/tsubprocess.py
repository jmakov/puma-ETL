import logging
import shlex
import subprocess

logger = logging.getLogger(__name__)


def run_blocking_command(command):
    args = shlex.split(command)  # determines correct args tokenization
    logger.info(f"Running: {args}")
    subprocess.call(args)


def run_command_with_pipes(command):
    logger.info(f"Running: {command}")
    subprocess.check_output(command, shell=True)


def match_found(check_match_command):
    try:
        args = shlex.split(check_match_command)  # determines correct args tokenization
        subprocess.check_output(args)
        return True
    except subprocess.CalledProcessError as e:
        logging.info(f"Nothing found for: {check_match_command}: e")
        return False
