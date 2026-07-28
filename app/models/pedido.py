from app.database import db
from app.models.status import Status
from app.models.metodo_pagamento import MetodoPagamento

class Pedido(db.Model):
    __tablename__="pedido"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete='CASCADE'),
        nullable= False
    )
    unidade_id = db.Column(
        db.Integer,
        db.ForeignKey("unidade.id", ondelete='CASCADE'),
        nullable= False
    )
    status = db.Column(db.Enum(Status), nullable=False, default=Status.AGUARDANDO_PAGAMENTO)
    data_pedido = db.Column(db.String(100), nullable=False)
    observacao = db.Column(db.Text)
    total = db.Column(db.Float, nullable=False)


    usuarios = db.relationship(
        "Usuario",
        back_populates= "pedido",
    )

    unidade = db.relationship(
        "Unidade",
        back_populates= "pedido"
    )

    itempedido = db.relationship(
        "ItemPedido",
        back_populates="pedido",
        cascade="all, delete-orphan",
        passive_deletes = True
    )