from app.database import db
from datetime import datetime

class HistoricoPreco(db.Model):
    __tablename__ = 'historico_preco'
    id = db.Column(db.Integer, primary_key = True)
    produto_id = db.Column(
        db.Integer,
        db.ForeignKey('produtos.id', ondelete = 'CASCADE'),
        nullable = False
    )
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id', ondelete = 'CASCADE'),
        nullable = False
    )
    preco_anterior = db.Column(db.Numeric(10,2), nullable = False)
    preco_novo = db.Column(db.Numeric(10,2), nullable=False)
    data_alteracao = db.Column(db.DateTime, default=datetime.now, nullable=False)

    produtos = db.relationship(
        "Produto",
        back_populates="historico_preco"
    )

    usuarios = db.relationship(
        "Usuario",
        back_populates="historico_preco"
    )