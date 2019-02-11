import sys, os, logging
sys.path.append(os.getcwd())
from Tickvuk.src.algos.wapm.wapm_objects import WapmObjects
from Tickvuk.src.loghandler.logger import wapm_logger


class WapmAlgo():
    def algo(self, ticktime, tickprice):
        WapmObjects.value = WapmObjects.value + 1
        wapm_logger.info("# - "+str(WapmObjects.value))