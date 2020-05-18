from pyxlsx import new_xlsx

filename = r"/Users/fort/git/python_projects/pyxlsx/pyxlsx/tests/data/test.xlsx"

def test_new(filename):
    with new_xlsx(filename) as wb:
        ws = wb.create_sheet()
        ws['A1'] = 1
        ws['A2'] = 2
        ws['a3'] = 3
        ws['a4'] = 4

        ws['B1'] = 2
        ws['B2'] = 4
        ws['B3'] = 6
        ws['B4'] = 8
        for row in range(1, 5):
            ws.cell(row, 3).value = "=A{0}+B{0}".format(row)  
            ws.cell(row, 4).value = "=vlookup(C{0}, A1:B4, 2, FALSE)".format(row)  
        
        print(ws['C1'].data)

if __name__ == "__main__":
    test_new(filename)