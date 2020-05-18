'''
Parse the output for lots and return the array of lots for a symbol
'''

class LotParser:
    def __init__(self, logger):
        super().__init__()

        self.logger = logger
    
    def get_lots(self, symbol):
        from .ledger_exec import LedgerExecutor
        from .ledger_output_parser import LedgerOutputParser

        params = f"b ^Assets and :{symbol}$ --lots"
    
        ledger = LedgerExecutor(self.logger)
        output = ledger.run(params)
        output = ledger.split_lines(output)

        parser = LedgerOutputParser()
        total_lines = parser.get_total_lines(output)

        return total_lines
