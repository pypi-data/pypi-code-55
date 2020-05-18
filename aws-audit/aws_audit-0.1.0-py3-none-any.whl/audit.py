import json, os
import argparse
import importlib
from aws_audit import __version__, __author__
from aws_audit.config.regions import regions, all_regions
from aws_audit.config.rules import services
from aws_audit.output import Output
from aws_audit.configure import Configure
from aws_audit.utils.logger import get_logger
from aws_audit.plugins.initialize import Initialize

def main():
    text = 'This utility will help you with the security audit of AWS cloud services.'
    
    parser = argparse.ArgumentParser(description=text)
    
    parser.add_argument("-v", "--version", help="Shows version of the utility.", action="store_true")
    parser.add_argument("-c", "--configure", help="Configure AWS Access Key ID and Secret Access Key.", action="store_true")
    parser.add_argument("-r", "--regions", help="Pass one or more comma seperated values for aws regions to evaluate the security audit of aws services")
    parser.add_argument("-s", "--services", help="Pass one or more comma seperated values for aws services that needs to be evaluated for security audit")
    parser.add_argument("-ls", "--list-services", help="Get list of all supported services.", action="store_true")
    parser.add_argument("-lr", "--list-rules", help="Get the list of rules for specific services.")
    # parser.add_argument("-o", "--output", help="Result will be return in form of excel or json. Default is excel.")
    
    logger = get_logger()
    configure = Configure(logger)
    configure.verify_configuration_file()
    
    args = parser.parse_args()
    
    default_regions = {}
    default_services = {}
    output_format = "excel"
    # valid_output = ['json', 'excel']
    
    try: 
        if args.version:
            print(f"Version - {__version__}")
            return

        if args.regions:
            regions_list = (args.regions).split(",")
            if all(region in all_regions for region in regions_list):
                default_regions = regions_list
            else:
                raise BaseException("Invalid list of regions passed.")

        # if args.output:
        #     if args.output in valid_output:
        #         output_format = args.output
        #     else:
        #         raise BaseException("Please provide valid output format.")
                
        if args.services:
            service_list = (args.services).split(",")
            if all(service in services for service in service_list):
                for service in service_list:
                    default_services[service] = services[service]
            else:
                raise BaseException("Invalid list of services passed.")

        if args.configure:            
            configure.set_configuartion()
            return

        if args.list_services:
            print('-'*25)
            print('| {:<21} |'.format('Available Services'))
            print('-'*25)
            for service in sorted(services.keys()):
                print('| {:<21} |'.format(service))
                print('-'*25)
            return
        
        if args.list_rules:
            service_list = (args.list_rules).split(",")
            print('-'*150)
            print('| {:<21} | {:<20} | {:<100} |'.format('Service', 'Rule ID', 'Rule'))
            print('-'*150)
            for service in service_list:
                i = 0
                for rule in services[service]:
                    if i == 0:
                        print('| {:<21} | {:<20} | {:<100} |'.format(service, rule['id'], rule['issue']))
                    else:
                        print('| {:<21} | {:<20} | {:<100} |'.format("", rule['id'], rule['issue']))
                    print('-'*150)
                    i = i + 1
            return
                
    except BaseException as e:
        logger.error('Error while parsing parameters. %s', e)
        return {
            "status": 'failure',
            "message": e
        }

    if not configure.is_configuration_done():
        print('Please configure the AWS Access Key ID and Secret Access Key.')
        print('Run "awsaudit --configure" command to do configuration')
        return
    else:
        configuration = configure.get_configuration()
        config = {
            'aws_access_key_id': configuration['AWS_ACCESS_KEY_ID'],
            'aws_secret_access_key': configuration['AWS_SECRET_ACCESS_KEY']
        }
        
    InitializePlugin  = Initialize(config, default_services, default_regions, logger)
    result = InitializePlugin.service()     
    
    OutputFormat = Output(result)
    if output_format == 'excel':
        logger.info('Converting output in excel format...')
        file_path = OutputFormat.convert_to_excel()
    # if output_format == 'json':
    #     logger.info('Converting output in json format...')
    #     file_path = OutputFormat.convert_to_json()
    # if output_format == 'pdf':
    #     logger.info('Converting output in pdf format...')
    #     file_path = OutputFormat.convert_to_pdf()
    
    print(f'Output file saved : {file_path}')

