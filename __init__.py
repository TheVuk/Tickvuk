import logging

from logging import FileHandler
from logging import Formatter
import os
import sys
sys.path.append(os.getcwd())

CONFIG_PATH="Tickvuk/src/config/tickvuk.ini"

from configparser import ConfigParser
parser = ConfigParser()
parser.read(CONFIG_PATH)