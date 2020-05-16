import os
import re
import pandas as pd
import json
import requests
import logging
from progress.bar import ShadyBar
from FileUtils import FileUtils as fru
from JSONUtils import JSONUtils as jru
from PandasUtils import PandasUtils as pru
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

# ALM connector URL
connector_url = 'http://almconnector:8080'
server_url = ''

alm_domain = None
alm_project = None

username = None
password = None

tp_parent_folder_id = '1'

# test plan folder creation params
alm_user_name = None
alm_password = None
test_plan_folder_id = None
test_parent_folder_id = None
test_name = None


def automation_framework_folder_creation(project_dir, project_name, host_name):
    logger.debug('****************************************************************************************************')
    logger.debug('Create automation test suite with default robot test case')
    logger.debug('****************************************************************************************************')

    # Create folders based on standard template
    os.mkdir(project_dir + project_name)
    folder_list = ['/data/Test_Inputs', '/results/actual_results', '/results/expected_results',
                   '/results/comparison_results', '/scripts', '/testcases']
    logger.info('  Automation Test Folder Creation In Progress ....')

    # Iterate through folder list and create required folders
    for item in folder_list:
        path = project_dir + project_name + item
        try:
            os.makedirs(path)
        except OSError:
            logger.info('Unable to create automation directories')

        # Create the standard robot regression test suite
        if re.search(r'testcases', item):
            file_path = path + '/' + project_name + '_Regression.robot'
            f = open(file_path, 'w+')
            f.write(automation_test_case_creation(project_name))
            f.close()

        # Create the script folder and suite_common_library/global_variables.py files
        if re.search(r'scripts', item):
            file_path = path + '/' + 'suite_common_library.py'
            f = open(file_path, 'w+')
            f.write(automation_suite_common_script_creation(project_name))
            f.close()

            file_path = path + '/' + 'global_variables.py'
            f = open(file_path, 'w+')
            f.write(automation_global_variables_creation(project_name, host_name))
            f.close()

    # Create the standard execution trigger script
    file_path = project_dir + project_name + '/' + 'results' + '/' + 'Trigger_Execution.bat'
    f = open(file_path, 'w+')
    content = r'robot -d . ' + project_dir + project_name + r'\\testcases\\' + project_name + '_Regression.robot'
    f.write(content)
    f.close()

    logger.info('  Automation Test Folder Created Successfully !!!!')
    logger.debug('****************************************************************************************************')


def automation_test_case_creation(project_name):

    # Standard template robot test case
    content = """*** Settings ***
Suite Setup     Create and execute test cases dynamically using API data sheet    ${test_data_full_path}
Library         Collections
Library         RequestsProLibrary/DynamicTestCases.py
Library         RequestsProLibrary
Library         ${CURDIR}${/}..${/}scripts${/}suite_common_library.py
Variables       ${CURDIR}${/}..${/}scripts${/}global_variables.py
Suite Teardown    Delete All Sessions

*** Variables ***
${Base_ENV_URL}    QA
${test_data_full_path}    ${CURDIR}${/}..${/}data${/}Test_Inputs${/}project_name_api_test_data.csv
${test_data_full_path}    ${CURDIR}${/}..${/}data${/}Test_Inputs${/}project_name_api_test_data_UAT.csv
${test_data_full_path}    ${CURDIR}${/}..${/}data${/}Test_Inputs${/}project_name_api_test_data_QA.csv

${actual_results_path}    ${CURDIR}${/}..${/}results${/}actual_results${/}
${expected_results_path}    ${CURDIR}${/}..${/}results${/}expected_results${/}
${test_input_path}    ${CURDIR}${/}..${/}data${/}Test_Inputs${/}
${comparison_results_path}    ${CURDIR}${/}..${/}results${/}comparison_results${/}

*** Test Cases ***
Placeholder Test
    [Tags]    exclude
    Log    ${test_data_full_path}
    Log    Placeholder test required by Robot Framework

*** Keywords ***
Generate and compare expected/actual results
    [Arguments]    ${api_name}
    Generate Actual Results    ${test_data_full_path}    ${api_name}    ${actual_results_path}    ${test_input_path}    ${Base_ENV_URL}
    Generate Expected Results    ${test_data_full_path}    ${api_name}    ${expected_results_path}
    Generate Actual Results    ${test_data_full_path}    ${api_name}    ${expected_results_path}    ${actual_results_path}    ${comparison_results_path}
    
Create and execute test cases dynamically using API data sheet
    [Arguments]    ${test_data_full_path}
    Set Log Level    INFO
    Log    ${test_data_full_path}
    Log    Get the list of test cases to be executed
    ${test_cases_list}=    API Test Cases List    ${test_data_full_path}
    ${no_of_test_cases}=    Get Length    ${test_cases_list}
    Log    Iterate through each test case and execute the test case
    FOR    ${i}    IN RANGE    ${no_of_test_cases}
        ${name}=    Get From Dictionary    ${test_cases_list}[${i}]    Test_Name
        ${tags}=    Get From Dictionary    ${test_cases_list}[${i}]    Test_Tags
        ${doc}=    Get From Dictionary    ${test_cases_list}[${i}]    Test_Documentation
        Add Test Case    ${name}    ${doc}    ${tags}    Generate and compare expected/actual results    ${name}
    END

"""
    content = content.replace('project_name', project_name)
    return content


def automation_suite_common_script_creation(project_name):

    # Standard template robot test case
    content = """from RequestsProLibrary import RequestsProKeywords
from robot.api.deco import keyword
from FileUtils import FileUtils as fru
from PandasUtils import PandasUtils as pru
import sys
import os
import logging
import pandas as pd
import global_variables as gl

sys.path.append(os.path.pardir + r'\\\\scripts\\\\')

# get logger from automation execution
logger = logging.getLogger('project_name.api_execution_log')


@keyword('Generate Actual Results')
def generate_actual_results(test_data_full_path, test_name, actual_results_path, test_input_path, base_env_url):
    logger.info('****************************************************************************************************')
    logger.info('Generate Actual Results for the test - ' + test_name)
    logger.info('****************************************************************************************************')
    logger.info('Step-01 : Start - Read and filter test data file based on Test_Name')
    test_cases_df = pd.read_csv(test_data_full_path)
    selected_api_df = test_cases_df.loc[test_cases_df['Test_Name'] == test_name].copy()
    selected_api_df = selected_api_df.loc[selected_api_df['TBE'] == 'YES'].reset_index()
    logger.info('Step-01 : End   - Read and filter test data file based on Test_Name')

    logger.info('Step-02 : Start - Determine the base environment url and trigger the test')
    expected_env_url = ''

    # condition to check if base_env_url is provided globally to override base_env_url from test data sheet
    logger.debug(base_env_url)
    if not base_env_url:
        execution_env = str(selected_api_df['Base_ENV_URL'][0])
    else:
        execution_env = base_env_url

    # Based on execution_env identify the server details from global variables and assign to expected_env_url
    if execution_env == 'DEV':
        expected_env_url = gl.dev_server_name
    elif execution_env == 'QA':
        expected_env_url = gl.qa_server_name
    elif execution_env == 'UAT':
        expected_env_url = gl.uat_server_name
    elif execution_env == 'PROD':
        expected_env_url = gl.prod_server_name

    # Based on the test type trigger the test, if Test_Type is API trigger the API to extract the response
    rl = RequestsProKeywords()
    selected_api_df = rl.trigger_api(test_data_full_path, test_input_path, test_name, expected_env_url)
    logger.info('Step-02 : End   - Determine the base environment url and trigger the test')

    logger.info('Step-03 : Start - Based on response validation flag generate the actual results')
    response_validation = str(selected_api_df['Response_Validation'][0])

    # delete and create new actual results folder for the test
    fru.delete_and_create_dir(actual_results_path + test_name)

    actual_results_df = pd.DataFrame([])
    logger.debug(test_name.lower())
    actual_results_df = selected_api_df.filter(
        ['Test_Name', 'API_Response_Code', 'API_Response_Content']).copy()
    pru.write_df_to_csv(actual_results_df, actual_results_path + test_name + '/', test_name + '.csv')

    # if response_validation is YES perform detailed validation else check for 200 status code
    if (response_validation == 'YES') or (response_validation == 'PREDEFINED'):
        logger.debug(test_name.lower())
        api_response_data = selected_api_df['API_Response_Content'][0]
    logger.info('Step-03 : End   - Based on response validation flag generate the actual results')
    logger.info('****************************************************************************************************')
    return actual_results_df

"""
    content = content.replace('project_name', project_name)
    return content


def automation_global_variables_creation(project_name, host_name):

    # Standard template robot test case
    content = """import os
# Assign path variables
root_dir = os.path.split(os.path.abspath(''))[0]

# Environment Variables
dev_server_name = 'host_name'
qa_server_name = 'host_name'
uat_server_name = 'host_name'
prod_server_name = 'host_name'

"""
    content = content.replace('project_name', project_name)
    content = content.replace('host_name', host_name)
    # content = content.replace('port_no', port_no)
    return content


def create_alm_test_folder(**kwargs):
    logger.debug('****************************************************************************************************')
    logger.debug('Create ALM Project Folders')
    logger.debug('****************************************************************************************************')

    logger.info('  ALM Project Folder Creation In Progress ....')
    global test_plan_folder_name

    # test plan folder creation params
    create_tp_folder_request_body = {
        "url": server_url,
        "domain": alm_domain,
        "project": alm_project,
        "username": alm_user_name,
        "password": alm_password,
        "folderid": tp_parent_folder_id,
        "user01": alm_user_name,
        "name": test_plan_folder_name,
    }

    # sending get request and saving the response as response object
    r = requests.post(url=connector_url + 'testfolder/', json=create_tp_folder_request_body)

    # convert the json response to string
    json_string = str(r.content.decode('utf-8'))

    # deserialize json_string to python object
    api_json_response_data = json.loads(json_string)

    api_response_df = jru.convert_json_to_data_frame(api_json_response_data)
    logger.debug(api_response_df)
    logger.debug('****************************************************************************************************')

    return api_json_response_data['id']


def create_alm_tests(**kwargs):

    global test_name

    # test plan folder creation params
    create_tp_tests_request_body = {
        "url": server_url,
        "domain": alm_domain,
        "project": alm_project,
        "username": alm_user_name,
        "password": alm_password,
        "folderid": tp_parent_folder_id,
        "user01": alm_user_name,
        "name": test_name,
        "steps": [
            {"name": "steps", "values":[{"value":"0"}]}],
        "custom": [
            {"name": "user-01", "value": "1 - High"},
            {"name": "user-07", "value": "1 - High"},
            {"name": "user-09", "value": "Automated"},
            {"name": "user-10", "value": "Robot"},
            {"name": "status", "value": "Design"},
            {"name": "owner", "value": alm_user_name},
        ],
    }

    # sending get request and saving the response as response object
    r = requests.post(url=connector_url + 'tests/', json=create_tp_tests_request_body)

    logger.debug(str(r.content))


def generate_api_test_data_using_swagger(url=None, project_dir=None, project_name=None, **kwargs):

    logger.debug('****************************************************************************************************')
    logger.debug('Create automation test data sheet using application swagger url')
    logger.debug('****************************************************************************************************')

    # extract the swagger json definition using the url
    response = requests.get(url, verify=False)
    swagger_json_data = response.json()
    logger.info('  Automation test data creation in progress ....')

    # define test data df and columns required for test data sheet
    test_data_df = pd.DataFrame(columns=['TBE', 'Test_Suite_Name', 'Test_Name', 'Test_Documentation', 'Test_Tags',
                                         'Test_Type', 'Request_Type', 'URI'])

    # define df to hold parameters for each api
    parameter_df = pd.DataFrame([])

    # extract the api definition from the swagger json data

    # extract the base path of the api definition
    base_path = swagger_json_data['basePath']

    bar1 = ShadyBar(r'Automation Test Data Creation In Progress', suffix='%(percent)d%%')

    # iterate and extract api details
    for (k, v) in swagger_json_data['paths'].items():

        # temp df to store the api details
        test_data_tmp_df = pd.DataFrame(columns=['TBE', 'Test_Suite_Name', 'Test_Name', 'Test_Documentation', 'Test_Tags',
                                             'Test_Type', 'Request_Type', 'URI'])

        # temp df to store the parameter details
        parameter_tmp_df = pd.DataFrame([])

        if type(v) is dict:
            for(k1, v1) in v.items():
                test_data_tmp_df['Test_Suite_Name'] = v1['tags']
                test_data_tmp_df['Test_Name'] = v1['operationId']

                # check if summary is blank and assign value as test documentation
                if 'summary' in v1:
                    test_data_tmp_df['Test_Documentation'] = v1['summary']

                test_data_tmp_df['TBE'] = 'NO'
                test_data_tmp_df['Response_Validation'] = 'NO'
                test_data_tmp_df['Test_Type'] = 'API'
                test_data_tmp_df['Request_Type'] = k1.upper()
                test_data_tmp_df['URI'] = base_path + k
                test_data_tmp_df['data'] = ''
                test_data_tmp_df['auth'] = ''
                test_data_tmp_df['headers'] = ''
                test_data_tmp_df['files'] = ''

                # check parameters and assign values for each api
                if 'parameters' in v1:
                    parameter_tmp_df = pd.DataFrame(v1['parameters'])
                    parameter_tmp_df['Test_Name'] = v1['operationId']

                    for i, row in parameter_tmp_df.iterrows():
                        parameter_name = row['name'] + '_d'

                        if 'x-example' in parameter_tmp_df.columns:
                            test_data_tmp_df[parameter_name] = row['x-example']
                        else:
                            test_data_tmp_df[parameter_name] = ''

                    if parameter_df.empty:
                        parameter_df = parameter_tmp_df.copy()
                    else:
                        parameter_df = parameter_df.append(parameter_tmp_df, ignore_index=True, sort=False)

        if test_data_df.empty:
            test_data_df = test_data_tmp_df.copy()
        else:
            test_data_df = test_data_df.append(test_data_tmp_df, ignore_index=True, sort=False)

        bar1.next()

    bar1.finish()

    pru.write_df_to_csv(test_data_df, project_dir + project_name + '/data/Test_Inputs/',
                        project_name + '_api_test_data.csv')
    pru.write_df_to_csv(parameter_df, project_dir + project_name + '/data/Test_Inputs/',
                        project_name + '_all_parameters.csv')

    parameter_df = parameter_df[['Test_Name', 'name', 'description', 'required', 'type']]
    pru.write_df_to_csv(parameter_df, project_dir + project_name + '/data/Test_Inputs/',
                        project_name + '_parameters_key_details.csv')

    # logger.info(test_data_df)
    # logger.info(parameter_df)




