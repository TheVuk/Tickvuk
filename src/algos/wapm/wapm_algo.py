import sys, os, logging
sys.path.append(os.getcwd())
from Tickvuk.src.algos.wapm.wapm_objects import WapmObjects as wo
from Tickvuk.src.loghandler.logger import wapm_logger
import datetime
import time
import Tickvuk.__init__ as tickvuk


class WapmAlgo():

    def algo(self, ticktime, tickprice):
        if (wo.LBuy_Position == True):
            if (tickprice >= (wo.LSL_Price + wo.SL + wo.TSL)):
                wo.LSL_Price = wo.LSL_Price + wo.TSL
            elif(tickprice <= wo.LSL_Price):
                print(str("* LONG EXIT * ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(tickprice)))
                wo.LBuy_Position = False
                wo.No_Trades = wo.No_Trades +1
        if (wo.SSell_Position == True):
            if (tickprice <= (wo.SSL_Price - wo.SL - wo.TSL)):
                wo.SSL_Price = wo.SSL_Price - wo.TSL
            elif(tickprice >= wo.SSL_Price):
                print(str("* SHORT EXIT * ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(tickprice)))
                wo.SSell_Position = False
                wo.No_Trades = wo.No_Trades +1  

        if (len(wo.titicks) > 0):
            if ((float(ticktime)-float(wo.titicks[0][0])) >= wo.TI ):
                wo.titicks.append([ticktime,tickprice])
                sum_value = 0.0 
                for i in wo.titicks:
                    sum_value = sum_value + i[1]
                if (len(wo.avgs) < 3 ):
                    wo.avgs.append(sum_value / len(wo.titicks))
                else:
                    wo.avgs[0] = wo.avgs[1]
                    wo.avgs[1] = wo.avgs[2]
                    wo.avgs[2] = (sum_value / len(wo.titicks))
                    #print("*Avg - "+str(wo.avgs[2]) + ", TickTime - "+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime)))))
                if (len(wo.avgs) == 3):
                    pv_delta = (wo.avgs[2] - wo.avgs[0])/wo.avgs[2]*100
                    if (pv_delta >=  wo.DTH) & (wo.LBuy_Position == False):
                        print(str("* LONG ENTRY * ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(tickprice)))
                        wo.LBuy_Position = True
                        wo.LSL_Price = tickprice - wo.SL
                    if (pv_delta <=  (wo.DTH * -1)) & (wo.SSell_Position == False):
                        print(str("* SHORT ENTRY * ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(tickprice)))
                        wo.SSell_Position = True
                        wo.SSL_Price = tickprice + wo.SL
                wo.titicks.clear()
            else:
                wo.titicks.append([ticktime,tickprice])
        else:
            wo.titicks.append([ticktime,tickprice])

if __name__ == '__main__':
    wobj = WapmAlgo()
    testlist = [[1548906300,165.0],[1548906303,165.25],[1548906309,165.15]]
    for item in testlist:
        wobj.algo(item[0],item[1])
    print(wo.titicks)
