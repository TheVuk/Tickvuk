import logging

from logging import FileHandler
from logging import Formatter

import os
from configparser import ConfigParser
import sys
sys.path.append(os.getcwd())
import Tickvuk.__init__

parser = ConfigParser()
parser.read(Tickvuk.__init__.CONFIG_PATH)

LOG_FORMAT = (
            "%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d")
LOG_LEVEL = logging.INFO

if not os.path.exists(parser.get('common', 'log_path')):
        os.makedirs(parser.get('common', 'log_path'))

# main logger
MAIM_LOG_FILE = parser.get('common', 'log_path')+"/main.log"


main_logger = logging.getLogger("tickvuk.main")
main_logger.setLevel(LOG_LEVEL)
main_logger_file_handler = FileHandler(MAIM_LOG_FILE)
main_logger_file_handler.setLevel(LOG_LEVEL)
main_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
main_logger.addHandler(main_logger_file_handler)

# wapm logger
WAPM_LOG_FILE = parser.get('common', 'log_path')+"/wapm.log"
wapm_logger = logging.getLogger("tickvuk.wapm")

wapm_logger.setLevel(LOG_LEVEL)
wapm_file_handler = FileHandler(WAPM_LOG_FILE)
wapm_file_handler.setLevel(LOG_LEVEL)
wapm_file_handler.setFormatter(Formatter(LOG_FORMAT))
wapm_logger.addHandler(wapm_file_handler)