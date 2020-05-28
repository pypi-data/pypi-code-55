from .file import File
from pysheets import Spreadsheet
from pysheets.spreadsheet import create_from_csv


class CSVFileError(Exception):
    pass


class CSVFile(File):
    def __init__(self, file_path, create=False):
        super().__init__(file_path, create=create)
        if not self.file.endswith(".csv"):
            raise CSVFileError(f"{self.file} isn't a csv file.")

    def add_row(self, row):
        read = self.read()
        new_content = read + "\r\n" + row
        self.write(new_content, is_txt=True)

    def add_rows(self, rows=None):
        if rows is None:
            rows = []

        for row in rows:
            self.add_row(row)

    def add_column(self, column):
        with open(self.file, "r") as file:
            lines = file.readlines()

        for y in range(len(column)):
            lines[y] = lines[y] + "," + column[y]

        dump = ""
        for line in lines:
            dump += line + "\r\n"
        dump = dump [0:len(dump)-2]

        with open(self.file, "w") as file:
            file.write(dump)

    def add_columns(self, columns=None):
        for column in columns:
            self.add_column(column)

    @property
    def sheet(self):
        return create_from_csv(self.file)

    def get_cell(self, x, y):
        return self.sheet.get_cell(x, y)

    def change_cell(self, x, y, new_content):
        sheet = self.sheet
        sheet.change_cell(x, y, new_content)
        sheet.csv(self.file)

    @property
    def x_len(self):
        return self.sheet.x_len

    @property
    def y_len(self):
        return self.sheet.y_len



