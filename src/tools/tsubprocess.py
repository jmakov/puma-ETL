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
        args = shlex.split(check_match_command)  # determines correct args tokenization
        subprocess.check_output(args)
        return True
    except subprocess.CalledProcessError as e:
        logging.info(f"Nothing found for: {check_match_command}: e")
        return False


def run_command_with_pipes(command1, command2):
    logger.info(f"Processing: {command1} ' | ' {command2}")

    args1 = shlex.split(command1)
    p1 = subprocess.Popen(args1, stdout=subprocess.PIPE)

    args2 = shlex.split(command2)
    subprocess.Popen(args2, stdin=p1.stdout, stdout=subprocess.PIPE)

    p1.stdout.close()
