from app.database import db
from app.models.metodo_pagamento import MetodoPagamento
from app.models.status import Status

class Pagamento(db.Model):
    __tablename__= 'pagamento'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey('pedido.id', ondelete='CASCADE'),
        nullable=False
    )
    metodo = db.Column(db.Enum(MetodoPagamento), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    aprovado = db.Column(db.Boolean, default=False, nullable=False)
    codigo = db.Column(db.String(50), nullable=False)

    pedido = db.relationship(
        "Pedido",
        back_populates='pagamento'
    )

