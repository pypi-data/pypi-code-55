from uuid import uuid4

import pytest

from rule_engine.error import RequiredFieldsMissing
from rule_engine.operator import In, Equals
from rule_engine.rule import RuleSet, Rule


def test_no_rule():
    rule_set = RuleSet([])
    assert rule_set.evaluate({})


def test_single_rule():
    origin_cluster_id = uuid4()
    destination_cluster_id = uuid4()
    rule_set = RuleSet(
        [
            Rule(
                "slot.od_cluster",
                In(),
                [(origin_cluster_id, destination_cluster_id), (uuid4(), uuid4())],
            )
        ]
    )
    result = rule_set.evaluate(
        {"slot.od_cluster": (origin_cluster_id, destination_cluster_id)}
    )

    assert result


def test_multiple_rules_both_passing():
    origin_cluster_id = uuid4()
    destination_cluster_id = uuid4()
    rule_set = RuleSet(
        [
            Rule(
                "slot.od_cluster",
                In(),
                [(origin_cluster_id, destination_cluster_id), (uuid4(), uuid4())],
            ),
            Rule("slot.session", Equals(), "MORNING"),
        ]
    )
    result = rule_set.evaluate(
        {
            "slot.od_cluster": (origin_cluster_id, destination_cluster_id),
            "slot.session": "MORNING",
        }
    )

    assert result


def test_multiple_rules_one_failing():
    origin_cluster_id = uuid4()
    destination_cluster_id = uuid4()
    rule_set = RuleSet(
        [
            Rule(
                "slot.od_cluster",
                In(),
                [(origin_cluster_id, destination_cluster_id), (uuid4(), uuid4())],
            ),
            Rule("slot.session", Equals(), "MORNING"),
        ]
    )
    result = rule_set.evaluate(
        {
            "slot.od_cluster": (origin_cluster_id, destination_cluster_id),
            "slot.session": "EVENING",
        }
    )

    assert not result


def test_multiple_rules_context_key_missing():
    origin_cluster_id = uuid4()
    destination_cluster_id = uuid4()
    rule_set = RuleSet(
        [
            Rule(
                "slot.od_cluster",
                In(),
                [(origin_cluster_id, destination_cluster_id), (uuid4(), uuid4())],
            ),
            Rule("slot.session", Equals(), "MORNING"),
        ]
    )
    with pytest.raises(RequiredFieldsMissing):
        result = rule_set.evaluate(
            {"slot.od_cluster": (origin_cluster_id, destination_cluster_id)}
        )
