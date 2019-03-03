import Tickvuk.__init__ as tickvuk
import csv, os

class WapmObjects():

    SYMBOL = tickvuk.parser.get('common', 'symbol')
    TI = int(tickvuk.parser.get(SYMBOL, 'TI'))
    SL = float(tickvuk.parser.get(SYMBOL, 'SL'))
    DTH = float(tickvuk.parser.get(SYMBOL, 'DTH'))
    TSL = float(tickvuk.parser.get(SYMBOL, 'TSL'))
    titicks = [] # this list we are going to save time interaval ticks
    avgs = []
    LBuy_Position = False # Long buy position
    SSell_Position = False # Short sell position
    LSL_Price = 0 #Long buy stop loss
    SSL_Price = 0 #Shotsell stop loss
    No_Trades = 0
