import logging
from . import ai_test_designer_library as ailib
import re
import getpass


def main():

    # Define logging
    # Create logger definition
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Create file handler which logs messages in log file
    fh = logging.FileHandler(__name__)
    fh.setLevel(logging.DEBUG)

    # Create console handler with high level log messages in console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(ch)
    # logger.addHandler(fh)

    logger.info('****************************************************************************************************')
    logger.info('Cognitive Quality Engineering Platform - Intelligent Test Designer (ITD)')
    logger.info('****************************************************************************************************')

    # get user details
    ailib.username = getpass.getuser()
    ailib.alm_user_name = getpass.getuser()
    logger.info('                        Welcome  !!!  ' + ailib.username + '  !!!                                    ')

    # get the folder path to create test suite based on template
    logger.info(r'Enter below information to create/update automation and manual test cases')
    project_dir = input('{}{}{} '.format('Automation Directory', '\t', ':'))
    project_name = input('{}{}{} '.format('Application Name', '\t', ':'))
    create_tc = input('{}{}{} '.format('Do you want to create test cases in ALM (Y/N)', '\t', ':'))

    if create_tc == 'Y':

        ailib.alm_domain = input('{}{}{} '.format('ALM Domain Name', '\t', ':'))
        ailib.alm_project = input('{}{}{} '.format('ALM Project Name', '\t', ':'))
        ailib.alm_user_name = input('{}{}{} '.format('ALM User Name', '\t', ':'))
        ailib.alm_password = input('{}{}{} '.format('ALM User Password', '\t', ':'))

    suite_type = input('{}{}{} '.format('Do you want to create API automation test suite (Y/N)', '\t', ':'))

    if suite_type == 'Y':

        swagger_url = input('{}{}{} '.format('Swagger URL', '\t', ':'))
        http_https = re.search("(.*?)://", swagger_url).group(1)
        server_name = re.search("://(.*?)/", swagger_url).group(1)
        host_name = http_https + '://' + server_name
        logger.debug(host_name)
        # if host_name.find(':') > 0:
        #     port_no_tmp = host_name.split(':')
        #     port_no = port_no_tmp[1]
        # else:
        #     port_no = None
        # logger.info(port_no)

    logger.info('****************************************************************************************************')
    logger.info('Building Automation Test Suite Using Swagger URL')
    logger.info('****************************************************************************************************')

    ailib.automation_framework_folder_creation(project_dir, project_name, host_name)

    if create_tc == 'Y':
        ailib.automation_test_case_creation(project_name)

    if suite_type == 'Y':
        ailib.generate_api_test_data_using_swagger(str(swagger_url), project_dir, project_name)
    logger.info('****************************************************************************************************')





