import Tickvuk.__init__ as tickvuk

class HasaObjects():
    SYMBOL = tickvuk.parser.get('common', 'symbol')
    TI = int(tickvuk.parser.get(SYMBOL, 'TI'))
    SL = float(tickvuk.parser.get(SYMBOL, 'SL'))
    DTH = float(tickvuk.parser.get(SYMBOL, 'DTH'))
    TSL = float(tickvuk.parser.get(SYMBOL, 'TSL'))
    HACT = int(tickvuk.parser.get('common', 'hact'))

    titicks = [] # this list we are going to save time interaval ticks
    avgs = []
    LB_Position = False # Long buy position
    SS_Position = False # Short sell position

    LB_Price = 0 #long buy Price
    SS_Price = 0 #short sell Price

    No_Trades = 0 # no of trades
    net_profit = [] # Profit/loss array

    LB_SL_Price = 0 #Long buy stop loss
    SS_SL_Price = 0 #Short sell stop loss
    LB_TSL=[] # Long buy Trailing stoploss array
    SS_TSL=[] # Short sell Trailing stoploss array

    HA_c1 = [ 0.0 , 0.0 , 0.0 , 0.0 , 'white' ] # Heikin Ashi Candle 1
    HA_c2 = [ 0.0 , 0.0 , 0.0 , 0.0 , 'white' ] # Heikin Ashi Candle 2
    HA_c3 = [ 0.0 , 0.0 , 0.0 , 0.0 , 'white' ] # Heikin Ashi Candle 3
    HA_c4 = [ 0.0 , 0.0 , 0.0 , 0.0 , 'white' ] # Heikin Ashi Candle 4
