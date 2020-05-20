from mongoengine import (
    StringField,
    BooleanField,
    Document
)


class FeatureFlag(Document):
    feature_flag = StringField(unique=True)
    feature_flag_value = BooleanField(default=False)

    meta = {'strict': True}
