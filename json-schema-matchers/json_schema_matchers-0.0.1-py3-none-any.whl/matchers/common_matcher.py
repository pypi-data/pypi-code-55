from hamcrest.core.base_matcher import BaseMatcher
from jsonschema import Draft7Validator, exceptions


class MatchesJsonSchema(BaseMatcher):

    def __init__(self, json_schema: dict):
        self.json_schema = json_schema

    def _matches(self, instance):
        try:
            Draft7Validator(self.json_schema).validate(instance)
            return True
        except exceptions.ValidationError as error:
            self.error = error
            return False

    def describe_to(self, description):
        title = f' "{self.json_schema.get("title", "")}"'
        description.append_text(f'\n     JSON object should match schema{title}')

    def describe_mismatch(self, item, mismatch_description):
        mismatch_description.append_text(f'\n     there was a mismatch: \n{self.error}"')


def matches_json_schema(json_schema: dict):
    return MatchesJsonSchema(json_schema)
