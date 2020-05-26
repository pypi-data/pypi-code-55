"""Tests for azure_storageaccount_encrypted_rule.py."""

from mc_nag.base_utils import read_template_file
from azure_nag.models.azure_template import AzureTemplate
from azure_nag.rules.azure_compute_disk_rule import (
    AzureComputeDiskEncryptedRule
)

TEMPLATE_PATH = 'tests/templates/azure_compute_disk'
PARAM_FILES_PATH = f'{TEMPLATE_PATH}/param_files'


def evaluate_rule(template_path, param_file_path=None):
    """Evaluate current rule and return output."""
    if param_file_path is None:
        template_model = AzureTemplate(template_path)
    else:
        template_model = AzureTemplate(template_path, param_file_path)
    rule_object = AzureComputeDiskEncryptedRule(template_model)
    return rule_object.evaluate()
#
#
def test_encrypted_azure_compute_disk_no_param_file():
    """Happy Path: Ensure rule does not return any resources."""
    test_file = f'{TEMPLATE_PATH}/' + \
                'valid_azure_compute_disk.json'
    violating_resources = evaluate_rule(test_file)
    assert not violating_resources

def test_encrypted_azure_compute_disk_with_param_file():
    """Happy Path: Ensure rule does not return any resources."""
    test_file = f'{TEMPLATE_PATH}/' + \
                'valid_azure_compute_disk.json'
    param_file = f'{PARAM_FILES_PATH}/' + \
                'valid_params_file.json'
    violating_resources = evaluate_rule(test_file, param_file)
    assert not violating_resources

def test_not_encrypted_azure_compute_disk_no_param_file():
    """Sad Path: Ensure rule returns violating resources."""
    test_file = f'{TEMPLATE_PATH}/' + \
                'violating_azure_compute_disk_1.json'
    violating_resources = evaluate_rule(test_file)
    assert len(violating_resources) == 1
    assert violating_resources[0].resource_name == 'azure-compute-disk'

def test_not_encrypted_azure_compute_disk_with_param_file():
    """Sad Path: Ensure rule returns violating resources."""
    test_file = f'{TEMPLATE_PATH}/' + \
                'violating_azure_compute_disk_1.json'
    param_file = f'{PARAM_FILES_PATH}/' + \
                 'violating_encryption_params_file.json'
    violating_resources = evaluate_rule(test_file, param_file)
    assert len(violating_resources) == 1
    assert violating_resources[0].resource_name == 'azure-compute-disk-param-test'

def test_azure_compute_disk_no_encryptionsettingscollection_property():
    """Sad Path: Ensure rule returns violating resources."""
    test_file = f'{TEMPLATE_PATH}/' + \
                'violating_azure_compute_disk_2.json'
    violating_resources = evaluate_rule(test_file)
    assert len(violating_resources) == 1
    assert violating_resources[0].resource_name == 'azure-compute-disk'
