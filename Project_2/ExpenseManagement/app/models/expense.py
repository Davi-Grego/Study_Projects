from app.extensions import db
from datetime import datetime, timezone


class Expense(db.Model):
    __tablename__ = "expenses"

    id          = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)           # RF007
    amount      = db.Column(db.Float, nullable=False)
    date        = db.Column(db.Date, nullable=False)                   # RF006 — data definida pelo usuário
    type        = db.Column(db.String(10), nullable=False)             # RF003 — 'income' | 'expense'
    created_at  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Categoria — RF005
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)

    # Usuário — RN001
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Parcelamento — RF008 / RF009
    # payment_type: 'single' | 'installment' | 'recurring'
    payment_type        = db.Column(db.String(20), nullable=False, default='single')
    installment_number  = db.Column(db.Integer, default=1)   # parcela atual (ex: 2)
    total_installments  = db.Column(db.Integer, default=1)   # total de parcelas (ex: 12)

    # Recorrência — RF010
    # recurrence: 'none' | 'monthly' | 'weekly' | 'yearly'
    is_recurring        = db.Column(db.Boolean, default=False)
    recurrence_type     = db.Column(db.String(20), nullable=True)      # 'monthly' | 'weekly' | 'yearly'
    recurrence_end_date = db.Column(db.Date, nullable=True)            # None = indeterminado
    transaction_nature = db.Column(db.String(10), nullable=False, default='variable')
    status = db.Column(db.String(20), nullable=False, default='paid', server_default='paid')
    
    # Agrupa parcelas e recorrências pelo ID da primeira entrada
    parent_id   = db.Column(db.Integer, db.ForeignKey("expenses.id"), nullable=True)
    children    = db.relationship("Expense", backref=db.backref("parent", remote_side=[id]), lazy=True)

    def __repr__(self):
        return f"<Expense {self.description} - {self.amount} ({self.type})>"

    def to_dict(self):
        return {
            'id':                  self.id,
            'description':         self.description,
            'amount':              self.amount,
            'date':                self.date.isoformat(),
            'type':                self.type,
            'payment_type':        self.payment_type,
            'installment_number':  self.installment_number,
            'total_installments':  self.total_installments,
            'is_recurring':        self.is_recurring,
            'recurrence_type':     self.recurrence_type,
            'recurrence_end_date': self.recurrence_end_date.isoformat() if self.recurrence_end_date else None,
            'transaction_nature':  self.transaction_nature,
            'category_id':         self.category_id,
            'status':              self.status,
            'user_id':             self.user_id,
            'parent_id':           self.parent_id,
            'created_at':          self.created_at.isoformat(),
        }