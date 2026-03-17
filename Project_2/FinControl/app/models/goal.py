from app.extensions import db
from datetime import datetime, timezone


class Goal(db.Model):
    __tablename__ = 'goals'

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(100), nullable=False)
    target_amount  = db.Column(db.Float, nullable=False)               # RF015 — meta de economia
    current_amount = db.Column(db.Float, default=0.0)                  # progresso atual
    deadline       = db.Column(db.Date, nullable=True)                 # prazo opcional da meta
    spending_limit = db.Column(db.Float, nullable=True)                # RF017 — limite de gasto para alerta
    is_active      = db.Column(db.Boolean, default=True)
    created_at     = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user_id        = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def progress_pct(self) -> float:
        """Percentual de progresso em direção à meta. RN005."""
        if self.target_amount <= 0:
            return 0.0
        return round((self.current_amount / self.target_amount) * 100, 2)

    @property
    def remaining(self) -> float:
        """Valor restante para atingir a meta."""
        return max(self.target_amount - self.current_amount, 0.0)

    def to_dict(self):
        return {
            'id':             self.id,
            'name':           self.name,
            'target_amount':  self.target_amount,
            'current_amount': self.current_amount,
            'remaining':      self.remaining,
            'progress_pct':   self.progress_pct,
            'deadline':       self.deadline.isoformat() if self.deadline else None,
            'spending_limit': self.spending_limit,
            'is_active':      self.is_active,
            'user_id':        self.user_id,
            'created_at':     self.created_at.isoformat(),
        }