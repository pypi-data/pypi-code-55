'''
The helper for Ledger output parsing
'''

class LedgerOutputParser:
    def __init__(self):
        super().__init__()
    
    def get_total_lines(self, output):
        '''
        Extract the total lines from the output, 
        unless there is only one account, in which case use the complete output
        '''
        result = []
        next_line_is_total = False
        total_line = None

        # Special cases
        # if len(output) == 0:
        #     return 0
        
        if len(output) == 1:
            # No income is an array with an empty string ['']
            if output[0] == '':
                total_line = "0"
            else:
                # One-line results don't have totals
                total_line = output[0]
            result.append(total_line)
        else:
            for i, item in enumerate(output):
                # get total
                if next_line_is_total:
                    total_line = output[i]
                    #self.logger.debug(f'total {total_line}')
                    result.append(total_line)
                else:
                    if '------' in output[i]:
                        next_line_is_total = True

        if total_line is None:
            raise ValueError(f'No total fetched in {output}')

        return result

    def get_lot_lines(self, output):
        pass
