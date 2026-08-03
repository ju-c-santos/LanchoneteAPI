from app.database import db
from datetime import datetime

class Pontos(db.Model):
    __tablename__ = 'pontos'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete='CASCADE'),
        nullable = False
    )
    pedido_id = db.Column(
        db.Integer,
        db.ForeignKey("pedido.id", ondelete='CASCADE'),
        nullable = False
    )
    tipo = db.Column(db.String(20), nullable=False) #pontos recebidos
    quantidade = db.Column(db.Integer, nullable=False) #pontos utilizados
    data_movimentacao = db.Column(db.DateTime, nullable=False, default=datetime.now)


    usuarios = db.relationship(
        "Usuario",
        back_populates="pontos"
    )
    
    pedido = db.relationship(
        "Pedido",
        back_populates="pontos"
    )