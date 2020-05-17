"""
    OracleSaaSApiPy - utils.py

    Contains common functions
"""

# utils.py
import base64
import os
import xml.etree.ElementTree as ET

from .constants import UCM_ACCOUNTS, JOBS, UCM_SECURITY_GROUPS


def b64_encode(file):
    """code the file content to base 64"""
    return base64.b64encode(open(file, 'rb').read()).decode("UTF-8")


def get_filename_extension(file):
    """return the filename and the extension from the file"""
    base_name = os.path.basename(file)
    return base_name, base_name.split('.')[-1].lower()


def decode_multipart_response(response):
    """Decode multipart response
    parses the repsonse and puts the XML and binary content into an list

    Args:
        response (request.response): HTTP response

    Returns:
        list: list of parsed mime multipart
    """
    body_parts = []

    # throw exception here
    if b'\r\n\r\n' not in response.content:
        body_parts.append(response.content)
        return body_parts

    content_type = response.headers.get('content-type', None)
    content_types = [c.strip() for c in content_type.split(';')]

    for ct in content_types:
        eq_found = ct.find('=')
        attr, val = ct[:eq_found], ct[eq_found + 1:]
        if attr == 'boundary':
            boundary = val.strip('"')
            break
    boundary = bytes(boundary, 'utf-8')
    boundary = b''.join((b'\r\n--', boundary))

    parts = response.content.split(boundary)

    for part in parts:
        p = part.split(b'\r\n\r\n')
        if len(p) > 1:
            body_parts.append(p[1])

    return body_parts


def parse_xml_nodes(xml_root, nodes_to_select):
    """Parse XML nodes with the nodes specified and returns them as
    a dictionary

    Args:
        xml_root (XML root): XML root
        nodes_to_select (list): list of nodes to be parsed

    Returns:
        dict: key value pair of the of the XML nodes
    """
    node_values = {}
    for elem in xml_root.iter():
        # if the XML tag contains namespace.
        # TODO: if they do not contain then handle the case
        elem_tag = elem.tag.rpartition('}')[2]
        if elem_tag in nodes_to_select:
            node_values[elem_tag] = elem.text
    return node_values


def format_ucm_account(account):
    """formats the UCM account as per the standard.
    The valid format `abc/def/xyz` or `abc$/def$/xyz$`

    Args:
        account (str): account name

    Returns:
        str: formatted UCM account name

    Raises:
        ValueError: If the account name passed in incorrect
    """
    if account:
        if account.find('$') == -1:
            account = '$/'.join(account.split('/')) + '$'

    return account


def validate_func_arguments(param_value, validation_check):
    """ validates the input parmaters to the functiton"""

    # if the param_value is None, we dont want to validate, return
    if not param_value:
        return

    # check if the file exists
    if validation_check == 'CheckFileExists':
        try:
            open(param_value, 'r').close()
        except FileNotFoundError:
            raise FileNotFoundError(f'No such file found: {param_value}')

    # check if the job name is valid based on the list
    elif validation_check == 'JobNameValid':
        try:
            JOBS[param_value]
        except KeyError:
            raise ValueError(f'The process name is not valid: {param_value}')

    # check if a string contains only digit - this validation is for
    # the request ID, doc ID etc.
    elif validation_check == 'ContainsOnlyDigit':
        # if the argument value is not string return
        if not isinstance(param_value, str):
            return

        if not param_value.isdigit():
            raise ValueError(f'Request ID {param_value} should only contains numbers')

    # check if a diretory exists, if not create it
    elif validation_check == 'DirectoryExists':
        try:
            os.mkdirs(param_value)
        except OSError:
            os.mkdirs(param_value)

    # check if the UCM Security Group exists
    elif validation_check == 'UCMSecurityGroupValid':
        if param_value.lower() not in UCM_SECURITY_GROUPS:
            raise ValueError(f'Security Group is not valid: {param_value}')

    elif validation_check == 'UCMAccountValid':
        if param_value.lower() not in UCM_ACCOUNTS:
            raise ValueError(f'''{param_value} is not a valid UCM Account.''')

    # check if the XML payload is valid
    elif validation_check == 'XMLPayloadValid':
        if isinstance(param_value, str):
            try:
                ET.fromstring(param_value)
            except ET.ParseError:
                raise ValueError('XML Payload is not a valid')

    # the validation critiria does not exists
    else:
        # superflous
        return
