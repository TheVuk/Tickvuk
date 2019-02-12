import collections
import logging
import time
import os.path
import argparse
import datetime
import inspect ,traceback
from random import randint
import csv
import subprocess
import sys, getopt
from ibapi.utils import iswrapper
from ibapi.common import * 
from ibapi.contract import * 
from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper
from ibapi.scanner import ScanData
from configparser import ConfigParser

import sys
sys.path.append(os.getcwd())
import Tickvuk.__init__ as tickvuk
from Tickvuk.src.loghandler.logger import main_logger
from Tickvuk.src.algos.sapm import sapm_algo
from Tickvuk.src.algos.wapm import wapm_algo

#parser = tickvuk.parser
#parser.read(Tickvuk.__init__.CONFIG_PATH)

wapm_obj = wapm_algo.WapmAlgo()
sapm_obj = sapm_algo.SapmAlgo()

def clear():
    if os.name in ('nt','dos'):
        subprocess.call("cls")
    elif os.name in ('linux','osx','posix'):
        subprocess.call("clear")
    else:
        print("\n") * 120

def printWhenExecuting(fn):
    def fn2(self):
        print("   doing", fn.__name__)
        fn(self)
        print("   done w/", fn.__name__)
    return fn2


def printinstance(self,inst:Object):
    attrs = vars(inst)
    print(', '.join("%s: %s" % item for item in attrs.items()))


class Activity(Object):
    def __init__(self, reqMsgId, ansMsgId, ansEndMsgId, reqId):
        self.reqMsdId = reqMsgId
        self.ansMsgId = ansMsgId
        self.ansEndMsgId = ansEndMsgId
        self.reqId = reqId


class RequestMgr(Object):
    def __init__(self):
        self.requests = []

    def addReq(self, req):
        self.requests.append(req)

    def receivedMsg(self, msg):
        pass


# ! [socket_declare]
class VukClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)
        # ! [socket_declare]

        # how many times a method is called to see test coverage
        self.clntMeth2callCount = collections.defaultdict(int)
        self.clntMeth2reqIdIdx = collections.defaultdict(lambda: -1)
        self.reqId2nReq = collections.defaultdict(int)
        self.setupDetectReqId()

    def countReqId(self, methName, fn):
        def countReqId_(*args, **kwargs):
            self.clntMeth2callCount[methName] += 1
            idx = self.clntMeth2reqIdIdx[methName]
            if idx >= 0:
                sign = -1 if 'cancel' in methName else 1
                self.reqId2nReq[sign * args[idx]] += 1
            return fn(*args, **kwargs)

        return countReqId_

    def setupDetectReqId(self):

        methods = inspect.getmembers(EClient, inspect.isfunction)
        for (methName, meth) in methods:
            if methName != "send_msg":
                # don't screw up the nice automated logging in the send_msg()
                self.clntMeth2callCount[methName] = 0
                # logging.debug("meth %s", name)
                sig = inspect.signature(meth)
                for (idx, pnameNparam) in enumerate(sig.parameters.items()):
                    (paramName, param) = pnameNparam # @UnusedVariable
                    if paramName == "reqId":
                        self.clntMeth2reqIdIdx[methName] = idx

                setattr(VukClient, methName, self.countReqId(methName, meth))

                # print("TestClient.clntMeth2reqIdIdx", self.clntMeth2reqIdIdx)


# ! [ewrapperimpl]
class VukWrapper(wrapper.EWrapper):
    # ! [ewrapperimpl]
    def __init__(self):
        wrapper.EWrapper.__init__(self)

        self.wrapMeth2callCount = collections.defaultdict(int)
        self.wrapMeth2reqIdIdx = collections.defaultdict(lambda: -1)
        self.reqId2nAns = collections.defaultdict(int)
        self.setupDetectWrapperReqId()

    # TODO: see how to factor this out !!

    def countWrapReqId(self, methName, fn):
        def countWrapReqId_(*args, **kwargs):
            self.wrapMeth2callCount[methName] += 1
            idx = self.wrapMeth2reqIdIdx[methName]
            if idx >= 0:
                self.reqId2nAns[args[idx]] += 1
            return fn(*args, **kwargs)

        return countWrapReqId_

    def setupDetectWrapperReqId(self):

        methods = inspect.getmembers(wrapper.EWrapper, inspect.isfunction)
        for (methName, meth) in methods:
            self.wrapMeth2callCount[methName] = 0
            # logging.debug("meth %s", name)
            sig = inspect.signature(meth)
            for (idx, pnameNparam) in enumerate(sig.parameters.items()):
                (paramName, param) = pnameNparam # @UnusedVariable
                # we want to count the errors as 'error' not 'answer'
                if 'error' not in methName and paramName == "reqId":
                    self.wrapMeth2reqIdIdx[methName] = idx

            setattr(VukWrapper, methName, self.countWrapReqId(methName, meth))


class TickVuk(VukWrapper, VukClient):

    HDATE=""
    SYMBOL=""
    IP=""
    PORT=""
    SECTYPE=""
    STRIKE=""
    RIGHT=""
    EXPIRY=""
    algo=""
    contract = Contract()
    #objwapm = wapm()

    def __init__(self):
        VukWrapper.__init__(self)
        VukClient.__init__(self, wrapper=self)
        # ! [socket_init]
        self.nKeybInt = 0
        self.started = False
        self.nextValidOrderId = None
        self.permId2ord = {}
        self.reqId2nErr = collections.defaultdict(int)
        self.globalCancelOnly = False
        self.simplePlaceOid = None
        self.initVariables()
    
    def initVariables(self):
        try:
            self.HDATE=tickvuk.parser.get('common', 'date')
            self.SYMBOL=tickvuk.parser.get('common', 'symbol')
            self.IP=tickvuk.parser.get('common', 'gateway_ip')
            self.PORT=tickvuk.parser.get('common', 'gateway_port')
            self.SECTYPE=tickvuk.parser.get('common', 'sectype')
            self.STRIKE=tickvuk.parser.get('common', 'strike')
            self.RIGHT=tickvuk.parser.get('common', 'right')
            self.EXPIRY=tickvuk.parser.get('common', 'expiry')
            self.algo=tickvuk.parser.get('common', 'algo')
            main_logger.info("All common variable set sucessfully")
        except Exception:
            main_logger.error(traceback.format_exc())
        finally:
            main_logger.info("initVariable execution completed")
    
    def dumpTestCoverageSituation(self):
        for clntMeth in sorted(self.clntMeth2callCount.keys()):
            main_logger.debug("ClntMeth: %-30s %6d" % (clntMeth,
                                                   self.clntMeth2callCount[clntMeth]))

        for wrapMeth in sorted(self.wrapMeth2callCount.keys()):
            main_logger.debug("WrapMeth: %-30s %6d" % (wrapMeth,
                                                   self.wrapMeth2callCount[wrapMeth]))

    def dumpReqAnsErrSituation(self):
        main_logger.debug("%s\t%s\t%s\t%s" % ("ReqId", "#Req", "#Ans", "#Err"))
        for reqId in sorted(self.reqId2nReq.keys()):
            nReq = self.reqId2nReq.get(reqId, 0)
            nAns = self.reqId2nAns.get(reqId, 0)
            nErr = self.reqId2nErr.get(reqId, 0)
            main_logger.debug("%d\t%d\t%s\t%d" % (reqId, nReq, nAns, nErr))


    @iswrapper
    # ! [historicaltickslast]
    def historicalTicksLast(self, reqId: int, ticks: ListOfHistoricalTickLast,
                            done: bool):
        self.fulldaydata(ticks)
    # ! [historicaltickslast]

    def fulldaydata(self,ticks):
        try:
            with open(tickvuk.parser.get('common', 'hrhd_data_path')+os.sep+self.SYMBOL+"_"+self.SECTYPE+"_"+str(self.HDATE)+".csv", 'a', newline='') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                if (len(ticks) >=1000):
                    i = 0
                    for tick in ticks:
                        #print(str(time.strftime("%D %H:%M:%S", time.localtime(int(tick.time))))+","+str(tick.price)+","+str(tick.size))
                        filewriter.writerow([str(time.strftime("%D %H:%M:%S", time.localtime(int(tick.time)))), str(tick.price),str(tick.size)])
                        i=i+1
                        sapm_obj.algo(tick.time,tick.price)
                        #wapm_obj.algo(tick.time,tick.price)
                        if (i==1000):
                            self.reqHistoricalTicks(randint(10, 999), self.contract,
                                    str(self.HDATE)+" "+str(time.strftime("%H:%M:%S", time.localtime(int(tick.time)))), "", 1000, "TRADES", 1, True, [])
                            break
                else:
                    for i, tick in enumerate(ticks, start=1):
                        #print(str(time.strftime("%D %H:%M:%S", time.localtime(int(tick.time))))+","+str(tick.price)+","+str(tick.size))
                        filewriter.writerow([str(time.strftime("%D %H:%M:%S", time.localtime(int(tick.time)))), str(tick.price),str(tick.size)])
                        if (i == len(ticks) -1):
                            print("\n")
                            print("~~~~~~~~~~~~~~~~~~~~~~~~ Sucess ~~~~~~~~~~~~~~~~~~~~~~~")
                            print("Check the Out put @ "+tickvuk.parser.get('common', 'hrhd_data_path')+os.sep+self.SYMBOL+"_"+self.SECTYPE+"_"+str(self.HDATE)+".csv")
                            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        except Exception as e:
            main_logger.error(traceback.format_exc())
            print(traceback.format_exc())
        finally:
            self.dumpTestCoverageSituation()
            self.dumpReqAnsErrSituation()

    @iswrapper
    # ! [currenttime]
    def currentTime(self, time:int):
        super().currentTime(time)
        print("CurrentTime:", datetime.datetime.fromtimestamp(time).strftime("%Y%m%d %H:%M:%S"))
    # ! [currenttime]

    
def main():
    #SetupLogger()
    main_logger.debug("Now is %s", datetime.datetime.now())
    #main_logger.getLogger().setLevel(main_logger.ERROR)
    from ibapi import utils
    Contract.__setattr__ = utils.setattr_log
    DeltaNeutralContract.__setattr__ = utils.setattr_log

    try:
        app = TickVuk()
        clear()
        print("\n")
        main_logger.info("Parameter set for back test :"+str(dict(tickvuk.parser.items('common'))))    
        app.connect(app.IP, int(app.PORT), clientId=1)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~ Tickvuk Start's Computing ~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("\n")
        print("Parameter set for back test :"+str(dict(tickvuk.parser.items('common'))))
        print("\n")
        print("IB Gateway Time : %s connectionTime:%s" % (app.serverVersion(), app.twsConnectionTime()))
        print("\n")
        app.contract.symbol = app.SYMBOL
        app.contract.currency = "INR"  
        app.contract.exchange = "NSE"
        if(app.SECTYPE == "STK"):
            app.contract.secType = app.SECTYPE
        elif(app.SECTYPE == "FUT"):
            app.contract.secType = app.SECTYPE
            app.contract.lastTradeDateOrContractMonth = app.EXPIRY
        elif(app.SECTYPE == "OPT"):
            app.contract.secType = app.SECTYPE
            app.contract.lastTradeDateOrContractMonth = app.EXPIRY
            app.contract.strike = app.STRIKE
            app.contract.right = app.RIGHT
            #app.contract.multiplier = "100"
        
        print("Instrument Details : "+str(app.contract))
        print("\n")
        print("Date : "+str(app.HDATE))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("\n")
        
        if not os.path.exists(tickvuk.parser.get('common', 'hrhd_data_path')):
            os.makedirs(tickvuk.parser.get('common', 'hrhd_data_path'))

        with open(tickvuk.parser.get('common', 'hrhd_data_path')+os.sep+app.SYMBOL+"_"+app.SECTYPE+"_"+str(app.HDATE)+".csv", 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(["TIME","PRICE","SIZE"])
        app.reqHistoricalTicks(1, app.contract,
                                str(app.HDATE)+" 09:10:00", "", 1000, "TRADES", 1, True, [])
        
        app.run()
        app.disconnect()
       
    except Exception :
        main_logger.error(traceback.format_exc())
        print("\n")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Error ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Error : "+traceback.format_exc())
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    finally:
        app.dumpTestCoverageSituation()
        app.dumpReqAnsErrSituation()
        
     

if __name__ == "__main__":
    main()