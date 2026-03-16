from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExpenseSchema(Schema):
    description = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200)
    )
    amount = fields.Float(
        required=True,
        validate=validate.Range(min=0.01, error="Valor deve ser maior que zero.")
    )
    date = fields.Date(
        required=True,
        error_messages={"invalid": "Data inválida. Use o formato YYYY-MM-DD."}
    )
    type = fields.Str(
        required=True,
        validate=validate.OneOf(
            ['income', 'expense'],
            error="Tipo deve ser 'income' ou 'expense'."
        )
    )
    category_id = fields.Int(load_default=None)

    # Parcelamento — RF008
    payment_type = fields.Str(
        load_default='single',
        validate=validate.OneOf(
            ['single', 'installment', 'recurring'],
            error="payment_type deve ser 'single', 'installment' ou 'recurring'."
        )
    )
    total_installments = fields.Int(
        load_default=1,
        validate=validate.Range(min=1, max=360)
    )

    # Recorrência — RF010
    recurrence_type = fields.Str(
        load_default=None,
        validate=validate.OneOf(
            [None, 'weekly', 'monthly', 'yearly'],
            error="recurrence_type deve ser 'weekly', 'monthly' ou 'yearly'."
        )
    )
    recurrence_end_date = fields.Date(load_default=None)

    @validates_schema
    def validate_payment_rules(self, data, **kwargs):
        payment_type = data.get('payment_type', 'single')

        # parcelamento precisa de total_installments > 1
        if payment_type == 'installment':
            if data.get('total_installments', 1) < 2:
                raise ValidationError(
                    "total_installments deve ser pelo menos 2 para pagamentos parcelados.",
                    field_name='total_installments'
                )

        # recorrência precisa de recurrence_type
        if payment_type == 'recurring':
            if not data.get('recurrence_type'):
                raise ValidationError(
                    "recurrence_type é obrigatório para movimentações recorrentes.",
                    field_name='recurrence_type'
                )

        # recurrence_end_date só faz sentido com recorrência
        if data.get('recurrence_end_date') and payment_type != 'recurring':
            raise ValidationError(
                "recurrence_end_date só pode ser definido para movimentações recorrentes.",
                field_name='recurrence_end_date'
            )


class ExpenseUpdateSchema(Schema):
    """Schema para edição — todos os campos são opcionais."""
    description         = fields.Str(validate=validate.Length(min=1, max=200))
    amount              = fields.Float(validate=validate.Range(min=0.01))
    date                = fields.Date()
    type                = fields.Str(validate=validate.OneOf(['income', 'expense']))
    category_id         = fields.Int(load_default=None)
    recurrence_end_date = fields.Date(load_default=None)