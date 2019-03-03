import sys, os, logging
sys.path.append(os.getcwd())
from Tickvuk.src.algos.hasa.hasa_objects import HasaObjects as ho
from Tickvuk.src.loghandler.logger import hasa_logger
import datetime
import time
import Tickvuk.__init__ as tickvuk

class HasaAlgo():


    def algo(self, ticktime, tickprice, tickvolume):
        if (len(ho.titicks) > 0):
            if ((float(ticktime)-float(ho.titicks[0][0])) >= ho.HACT ):
                ho.titicks.append([ticktime,tickprice,tickvolume])
                if ((float(ticktime)-float(ho.titicks[0][0])) == 0 ):
                    ho.HA_c4[0]= ho.HA_c4[1] = ho.HA_c4[2] = float(tickprice) # catch open and initilialize low and high
                elif ((float(ticktime)-float(ho.titicks[0][0])) > (float(ho.HACT)-2) ):
                    ho.HA_c4[3] = tickprice
                if (float(ho.HA_c4[1]) > float(tickprice)):
                    float(ho.HA_c4[1]) = float(tickprice)   #Find low
                elif (float(ho.HA_c4[2]) < float(tickprice)):
                    float(ho.HA_c4[2]) = float(tickprice)   #Find high




        if (len(ho.titicks) > 0):
            if ((float(ticktime)-float(ho.titicks[0][0])) >= ho.TI ):
                ho.titicks.append([ticktime,tickprice])
                sum_value = 0.0
                for i in ho.titicks:
                    sum_value = sum_value + i[1]
                if (len(ho.avgs) < 4 ):
                    ho.avgs.append(sum_value / len(ho.titicks))
                else:
                    ho.avgs[0] = ho.avgs[1]
                    ho.avgs[1] = ho.avgs[2]
                    # ho.avgs[2] = ho.avgs[3]
                    ho.avgs[2] = (sum_value / len(ho.titicks))
                    #print("*Avg - "+str(ho.avgs[2]) + ", TickTime - "+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime)))))


                ho.titicks.clear()
            else:
                ho.titicks.append([ticktime,tickprice])
        else:
            ho.titicks.append([ticktime,tickprice])


# if __name__ == '__main__':
#     hobj = HasaAlgo()
#     testlist = [[1548906300,165.0],[1548906303,165.25],[1548906309,165.15]]
#     for item in testlist:
#         hobj.algo(item[0],item[1])
#     print(ho.titicks)



        # TSL
        # if (ho.LBuy_Position == True):
        #     if (tickprice >= (ho.LSL_Price + ho.SL + ho.TSL)):
        #         ho.LSL_Price = ho.LSL_Price + ho.TSL
        #     elif(tickprice <= ho.LSL_Price):
        #         print("* LONG EXIT ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(tickprice))
        #         print(ho.LB_TSL)
        #         ho.LB_TSL[:] =[]
        #         # print ("LONG postion :"+str(tickprice - ho.LB_Price))
        #         ho.net_profit.append(tickprice - ho.LB_Price)
        #         ho.LBuy_Position = False
        #         ho.LB_Price = 0
        #         ho.No_Trades = ho.No_Trades +1
        #         print ("NET :"+str(sum(ho.net_profit)))
        #         print("Number of TRADES :"+ str(ho.No_Trades))
        # if (ho.SSell_Position == True):
        #     if (tickprice <= (ho.SSL_Price - ho.SL - ho.TSL)):
        #         ho.SSL_Price = ho.SSL_Price - ho.TSL
        #     elif(tickprice >= ho.SSL_Price):
        #         print("* SHORT EXIT ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(tickprice))
        #         print(ho.SS_TSL)
        #         ho.SS_TSL[:] =[]
        #         # print ("SHORT postion :"+str(ho.SS_Price - tickprice))
        #         ho.net_profit.append(ho.SS_Price - tickprice)
        #         ho.SSell_Position = False
        #         ho.SS_Price = 0
        #         ho.No_Trades = ho.No_Trades +1
        #         print ("NET :"+str(sum(ho.net_profit)))
        #         print("Number of TRADES :"+ str(ho.No_Trades))




                        if (len(ho.avgs) == 4):
                            pv_delta = (ho.avgs[3] - ho.avgs[1])/ho.avgs[3]*100
                            # pv_beta = (ho.avgs[2] - ho.avgs[0])/ho.avgs[2]*100
                            # print("     "+str(pv_delta)+","+str(tickprice))
                            if ((pv_delta >=  ho.DTH)):
                            # & (pv_delta > pv_beta)

                                # print(str(pv_delta)+","+str(tickprice))
                                # if(ho.LBuy_Position == False):
                                #     if (ho.SSell_Position == True):
                                #         print("SHORT EXIT ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(pv_delta)+","+str(tickprice))
                                #         print(ho.SS_TSL)
                                #         # print ("SHORT postion :"+str(ho.SS_Price - tickprice))
                                #         ho.net_profit.append(ho.SS_Price - tickprice)
                                #         ho.SSell_Position = False
                                #         ho.SS_Price = 0
                                #         ho.No_Trades = ho.No_Trades +1
                                #         ho.SS_TSL[:] =[]
                                #         print ("NET :"+str(sum(ho.net_profit)))
                                #         print("Number of TRADES :"+ str(ho.No_Trades))
                                #     print("LONG ENTRY ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(pv_delta)+","+str(tickprice))
                                #     ho.LB_Price = tickprice
                                #     ho.LBuy_Position = True
                                #     ho.LSL_Price = tickprice - ho.SL
                                #     ho.LB_TSL.append(ho.LSL_Price)
                                # if((tickprice > ho.LB_TSL[len(ho.LB_TSL)-1])):
                                #     ho.LB_TSL.append(tickprice)
                                    # if( ho.LSL_Price < ho.LB_TSL[len(ho.LB_TSL)-2]):
                                    #     ho.LSL_Price = ho.LB_TSL[len(ho.LB_TSL)-2]



                            if ((pv_delta <=  (ho.DTH * -1))):
                                # & (pv_delta < pv_beta)):

                                # print(str(pv_delta)+","+str(tickprice))
                                # if(ho.SSell_Position == False):
                                #     if (ho.LBuy_Position == True):
                                #         print("LONG EXIT ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(pv_delta)+","+str(tickprice))
                                #         print(ho.LB_TSL)
                                #         # print ("LONG postion :"+str(tickprice - ho.LB_Price))
                                #         ho.net_profit.append(tickprice - ho.LB_Price)
                                #         ho.LBuy_Position = False
                                #         ho.LB_Price = 0
                                #         ho.No_Trades = ho.No_Trades +1
                                #         ho.LB_TSL[:] =[]
                                #         print ("NET :"+str(sum(ho.net_profit)))
                                #         print("Number of TRADES :"+ str(ho.No_Trades))
                                #     print("SHORT ENTRY ,"+str(time.strftime("%D %H:%M:%S", time.localtime(int(ticktime))))+","+str(pv_delta)+","+str(tickprice))
                                #     ho.SS_Price = tickprice
                                #     ho.SSell_Position = True
                                #     ho.SSL_Price = tickprice + ho.SL
                                #     ho.SS_TSL.append(ho.SSL_Price)
                                # if((tickprice < ho.SS_TSL[len(ho.SS_TSL)-1])):
                                #     ho.SS_TSL.append(tickprice)
                                    # if(ho.SSL_Price > ho.SS_TSL[len(ho.SS_TSL)-2]):
                                    #     ho.SSL_Price = ho.SS_TSL[len(ho.SS_TSL)-2]
