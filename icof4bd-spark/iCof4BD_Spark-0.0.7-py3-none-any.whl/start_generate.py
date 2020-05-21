import argparse
import os

from iCof4BD_Spark.generate_template import *
from iCof4BD_Spark.generate_xml import generate_xml
from iCof4BD_Spark.web_crawl import WebCrawl


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', metavar='URL_address', type=str,
                        help='http://host:port/history/application_*/1/jobs', required=True)
    parser.add_argument('-s', '--slaves', metavar='Slave_numbers', type=int, help='The slave Numbers', required=True)
    parser.add_argument('-start', '--start_application', metavar='Application_Range', type=str,
                        help='The range of your application, started from this one')
    parser.add_argument('-end', '--end_application', metavar='Application_Range', type=str,
                        help='The range of your application, ended to this one')
    parser.add_argument('-apps', '--applications', metavar='Applications', type=str, nargs='+', help='Application[s]')
    # parser.add_argument('-g', '--generate_template', metavar='Generate_Template_File', type=str,
    # choices=['Y', 'N'], default='N', help='Generate_Template_File')

    args = parser.parse_args()

    start_application = args.start_application
    end_application = args.end_application
    applications = args.applications
    # generate_template = args.generate_template

    application_id_range = []

    if start_application or applications:
        if start_application:
            if end_application and start_application.split("_")[1] == end_application.split("_")[1]:
                for i in range(int(start_application.split("_")[2]), int(end_application.split("_")[2]) + 1):
                    application_id_range.append(
                        start_application.split("_")[0] + '_' + start_application.split("_")[1] + '_' + ("%04d" % i))
            else:
                print("Please check --start_application and --end_application")
        if applications:
            for application in applications:
                application_id_range.append(application)
    else:
        print("No applications Input, Please check --start_application and --end_application or --applications")
    if not (os.path.exists('xml_ini.xml')):
        wc = WebCrawl()
        wc.get_start_page(args.url, application_id_range[0])
        generate_xml_template(wc, args.slaves)
        del wc
        print("Generated files: xml_ini.xml, please check!")
    if not (os.path.exists('use_this_cofs_dp.csv')):
        generate_csv_file_template(args.slaves)
        print("Generated files: use_this_cofs_dp.csv, please check!")
    if not (os.path.exists('run_ini.txt')):
        generate_batch_file_template()
        print("Generated files: run_ini.txt, please check!")
    try:
        with open('run.bat', 'a') as f:
            f.seek(0)
            f.truncate()
            f.close()
    except FileNotFoundError:
        print("Please check the batch file path: " + 'run.bat')
    while application_id_range:
        print(application_id_range[0] + ' start')
        try:
            wc = WebCrawl()
            wc.get_start_page(args.url, application_id_range[0])
            generate_xml(wc, args.slaves)
            print(application_id_range[0] + ' finished')
        except IndexError:
            print("Application_Id don't match")

            print(application_id_range[0] + ' failed')
        application_id_range.remove(application_id_range[0])


if __name__ == "__main__":
    # string = 'http://10.239.166.104:18088/history/application_1587718859083_0232/1/jobs  '
    # lists=string.strip().split('/')
    # print(lists)
    # print(lists[4])
    # lists[4]='aaa'
    # print('/'.join(lists))
    # host = string.strip().split('/hi')
    # print(host)
    main()
