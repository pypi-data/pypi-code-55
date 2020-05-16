from marshmallow import (
    Schema,
    fields,
    validate,
)


class DrugLabelResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    spl_id = fields.String(validate=not_blank, required=True)
    set_id = fields.String(validate=not_blank, required=True)
    indication_text = fields.String(allow_none=True)
    updated_at = fields.DateTime()


class DrugLabelQueryParamsSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer()
    spl_id = fields.String(validate=not_blank)
    set_id = fields.String(validate=not_blank)


class DrugLabelPatchSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    spl_id = fields.String(validate=not_blank)
    set_id = fields.String(validate=not_blank)
    indication_text = fields.String(allow_none=True)
