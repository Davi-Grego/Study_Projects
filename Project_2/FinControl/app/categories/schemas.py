from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100, error="Nome deve ter entre 1 e 100 caracteres.")
    )
    icon = fields.Str(
        load_default=None,
        validate=validate.Length(max=50)
    )


class CategoryUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=100))
    icon = fields.Str(validate=validate.Length(max=50))
