import sys, os, logging
sys.path.append(os.getcwd())
from Tickvuk.src.algos.sapm.sapm_objects import SapmObjects as so
from Tickvuk.src.loghandler.logger import sapm_logger
import datetime
import time
import Tickvuk.__init__ as tickvuk

class SapmAlgo():

    def algo(self, ticktime, tickprice):
        if (so.LBuy_Position == True):
            if (tickprice >= (so.LSL_Price + so.SL + so.TSL)):
                so.LSL_Price = so.LSL_Price + so.TSL
            elif(tickprice <= so.LSL_Price):
                print("LONG EXIT ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(tickprice))
                so.LBuy_Position = False
                so.No_Trades = so.No_Trades +1
        if (so.SSell_Position == True):
            if (tickprice <= (so.SSL_Price - so.SL - so.TSL)):
                so.SSL_Price = so.SSL_Price - so.TSL
            elif(tickprice >= so.SSL_Price):
                print("SHORT EXIT ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(tickprice))
                so.SSell_Position = False
                so.No_Trades = so.No_Trades +1  

        if (len(so.titicks) > 0):
            if ((float(ticktime)-float(so.titicks[0][0])) >= so.TI ):
                so.titicks.append([ticktime,tickprice])
                sum_value = 0.0 
                for i in so.titicks:
                    sum_value = sum_value + i[1]
                if (len(so.avgs) < 3 ):
                    so.avgs.append(sum_value / len(so.titicks))
                else:
                    so.avgs[0] = so.avgs[1]
                    so.avgs[1] = so.avgs[2]
                    so.avgs[2] = (sum_value / len(so.titicks))
                    #print("*Avg - "+str(so.avgs[2]) + ", TickTime - "+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime)))))
                if (len(so.avgs) == 3):
                    pv_delta = (so.avgs[2] - so.avgs[0])/so.avgs[2]*100
                    # print("     "+str(pv_delta)+","+str(tickprice))
                    if (pv_delta >=  so.DTH) & (so.LBuy_Position == False):
                        if (so.SSell_Position == True):
                            print("SHORT EXIT ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(tickprice))
                            so.SSell_Position = False
                            so.No_Trades = so.No_Trades +1
                        print("LONG ENTRY ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(tickprice))
                        so.LBuy_Position = True
                        so.LSL_Price = tickprice - so.SL
                        
                        
                    if (pv_delta <=  (so.DTH * -1)) & (so.SSell_Position == False):
                        if (so.LBuy_Position == True):
                            print("LONG EXIT ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(tickprice))
                            so.LBuy_Position = False
                            so.No_Trades = so.No_Trades +1
                        print("SHORT ENTRY ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(tickprice))
                        so.SSell_Position = True
                        so.SSL_Price = tickprice + so.SL
                        
                so.titicks.clear()
            else:
                so.titicks.append([ticktime,tickprice])
        else:
            so.titicks.append([ticktime,tickprice])
        

if __name__ == '__main__':
    sobj = SapmAlgo()
    testlist = [[1548906300,165.0],[1548906303,165.25],[1548906309,165.15]]
    for item in testlist:
        sobj.algo(item[0],item[1])
    print(so.titicks)
