import os
import logging
import logging.handlers
import argparse

from utils.helper import is_user_root
from utils.staticvalues import PROGRAM_NAME
from mainwindow import MainWindow

LOG_FORMAT = "%(levelname)7s:%(asctime)s - %(filename)25s:%(lineno)4s - %(name)25s %(funcName)25s() - %(message)s"
LOG_DATEFORMATE = "%d/%m/%Y %H:%M:%S %p"
LOG_FILEPATH = os.path.join("/var", "log", PROGRAM_NAME, "wmi-ui.log")
#LOG_FILEPATH = os.path.join("/tmp", "wmi-log", PROGRAM_NAME, "wmi-ui.log")

def main():
    create_program_directories()

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", default=False)
    args = parser.parse_args()

    configure_logger(args.debug)

    logger = logging.getLogger(PROGRAM_NAME)
    logger.info("debugmode: '%s'", args.debug)

    MainWindow().start(args.debug)

def configure_logger(debugmode):
    logger = logging.getLogger(PROGRAM_NAME)

    if debugmode:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    formatter = logging.Formatter(LOG_FORMAT, LOG_DATEFORMATE)

    handler = logging.handlers.RotatingFileHandler(LOG_FILEPATH, backupCount=10)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.handlers[0].doRollover()

    logger.info("finish configure logger")

def create_program_directories():
    log_directory = os.path.dirname(LOG_FILEPATH)

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

if __name__ == "__main__":
    if is_user_root() is False:
        print("program not started as root")
        print("Abort the programstart, only root can run this program")
    else:
        main()
