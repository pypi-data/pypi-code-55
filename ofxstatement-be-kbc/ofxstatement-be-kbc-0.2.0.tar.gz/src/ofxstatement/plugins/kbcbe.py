from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.exceptions import ParseError
import csv

LINELENGTH = 18
HEADER_START = "Rekeningnummer"


class KbcBePlugin(Plugin):
    """Belgian KBC Bank plugin for ofxstatement
    """

    def get_parser(self, filename):
        f = open(filename, 'r')
        parser = KbcBeParser(f)
        return parser


class KbcBeParser(CsvStatementParser):
    date_format = "%d/%m/%Y"

    mappings = {
        'memo': 6,
        'date': 5,
        'amount': 8,
        'check_no': 4,
        'refnum': 4
    }

    line_nr = 0

    def split_records(self):
        """Return iterable object consisting of a line per transaction
        """
        return csv.reader(self.fin, delimiter=';')

    def parse_record(self, line):
        """Parse given transaction line and return StatementLine object
        """
        self.line_nr += 1
        if line[0] == HEADER_START:
            return None
        elif len(line) != LINELENGTH:
            raise ParseError(self.line_nr,
                             'Wrong number of fields in line! ' +
                             'Found ' + str(len(line)) + ' fields ' +
                             'but should be ' + str(LINELENGTH) + '!')

        # Check the account id. Each line should be for the same account!
        if self.statement.account_id:
            if line[0] != self.statement.account_id:
                raise ParseError(self.line_nr,
                                 'AccountID does not match on all lines! ' +
                                 'Line has ' + line[0] + ' but file ' +
                                 'started with ' + self.statement.account_id)
        else:
            self.statement.account_id = line[0]

        # Check the currency. Each line should be for the same currency!
        if self.statement.currency:
            if line[3] != self.statement.currency:
                raise ParseError(self.line_nr,
                                 'Currency does not match on all lines! ' +
                                 'Line has ' + line[3] + ' but file ' +
                                 'started with ' + self.statement.currency)
        else:
            self.statement.currency = line[3]

        # Get reconciliation data. First line is the most recent transaction
        # and contains the end balance. Last line is the oldest transaction and
        # contains the start balance plus or minus the oldest transaction
        # amount. Not perfect since we need to calculate, but still valuable.
        if self.line_nr == 2:  # First line with data is line nr 2 :-)
            # Store end balance
            self.statement.end_balance = self.parse_float(line[9])
        else:
            # Calculate start balance & store start balance,
            # will overwrite every time, last line survives.
            self.statement.start_balance = self.parse_float(line[9]) - \
                                           self.parse_float(line[8])

        stmt_ln = super(KbcBeParser, self).parse_record(line)

        return stmt_ln
