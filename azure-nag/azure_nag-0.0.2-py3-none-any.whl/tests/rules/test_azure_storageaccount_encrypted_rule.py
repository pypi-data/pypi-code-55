"""Tests for azure_storageaccount_encrypted_rule.py."""

from mc_nag.base_utils import read_template_file
from azure_nag.models.azure_template import AzureTemplate
from azure_nag.rules.azure_storageaccount_encrypted_rule import (
    AzureStorageAccountEncryptedRule
)

TEMPLATE_PATH = 'tests/templates'


def evaluate_rule(template_path):
    """Evaluate current rule and return output."""
    template_model = AzureTemplate(template_path)
    rule_object = AzureStorageAccountEncryptedRule(template_model)
    return rule_object.evaluate()


def test_encrypted_storageaccount():
    """Happy Path: Ensure rule does not return any resources."""
    test_file = f'{TEMPLATE_PATH}/azure_storageAccounts/' + \
                'valid_storageAccounts.json'
    violating_resources = evaluate_rule(test_file)
    assert not violating_resources


def test_storageaccount_no_encryption():
    """Sad Path: Ensure rule returns violating resources."""
    test_file = f'{TEMPLATE_PATH}/azure_storageAccounts/' + \
                'invalid_storageAccounts_without_encryption.json'
    violating_resources = evaluate_rule(test_file)

    assert len(violating_resources) == 1
    assert violating_resources[0].resource_name == 'insecurestorageaccount'


def test_storageaccount_encryption_service_disabled():
    """Sad Path: Ensure rule returns violating resources."""
    test_file = f'{TEMPLATE_PATH}/azure_storageAccounts/' + \
                'invalid_storageAccounts_encryption_services_disabled.json'
    violating_resources = evaluate_rule(test_file)

    assert len(violating_resources) == 1
    assert violating_resources[0].resource_name == 'insecurestorageaccount'


def test_storageaccount_encryption_missing_keysource():
    """Sad Path: Ensure rule returns violating resources."""
    test_file = f'{TEMPLATE_PATH}/azure_storageAccounts/' + \
                'invalid_storageAccounts_encryption_missing_keysource.json'
    violating_resources = evaluate_rule(test_file)

    assert len(violating_resources) == 1
    assert violating_resources[0].resource_name == 'insecurestorageaccount'
