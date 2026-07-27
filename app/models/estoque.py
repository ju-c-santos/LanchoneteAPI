from app.database import db

class Estoque(db.Model):
    __tablename__="estoque"

    id = db.Column(db.Integer, primary_key=True) 
    id_produto = db.Column(
        db.Integer,
        db.ForeignKey("produtos.id", ondelete='CASCADE'),
        nullable = False 
    )
    id_unidade = db.Column(
        db.Integer,
        db.ForeignKey("unidade.id", ondelete='CASCADE'),
        nullable=False
    )
    categoria = db.Column(db.String(150), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)

    produtos = db.relationship(
        "Produto",
        back_populates="estoque"
    )

    unidade = db.relationship(
        "Unidade",
        back_populates="estoque",
        uselist=False
    )

