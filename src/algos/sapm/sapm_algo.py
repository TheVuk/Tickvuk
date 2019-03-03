import sys, os, logging
# import pandas as pd
sys.path.append(os.getcwd())
from Tickvuk.src.algos.sapm.sapm_objects import SapmObjects as so
from Tickvuk.src.loghandler.logger import sapm_logger
import datetime
import time
import Tickvuk.__init__ as tickvuk

entime = datetime.datetime.strptime(tickvuk.parser.get('common', 'date')+' 09:30:00', '%Y%m%d %H:%M:%S')
ent930am = time.mktime(entime.timetuple())
extime = datetime.datetime.strptime(tickvuk.parser.get('common', 'date')+' 15:20:00', '%Y%m%d %H:%M:%S')
exit320pm = time.mktime(extime.timetuple())



class SapmAlgo():

    def algo(self, ticktime, tickprice):
        # if (so.SL == 0 ):
        #     so.SL = round(tickprice/100, 2)
        #     so.TSL = round(tickprice/200, 2)
        #     print("*** SL set to :"+ str(so.SL) +"TSL set to :"+str(so.TSL))
        if ( ticktime > exit320pm ) :
            if (so.LBuy_Position == True):
                print("*** LONG EXIT ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(tickprice))
                print(so.LB_TSL)
                so.LB_TSL[:] =[]
                print ("LONG postion :"+str(tickprice - so.LB_Price))
                so.net_profit.append(tickprice - so.LB_Price)
                so.LBuy_Position = False
                so.LB_Price = 0
                so.No_Trades = so.No_Trades +1
                print ("NET :"+str(sum(so.net_profit)))
                print("Number of TRADES :"+ str(so.No_Trades))
            if (so.SSell_Position == True):
                print("*** SHORT EXIT ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(tickprice))
                print(so.SS_TSL)
                so.SS_TSL[:] =[]
                print ("SHORT postion :"+str(so.SS_Price - tickprice))
                so.net_profit.append(so.SS_Price - tickprice)
                so.SSell_Position = False
                so.SS_Price = 0
                so.No_Trades = so.No_Trades +1
                print ("NET :"+str(sum(so.net_profit)))
                print("Number of TRADES :"+ str(so.No_Trades))

        if (so.LBuy_Position == True):
            if (tickprice >= (so.LSL_Price + so.SL + so.TSL)):
                so.LSL_Price = so.LSL_Price + so.TSL
            elif(tickprice <= so.LSL_Price):
                print("* LONG EXIT ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(tickprice))
                print(so.LB_TSL)
                so.LB_TSL[:] =[]
                print ("LONG postion :"+str(tickprice - so.LB_Price))
                so.net_profit.append(tickprice - so.LB_Price)
                so.LBuy_Position = False
                so.LB_Price = 0
                so.No_Trades = so.No_Trades +1
                print ("NET :"+str(sum(so.net_profit)))
                print("Number of TRADES :"+ str(so.No_Trades))
        if (so.SSell_Position == True):
            if (tickprice <= (so.SSL_Price - so.SL - so.TSL)):
                so.SSL_Price = so.SSL_Price - so.TSL
            elif(tickprice >= so.SSL_Price):
                print("* SHORT EXIT ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(tickprice))
                print(so.SS_TSL)
                so.SS_TSL[:] =[]
                print ("SHORT postion :"+str(so.SS_Price - tickprice))
                so.net_profit.append(so.SS_Price - tickprice)
                so.SSell_Position = False
                so.SS_Price = 0
                so.No_Trades = so.No_Trades +1
                print ("NET :"+str(sum(so.net_profit)))
                print("Number of TRADES :"+ str(so.No_Trades))

        if ( ticktime < exit320pm and ticktime > ent930am ) :
            if (len(so.titicks) > 0):
                if ((float(ticktime)-float(so.titicks[0][0])) >= so.TI ):
                    so.titicks.append([ticktime,tickprice])
                    sum_value = 0.0
                    for i in so.titicks:
                        sum_value = sum_value + i[1]
                    if (len(so.avgs) < 4 ):
                        so.avgs.append(sum_value / len(so.titicks))
                    else:
                        so.avgs[0] = so.avgs[1]
                        so.avgs[1] = so.avgs[2]
                        # so.avgs[2] = so.avgs[3]
                        so.avgs[2] = (sum_value / len(so.titicks))
                        #print("*Avg - "+str(so.avgs[2]) + ", TickTime - "+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime)))))
                    if (len(so.avgs) == 4):
                        pv_delta = (so.avgs[3] - so.avgs[1])/so.avgs[3]*100
                        # pv_beta = (so.avgs[2] - so.avgs[0])/so.avgs[2]*100
                        # print("     "+str(pv_delta)+","+str(tickprice))
                        if ((pv_delta >=  so.DTH)):
                        # & (pv_delta > pv_beta)
                            # print(str(pv_delta)+","+str(tickprice))
                            if(so.LBuy_Position == False):
                                if (so.SSell_Position == True):
                                    print("SHORT EXIT ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(pv_delta)+","+str(tickprice))
                                    print(so.SS_TSL)
                                    print ("SHORT postion :"+str(so.SS_Price - tickprice))
                                    so.net_profit.append(so.SS_Price - tickprice)
                                    so.SSell_Position = False
                                    so.SS_Price = 0
                                    so.No_Trades = so.No_Trades +1
                                    so.SS_TSL[:] =[]
                                    print ("NET :"+str(sum(so.net_profit)))
                                    print("Number of TRADES :"+ str(so.No_Trades))
                                print("LONG ENTRY ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(pv_delta)+","+str(tickprice))
                                so.LB_Price = tickprice
                                so.LBuy_Position = True
                                so.LSL_Price = tickprice - so.SL
                                so.LB_TSL.append(so.LSL_Price)
                            if((tickprice > so.LB_TSL[len(so.LB_TSL)-1])):
                                so.LB_TSL.append(tickprice)
                                # if( so.LSL_Price < so.LB_TSL[len(so.LB_TSL)-2]):
                                #     so.LSL_Price = so.LB_TSL[len(so.LB_TSL)-2]



                        if ((pv_delta <=  (so.DTH * -1))):
                            # & (pv_delta < pv_beta)):
                            # print(str(pv_delta)+","+str(tickprice))
                            if(so.SSell_Position == False):
                                if (so.LBuy_Position == True):
                                    print("LONG EXIT ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(pv_delta)+","+str(tickprice))
                                    print(so.LB_TSL)
                                    print ("LONG postion :"+str(tickprice - so.LB_Price))
                                    so.net_profit.append(tickprice - so.LB_Price)
                                    so.LBuy_Position = False
                                    so.LB_Price = 0
                                    so.No_Trades = so.No_Trades +1
                                    so.LB_TSL[:] =[]
                                    print ("NET :"+str(sum(so.net_profit)))
                                    print("Number of TRADES :"+ str(so.No_Trades))
                                print("SHORT ENTRY ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(pv_delta)+","+str(tickprice))
                                so.SS_Price = tickprice
                                so.SSell_Position = True
                                so.SSL_Price = tickprice + so.SL
                                so.SS_TSL.append(so.SSL_Price)
                            if((tickprice < so.SS_TSL[len(so.SS_TSL)-1])):
                                so.SS_TSL.append(tickprice)
                                # if(so.SSL_Price > so.SS_TSL[len(so.SS_TSL)-2]):
                                #     so.SSL_Price = so.SS_TSL[len(so.SS_TSL)-2]

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
