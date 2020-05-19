"""RuleDirectoryManager tests."""
from mc_nag.base_utils.models.rule import BaseRule
from mc_nag.base_utils.models.rule_directory import RuleDirectoryManager

STD_RULES_DIR = 'tests/rules/standard'
CUSTOM_RULES_DIR = 'tests/rules/custom'


def test_initilize_rule_dirs():
    """Initialized the RuleDirectoryManager successfully."""
    rule_dir_mngr = RuleDirectoryManager(True, STD_RULES_DIR, None)
    assert isinstance(rule_dir_mngr, RuleDirectoryManager)
    assert not isinstance(rule_dir_mngr, BaseRule)


def test_standard_rule_dirs():
    """Initialized the standard rules successfully."""
    rule_dir_mngr = RuleDirectoryManager(True, STD_RULES_DIR, None)
    assert len(rule_dir_mngr.rule_directories()) == 1
    assert not None in rule_dir_mngr.rule_directories()


def test_standard_and_custom_rule_dirs():
    """Initialized standard and custom rules successfully."""
    rule_dir_mngr = RuleDirectoryManager(True, STD_RULES_DIR, CUSTOM_RULES_DIR)
    assert len(rule_dir_mngr.rule_directories()) == 2


def test_only_custom_rule_dirs():
    """Initialized standard and custom rules successfully."""
    rule_dir_mngr = RuleDirectoryManager(False, None, CUSTOM_RULES_DIR)
    assert len(rule_dir_mngr.rule_directories()) == 1
    assert rule_dir_mngr.rule_directories().pop() == CUSTOM_RULES_DIR


def test_adding_list_to_rule_dirs():
    """Rule Manager supports passing in lists of directories."""
    THREE_CUSTOM_DIRS = ["custom1/", "custom2/", "custom3/"]
    rule_dir_mngr = RuleDirectoryManager(False, None, THREE_CUSTOM_DIRS)
    assert len(rule_dir_mngr.rule_directories()) == 3
    assert rule_dir_mngr.rule_directories()[0] == "custom1/"
