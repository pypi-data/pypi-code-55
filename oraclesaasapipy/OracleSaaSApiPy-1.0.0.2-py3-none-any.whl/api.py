"""
    ERP Integration Service Wrapper
"""

__all__ = ['ErpServiceApi', 'ErpServiceApiResponse']

import logging
import requests
import xml.etree.ElementTree as ET

from functools import wraps
from os.path import join as path_join
from xml.etree.ElementTree import Element, SubElement, tostring

from . import utils
from .constants import UCM_ACCOUNTS, JOBS, UCM_SECURITY_GROUPS


# logging here
erp_logger = logging.getLogger(__name__)
erp_logger.setLevel(logging.NOTSET)
log_handler = logging.FileHandler('erp_api.log')
log_handler.setLevel(logging.NOTSET)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(funcName)s: %(message)s')
log_handler.setFormatter(formatter)
erp_logger.addHandler(log_handler)


# log decorator
def log_decorator(func):
    """ decorator to capture logging and exceptions """
    @wraps(func)
    # Use functools.wrap to preserve the function signatures
    def log_wrapper(*args, **kwargs):
        erp_logger.debug(f'Entering {func.__qualname__}, {args}, {kwargs}')
        try:
            out = func(*args, **kwargs)
            erp_logger.debug(f'<!!OUTPUT!! for {func.__qualname__}> {out}')
        except Exception as ex:
            erp_logger.exception(
                f'exception caught in {func.__qualname__}: {ex}')
            raise ex
        erp_logger.debug(f'Exiting {func.__qualname__}')
        return out

    return log_wrapper


# Namespace attributes for the payloads
ns_attr = {
    'xmlns:soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
    'xmlns:typ': 'http://xmlns.oracle.com/apps/financials/commonModules/shared/model/erpIntegrationService/types/',
    'xmlns:erp': 'http://xmlns.oracle.com/apps/financials/commonModules/shared/model/erpIntegrationService/'
}

ns_attr2 = {
    'xmlns:soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
    'xmlns:typ': 'http://xmlns.oracle.com/apps/financials/commonModules/shared/model/erpIntegrationService/types/'
}


# Response class
class ErpServiceApiResponse:
    """ response class to capture the detials """

    def __init__(self, response, results, mime_parts):
        """
        Args:
            response (request.response): response object
            results (dict): dictinary of the result tags
            mime_parts (list): the mime_parts of the xml response
        """
        self.response = response
        self.success = response.ok
        self.results = results
        self.mime_parts = mime_parts
        self.value = None

    def __str__(self):
        """ string representation of the response object """
        return f'[Success] {self.success} [Results] {self.value}'


# Client Class
class ErpServiceApi:
    """This class is to automate the intergation servies"""

    def __init__(self, url, username, password, debug=False):
        """
        Args:
            url (str): server URL
            username (str): username
            password (str): password
            debug (bool, optional): debug option
        """
        self._url = url
        self._username = username
        self._password = password
        self.debug = debug

        self._validate_inputs()

        self.erp_url = self._url + '/fscmService/ErpIntegrationService?WSDL'

        if self.debug:
            erp_logger.setLevel(logging.DEBUG)

    @log_decorator
    def set_debug(self, value):
        """ set debug flag and enable the logger
        if True, the logging level would be set to DEBUG
        if False, the logging level would be set to ERROR.
        Args:
            value (Boolean): True or False
        """
        self.debug = value

        if value:
            erp_logger.info(f'Logging level set to DEBUG')
            erp_logger.setLevel(logging.DEBUG)
        else:
            erp_logger.info(f'Logging level set to ERROR')
            erp_logger.setLevel(logging.ERROR)

    @log_decorator
    def _validate_inputs(self):
        """ function to validate the inputs passed to the object """

        if not self._url:
            raise ValueError(f'The URL must be set.')

        if not self._username or not self._password:
            raise ValueError(f'The username and password must be set.')

        self._is_url_reachable()
        self._is_user_cred_valid()

    @log_decorator
    def _parse_fault_string(self, fault_str):
        """if the response of the request is unsuccessful, it returns a fault message.
        This function parses the fault message and extracts the error message
        number and text

        Args:
            fault_str (str): fault string from the XML

        Returns:
            TYPE: str
        """

        # fault string format
        # <faultstring>JBO-FND:::FND_CMN_SYS_ERR
        #   <MESSAGE>
        #       <NUMBER>FND-2</NUMBER>
        #       <TEXT>Error Message</TEXT>
        #       <CAUSE></CAUSE><ACTION></ACTION>
        #       <DETAILS></DETAILS><INCIDENT></INCIDENT>
        #   </MESSAGE>>
        # </faultstring>

        # find if the fault string contains error message XML
        if fault_str.find('<MESSAGE>') > -1:
            gt = fault_str.find('<MESSAGE>')
            # parse all string before first occurence of <
            err_code = fault_str[:gt].strip()

            # everything after < is the xml part
            part_xml = fault_str[gt:]

            # parse xml - first node of the xml part is error number
            # second part is error message
            erp_logger.debug(f'XML part for parsing {part_xml}')
            root = ET.ElementTree(ET.fromstring(part_xml)).getroot()
            msg_nbr = root[0].text
            msg_text = root[1].text

            fault_str = f'{err_code} | {msg_nbr} -> {msg_text}'

        return fault_str

    @log_decorator
    def _is_url_reachable(self):
        """check if the URL is valid.

        Raises:
            ValueError: if the url is invalid or network connection is down
        """

        try:
            requests.get(self._url)
        except (requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout):
            raise ValueError(f'Either the URL {self.erp_url} is invalid or you'
                             'are not connected to the internet.')

    @log_decorator
    def _is_user_cred_valid(self):
        """Validate the user credentials
        Use the BI Security Service to Check if the credentials are valid

        Raises:
            Exception: if the username and password are not correct
        """

        bi_url = self._url + '/xmlpserver/services/v2/SecurityService?WSDL'

        ns_attr = {
            'xmlns:soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
            'xmlns:v2': 'http://xmlns.oracle.com/oxp/service/v2'}

        # for the xml payload
        root = Element('soapenv:Envelope', attrib=ns_attr)
        SubElement(root, 'soapenv:Header')
        elem = SubElement(root, 'soapenv:Body')
        elem = SubElement(elem, 'v2:login')
        SubElement(elem, 'v2:userID').text = self._username
        SubElement(elem, 'v2:password').text = self._password

        payload = tostring(root, encoding='unicode')

        response = self._send_request('login', payload, url=bi_url,
                                      result_tags=['loginReturn'])

        if not response.success:
            raise Exception(f'Username/password are invalid. Please check.')

    @log_decorator
    def _send_request(self, soap_action, payload, url=None, result_tags=['result'], fault_tags=['faultstring']):
        """Summary

        Args:
            soap_action (str): Soap Action
            payload (str): XML payload
            url (str, optional): URL to submit. If URL is not passed,
            it will send the request to the ERP Integration Service
            result_tags (list, optional): list of tags to be extracted out of response xml
            fault_tags (list, optional): list of tags to be extract out of response xml, if failure occured

        Returns:
            ErpServiceApiResponse: ERP Service API Response

        Raises:
            ValueError: raises ValueError is payload or soap action is not passed
        """

        if not payload:
            raise ValueError(f'Payload is required')

        if not soap_action:
            raise ValueError(f'Soap Action is required')

        # this is a generic function to send HTTP POST request
        # in case you want to send a request to a diffrent URL, override the URL
        url = url or self.erp_url

        # make a post request
        response = self._request(url, soap_action, payload)

        # the response can be a multipart response with XML and the binary data
        parts = utils.decode_multipart_response(response)
        erp_logger.debug(f'mime parts {parts}')

        xml_response = parts[0].decode("utf-8")

        erp_logger.debug('xml response parsed from mime multipart {xml_response}')
        try:
            root = ET.ElementTree(ET.fromstring(xml_response)).getroot()
        except Exception:
            raise ValueError(f'XML Payload from multipart response not valid {xml_response}')

        tags = result_tags if response.ok else fault_tags
        results = utils.parse_xml_nodes(root, tags)

        return ErpServiceApiResponse(response, results, parts)

    @log_decorator
    def _request(self, url, soap_action, payload):
        """Summary

        Args:
            url (str): the URL for service request
            soap_action (str): Soap Action. This will get added to the request header
            payload (str): XML payload

        Returns:
            requests.response: request.response for the HTTP request

        Raises:
            Exception: If unable to reach the website, exception will be raised
            ValueError: If the XML paylaod is not valid
        """

        # check - can this be made generic to handle REST/JSon requests as well?

        utils.validate_func_arguments(payload, 'XMLPayloadValid')

        try:
            headers = {'SOAPAction': soap_action, 'Content-Type': 'text/xml'}
            http_auth = requests.auth.HTTPBasicAuth(self._username,
                                                    self._password)

            response = requests.post(url, auth=http_auth,
                                     headers=headers, data=payload)

            erp_logger.debug(f'Payload {payload}')
            erp_logger.debug(f'Response {response}')
            erp_logger.debug(f'response status {response.status_code}')

        except requests.exceptions.ConnectionError:
            # raise error if not able to connect to the server
            raise Exception(0, 'Host not reachable. Please check.')

        return response

    @log_decorator
    def upload_file_to_ucm(self, file_to_upload, account, security_group='FAFusionImportExport', include_author=False):
        """Uploads a file to the Universal Content Management server based on the document specified

        Args:
            file_to_upload (str): file to be updated. Requires full path
            account (str): UCM account
            security_group (str, optional): UCM Security group, will be defaulted to `FAFusionImportExport`
            include_author (bool, optional): Include author while uploading the file to UCM

        Returns:
            str: is success, returns the value the document ID for the uploaded file
            if failed, returns the message code and text of the fault string

        Raises:
            FileNotFoundError: Raises if the file to be uploaded is not found
            ValueError: Raises if the account number passed is not valid.
        """

        # validate if the file exists
        utils.validate_func_arguments(file_to_upload, 'CheckFileExists')
        utils.validate_func_arguments(security_group, 'UCMSecurityGroupValid')

        # if the UCM account does not have a $, append it
        # also this function validates if the account exists in a list
        # if not, throws an exception UCMAccountNotValid
        account = utils.format_ucm_account(account)
        utils.validate_func_arguments(account, 'UCMAccountValid')

        # get the filename and file extension from the filepath
        file_name, file_ext = utils.get_filename_extension(file_to_upload)

        # encode file to base64
        file_b64 = utils.b64_encode(file_to_upload)

        # for the xml payload
        root = Element('soapenv:Envelope', attrib=ns_attr)
        SubElement(root, 'soapenv:Header')
        elem = SubElement(root, 'soapenv:Body')
        elem = SubElement(elem, 'typ:uploadFileToUcm')
        document = SubElement(elem, 'typ:document')
        SubElement(document, 'erp:Content').text = file_b64
        SubElement(document, 'erp:FileName').text = file_name
        SubElement(document, 'erp:ContentType').text = file_ext
        SubElement(document, 'erp:DocumentTitle').text = file_name
        SubElement(document, 'erp:DocumentSecurityGroup').text = security_group
        SubElement(document, 'erp:DocumentAccount').text = account
        if include_author:
            SubElement(document, 'erp:DocumentAuthor').text = self._username

        payload = tostring(root, encoding='unicode')

        # once you get the resposne from the request, parse it here,
        # if error then throw exception with proper error message
        # if success, return the value expected.

        r = self._send_request('uploadFileToUcm', payload)

        if r.success:
            # only return the value of the docID
            r.value = r.results['result']
        else:
            # parse error message to return meaningful string
            r.value = self._parse_fault_string(r.results['faultstring'])

        return r

    @log_decorator
    def submit_ess_job_request(self, params_):
        """Submits an Scheduling job request for the specified job

        Args:
            params_ (dict): input which contains process definitation & proces parameters
            dict keys are jobPackageName, jobDefinitionName and params
            params is a tuple - so that the order of params is maintained

            Sample dict example:
            --------------------
            params = {
                'jobPackageName': 'oracle/apps/ess/financials/commonModules/shared/common/interfaceLoader',
                'jobDefinitionName': 'InterfaceLoaderController',
                'params': (param1, param2, param3)  #tuples need to be str
            }

        Returns:
            ErpServiceApiResponse: Object of ErpServiceApiResponse
        """

        # TODO: check for the params_ keys is exists if not return

        # for the xml payload
        root = Element('soapenv:Envelope', attrib=ns_attr2)
        SubElement(root, 'soapenv:Header')
        elem = SubElement(root, 'soapenv:Body')
        req = SubElement(elem, 'typ:submitESSJobRequest')
        SubElement(req, 'typ:jobPackageName').text = params_['jobPackageName']
        SubElement(req, 'typ:jobDefinitionName').text = params_['jobDefinitionName']

        for param in params_['params']:
            if not isinstance(param, str):
                # throw warning that we are converting it to string
                # this errors out while assigning value to node text
                param = str(param)
            SubElement(req, 'typ:paramList').text = param

        payload = tostring(root, encoding='unicode')

        return self._send_request('submitESSJobRequest', payload)

    @log_decorator
    def load_interface_file(self, job_name, doc_id):
        """Submits an `Load Interface File for Import` job for the specified job

        Args:
            job_name (str): The job name for which the load interface file needs
            to be processed
            doc_id (str): the ID for the document uploaded to the UCM Server

        Returns:
            str: if success, returns the request id of the submitted jon
            if failed, returns the fault string

        Raises:
            ValueError: Raises if the job name is not valid
        """

        # check fi the import process exists in our list
        utils.validate_func_arguments(job_name, 'JobNameValid')
        utils.validate_func_arguments(doc_id, 'ContainsOnlyDigit')

        # try:
        interface_id = JOBS[job_name]['interfaceId']
        # except KeyError:
        #     raise ValueError(f'The process name is not valid: {job_name}')

        if not isinstance(doc_id, str):
            doc_id = str(doc_id)

        params = {
            'jobPackageName': 'oracle/apps/ess/financials/commonModules/shared/common/interfaceLoader',
            'jobDefinitionName': 'InterfaceLoaderController',
            'params': (interface_id, doc_id, 'N', 'N')
        }

        r = self.submit_ess_job_request(params)

        if r.success:
            r.value = r.results['result']
        else:
            r.value = self._parse_fault_string(r.results['faultstring'])

        return r

    @log_decorator
    def process_interface_file(self, job_name, params):
        """Execute the import process for the specified job

        Args:
            job_name (str): scheduled process name
            params (tuple): Parameters passed to the job.
            Parameters for the job are to be passed as tuple, so the ordered
            is maintained.

            Sample value for params:
            params_ = tuple('300000012613562,N,SUBMIT,170420200653,null,Y')

        Returns:
            str: if success, returns the request id of the submitted job
            if failed, returns the error message

        Raises:
            ValueError: raise exception, if the job name is not valid
        """

        # validate arguments
        utils.validate_func_arguments(job_name, 'JobNameValid')

        # if a single value is passed in the tuple, python splits them up into
        # individual values. Add comma to the param.
        if not isinstance(params, tuple):
            params = (params,)

        params_ = {
            'jobPackageName': JOBS[job_name]['jobPackageName'],
            'jobDefinitionName': JOBS[job_name]['jobDefinitionName'],
            'params': params
        }

        r = self.submit_ess_job_request(params_)

        if r.success:
            # only return the value of the docID
            r.value = r.results['result']
        else:
            # parse error message to return meaningful string
            r.value = self._parse_fault_string(r.results['faultstring'])

        return r

    @log_decorator
    def get_ess_job_status(self, request_id):
        """Obtains the request status of the submitted scheduled job

        Args:
            request_id (str): process ID of the submitted job

        Returns:
            str: string: if success, returns the status of the submitted job
            If failed, returns the error message

        Raises:
            ValueError: if the request_id contains characters
        """

        # check if the request id only contains numbers and not characters
        utils.validate_func_arguments(request_id, 'ContainsOnlyDigit')

        # for the xml payload
        root = Element('soapenv:Envelope', attrib=ns_attr2)
        SubElement(root, 'soapenv:Header')
        elem = SubElement(root, 'soapenv:Body')
        status = SubElement(elem, 'typ:getESSJobStatus')
        SubElement(status, 'typ:requestId').text = request_id

        payload = tostring(root, encoding="unicode")

        r = self._send_request('getESSJobStatus', payload)

        if r.success:
            r.value = r.results['result']
        else:
            r.value = self._parse_fault_string(r.results['faultstring'])

        return r

    @log_decorator
    def load_and_import_data(self, file_to_upload, job_name, params_):
        """Uploads a file to the Oracle Universal Content Management server
        based on the document specified and submits the scheduled job to
        import and process the uploaded file.

        Args:
            file_to_upload (str): The file to be uploaded to Oracle UCM
            job_name (str): The job name to
            params_ (str): comman separated list of parameters to invoke the
            job. The order of the parameters is maintained per the list.

        Returns:
            string: the request ID of the import process submitted
            If failed, returns the error message

        Raises:
            ValueError: throws exception if the process name is not valid.
            FileNotFoundError: if file is not found
        """

        utils.validate_func_arguments(file_to_upload, 'CheckFileExists')
        utils.validate_func_arguments(job_name, 'JobNameValid')

        account = JOBS[job_name]['ucmAccount']
        job_name = ','.join((JOBS[job_name]['jobPackageName'],
                            JOBS[job_name]['jobDefinitionName']))
        interface_code = JOBS[job_name]['interfaceId']

        file_name, file_ext = utils.get_filename_extension(file_to_upload)

        security_group = 'FAFusionImportExport'

        # form the XML
        root = Element('soapenv:Envelope', attrib=ns_attr)
        SubElement(root, 'soapenv:Header')
        elem = SubElement(root, 'soapenv:Body')
        elem = SubElement(elem, 'typ:loadAndImportData')
        doc = SubElement(elem, 'typ:document')
        SubElement(doc, 'erp:Content').text = utils.b64_encode(file_to_upload)
        SubElement(doc, 'erp:FileName').text = file_name
        SubElement(doc, 'erp:ContentType').text = file_ext
        SubElement(doc, 'erp:DocumentTitle').text = file_name
        SubElement(doc, 'erp:DocumentSecurityGroup').text = security_group
        SubElement(doc, 'erp:DocumentAccount').text = account
        SubElement(doc, 'erp:DocumentAuthor').text = self._username
        job_list = SubElement(elem, 'typ:jobList')
        SubElement(job_list, 'erp:JobName').text = job_name
        SubElement(job_list, 'erp:ParameterList').text = params_
        SubElement(elem, 'typ:interfaceDetails').text = interface_code
        SubElement(elem, 'typ:notificationCode').text = '20'
        SubElement(elem, 'typ:callbackURL').text = ""

        payload = tostring(root, encoding="unicode")

        r = self._send_request('loadAndImportData', payload)

        if r.success:
            r.value = r.results['result']
        else:
            r.value = self._parse_fault_string(r.results['faultstring'])

        return r

    @log_decorator
    def download_ess_job_execution_details(self, request_id, file_type=None, file_path=None):
        """Downloads the output of Enterprise Scheduling Service job and logs

        Args:
            request_id (str): The request ID of the submitted job.
            fileType (str, optional): file type to download
            file_path (str, optional): local filepath to save the attachment

        Returns:
            string: if success, local path of the downloaded file.
            if failed, returns the errors message

        Raises:
            ValueError: If request_id contains characters
        """

        # TODO: validate the file type argument

        # validate input params
        utils.validate_func_arguments(request_id, 'ContainsOnlyDigit')
        utils.validate_func_arguments(file_path, 'DirectoryExists')

        root = Element('soapenv:Envelope', attrib=ns_attr2)
        SubElement(root, 'soapenv:Header')
        elem = SubElement(root, 'soapenv:Body')
        elem = SubElement(elem, 'typ:downloadESSJobExecutionDetails')
        SubElement(elem, 'typ:requestId').text = request_id
        SubElement(elem, 'typ:fileType').text = file_type

        payload = tostring(root, encoding="unicode")

        r = self._send_request('downloadESSJobExecutionDetails',
                               payload, result_tags=['DocumentName'])

        # if success, save the mime attachment to a local path
        # get the document name from the response and save it.
        if r.success:
            r.value = r.results['DocumentName']
            if file_path:
                save_file = path_join(file_path, r.value)
            else:
                save_file = r.value
            open(save_file, 'wb').write(r.mime_parts[1])
        else:
            # if failed return the fault string
            r.value = self._parse_fault_string(r.results['faultstring'])

        return r

    def get_jobs(self):
        """get the list of valid jobs currently configured"""

        # TODO: add jobs as well..
        return list(JOBS.keys())
