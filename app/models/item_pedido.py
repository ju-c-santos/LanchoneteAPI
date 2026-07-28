from app.database import db

class ItemPedido(db.Model):
    __tablename__ = "itempedido"

    id = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(
        db.Integer, 
        db.ForeignKey("pedido.id", ondelete='CASCADE'),
        nullable= False
    )
    estoque_id = db.Column(
        db.Integer,
        db.ForeignKey("estoque.id", ondelete='CASCADE'),
        nullable=False
    )
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    pedido = db.relationship(
        "Pedido",
        back_populates="itempedido",
    )

    estoque = db.relationship(
        "Estoque",
        back_populates="itempedido"
    )
