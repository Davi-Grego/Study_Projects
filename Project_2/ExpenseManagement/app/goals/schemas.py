from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from datetime import date


class GoalSchema(Schema):
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100)
    )
    target_amount = fields.Float(
        required=True,
        validate=validate.Range(min=0.01, error="Meta deve ser maior que zero.")
    )
    deadline = fields.Date(load_default=None)
    spending_limit = fields.Float(
        load_default=None,
        validate=validate.Range(min=0.01, error="Limite de gasto deve ser maior que zero.")
    )

    @validates_schema
    def validate_deadline(self, data, **kwargs):
        deadline = data.get('deadline')
        if deadline and deadline < date.today():
            raise ValidationError(
                "O prazo da meta não pode ser uma data no passado.",
                field_name='deadline'
            )


class GoalUpdateSchema(Schema):
    """Todos os campos opcionais para edição parcial."""
    name           = fields.Str(validate=validate.Length(min=1, max=100))
    target_amount  = fields.Float(validate=validate.Range(min=0.01))
    current_amount = fields.Float(validate=validate.Range(min=0.0))
    deadline       = fields.Date(load_default=None)
    spending_limit = fields.Float(validate=validate.Range(min=0.01))
    is_active      = fields.Bool()