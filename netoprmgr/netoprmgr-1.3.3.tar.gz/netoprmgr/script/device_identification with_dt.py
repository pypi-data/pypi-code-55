#using netmiko with raw_data include device_type
import xlrd
import xlsxwriter
from netmiko import Netmiko

def device_identification(raw_data_dir):
    book = xlrd.open_workbook(raw_data_dir)
    first_sheet = book.sheet_by_index(0)
    cell = first_sheet.cell(0,0)

    wb = xlsxwriter.Workbook('devices_data.xlsx')
    ws = wb.add_worksheet('summary')

    count_row = 0
    for i in range(first_sheet.nrows):
        
        my_device = {
            "host": first_sheet.row_values(i)[1],
            "username": first_sheet.row_values(i)[2],
            "password": first_sheet.row_values(i)[3],
            "device_type": first_sheet.row_values(i)[4],
        }

        try:
            net_connect = Netmiko(**my_device)
            output = net_connect.send_command('show ver')
            print(output)

            ws.write(count_row,0,first_sheet.row_values(i)[0])
            ws.write(count_row,1,my_device["host"])
            ws.write(count_row,2,my_device["username"])
            ws.write(count_row,3,my_device["password"])
            ws.write(count_row,4,my_device["device_type"])

            if 'C3850' in output:
                ws.write(count_row,5,'C3850')
            elif 'C2960' in output:
                ws.write(count_row,5,'C2960')

        except:
            pass

        count_row+=1
    wb.close()