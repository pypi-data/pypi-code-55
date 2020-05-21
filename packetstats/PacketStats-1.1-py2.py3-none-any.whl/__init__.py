# __init__.py
import csv

from .statistics import *
from .convertion import *


def generate_csv(f_name, move, percentage, header_names):
    export_to_txt(f_name, f_name.split('.')[0] + '.csv')
    delete_non_udp(f_name.split('.')[0] + '.csv', header_names)
    print("%s %s %s" % (f_name, move, percentage))
    result = permutations(statistics(f_name, header_names), header_names, move, percentage)
    with open(f_name.split('.')[0] + '-generated-data.csv', 'w', newline='') as file:
        csv_file = csv.writer(file, delimiter='\t')
        for row in result:
            csv_file.writerow(row)
