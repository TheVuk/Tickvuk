import Tickvuk.__init__ as tickvuk

class SapmObjects():
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
    LB_Price = 0 #long buy Price
    SS_Price = 0 #short sell Price
    No_Trades = 0
    net_profit = []
    LB_TSL = []
    SS_TSL = []
