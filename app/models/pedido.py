from app.database import db
from app.models.status import Status
from app.models.local_pedido import LocalPedido

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
    data_pedido = db.Column(db.DateTime, nullable=False)
    observacao = db.Column(db.Text)
    total = db.Column(db.Numeric(10,2), nullable=False)
    volume = db.Column(db.Integer, nullable=False)
    entrega = db.Column(db.Boolean, nullable=False, default=False)
    local_pedido = db.Column(db.Enum(LocalPedido), nullable=False, default=LocalPedido.BALCAO)
    usar_pontos = db.Column(db.Boolean, nullable=False, default=False)
    desconto = db.Column(db.Numeric(10,2))
    
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

    pagamento = db.relationship(
        "Pagamento",
        back_populates='pedido'
    )

    pontos = db.relationship(
        "Pontos",
        back_populates="pedido",
        cascade = "all, delete-orphan",
        passive_deletes= True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "unidade_id": self.unidade_id,
            "status": self.status.value,
            "total": self.total,
            "observacao": self.observacao,
            "local_pedido": self.local_pedido.value,
            "data_pedido": self.data_pedido.isoformat(),
            "entrega": self.entrega,
            "usar_pontos": self.usar_pontos,
            "itempedido": [item.to_dict() for item in self.itempedido]
        }