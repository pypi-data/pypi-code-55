import csv

from ofxstatement.parser import CsvStatementParser
from ofxstatement.plugin import Plugin
from ofxstatement.statement import generate_transaction_id


class ALBankPlugin(Plugin):
    """Arbejdernes Landsbank <https://www.al-bank.dk>"""

    def get_parser(self, filename):
        bank_id = self.settings.get('bank', 'ALBADKKK')
        account_id = self.settings.get('account')
        return ALBankParser(open(filename, mode='r', encoding='ISO-8859-15'), bank_id, account_id)


class ALBankParser(CsvStatementParser):
    date_format = '%d-%m-%Y'

    def __init__(self, fin, bank_id, account_id):
        super().__init__(fin)
        self.statement.bank_id = bank_id
        self.statement.account_id = account_id
        self.statement.currency = 'DKK'
        self.headers = {}
        self.row_num = 0
        self.balance = None
        self.balance_date = None

    def parse(self):
        s = super().parse()
        s.end_balance = self.balance
        s.end_date = self.balance_date
        return s

    def split_records(self):
        reader = csv.reader(self.fin, delimiter=';')

        headers = next(reader)
        for i, header in enumerate(headers):
            self.headers[header] = i
            if header == 'Dato':
                self.mappings['date'] = i
            elif header == 'Valørdato':
                self.mappings['date_user'] = i
            elif header == 'Tekst':
                self.mappings['memo'] = i
            elif header == 'Beløb':
                self.mappings['amount'] = i

        return reader

    def parse_record(self, line):
        r = super().parse_record(line)
        self.row_num += 1

        r.refnum = str(self.row_num)
        r.trntype = self.get_type(r)
        if r.date_user:
            r.date_user = self.parse_datetime(r.date_user)
        r.memo = self.concat(r.memo, line, 'Tekst til modtager')
        r.memo = self.concat(r.memo, line, 'Supp. tekst til modtager')
        if r.amount < 0:
            r.memo = self.concat(r.memo, line, 'Modtagernavn')
            r.memo = self.concat(r.memo, line, 'Modtagerkonto')
        elif r.amount > 0:
            r.memo = self.concat(r.memo, line, 'Indbetaler')
        r.id = generate_transaction_id(r)

        balance = self.get_value(line, 'Saldo')
        if balance:
            self.balance = self.parse_float(balance)
            self.balance_date = r.date

        return r

    def parse_datetime(self, value):
        if isinstance(value, str):
            return super().parse_datetime(value)
        else:
            return value

    def parse_float(self, value):
        value = value.replace(',', '.')
        return super().parse_float(value)

    def concat(self, text, line, header):
        result = text or ''
        value = self.get_value(line, header)
        if value:
            components = result.split(' | ')
            if value not in components:
                if result:
                    result += ' | '
                result += value
        return result

    def get_value(self, line, header):
        if header in self.headers:
            index = self.headers[header]
            value = line[index]
            if value:
                return value.strip()
        return ''

    @staticmethod
    def get_type(line):
        if line.amount > 0:
            return 'CREDIT'
        elif line.amount < 0:
            return 'DEBIT'
        else:
            return 'OTHER'
