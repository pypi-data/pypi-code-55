from colorama import Style, Fore


class TickLiveData:
    def __init__(self, symbol):
        # --Common Variables
        self.timestamp = None
        self.symbol = symbol
        self.symbol_id = None
        self.day_high = None
        self.day_low = None
        self.day_open = None
        self.prev_day_close = None
        self.prev_day_oi = None
        self.oi = None
        self.change = None
        self.change_perc = None
        self.oi_change = None
        self.oi_change_perc = None
        self.volume = None
        # --Obj specific
        self.ltp = None
        self.atp = None
        self.ttq = None
        self.special_tag = ""
        self.tick_seq = None
        self.best_bid_price = None
        self.best_bid_qty = None
        self.best_ask_price = None
        self.best_ask_qty = None
        # -- Unused
        # self.exchange = 'NSE'
        # -For level 2 and level 3 data
        # self.bids = []
        # self.asks = []

    def __eq__(self, other):
        res = True
        assert type(self) == type(other)
        try:
            if self.tick_seq != other.tick_seq:
                res = False
            elif self.best_bid_price != other.best_bid_price\
                    or self.best_bid_qty != other.best_bid_qty\
                    or self.best_ask_price != other.best_ask_price\
                    or self.best_ask_qty != other.best_ask_qty:
                res = False
        except AttributeError:
            pass
        return res

    def __str__(self):
        if self.special_tag == "":
            starting_formatter = ending_formatter = ""
        else:
            if self.special_tag == "H":
                starting_formatter = f"{Style.BRIGHT}{Fore.GREEN}"
                ending_formatter = f"{Style.RESET_ALL}"
            elif self.special_tag == "L":
                starting_formatter = f"{Style.BRIGHT}{Fore.RED}"
                ending_formatter = f"{Style.RESET_ALL}"
            else:
                starting_formatter = ending_formatter = ""
        return f"{starting_formatter}{str(self.__dict__)}{ending_formatter}"


class MinLiveData:
    def __init__(self, symbol):
        # --Common Variables
        self.timestamp = None
        self.symbol = symbol
        self.symbol_id = None
        self.day_high = None
        self.day_low = None
        self.day_open = None
        self.prev_day_close = None
        self.prev_day_oi = None
        self.oi = None
        self.change = None
        self.change_perc = None
        self.oi_change = None
        self.oi_change_perc = None
        self.volume = None
        # --Obj specific
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        # --Unused
        # self.exchange = 'NSE'
        # -For level 2 and level 3 data
        # self.bids = []
        # self.asks = []

    def __eq__(self, other):
        res = True
        assert type(self) == type(other)
        if self.timestamp != other.timestamp\
                or self.symbol != other.symbol:
            res = False
        return res

    def __str__(self):
        return str(self.__dict__)


class TouchlineData:
    def __init__(self):
        self.symbol = None
        self.truedata_id = None
        self.open = None
        self.high = None
        self.low = None
        self.ltp = None
        self.prev_close = None
        self.ttq = None
        self.oi = None
        self.prev_oi = None
        self.turnover = None

    def __str__(self):
        return str(self.__dict__)
