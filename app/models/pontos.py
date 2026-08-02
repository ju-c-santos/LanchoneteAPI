from app.database import db

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

    pontos = db.Column(db.Integer, nullable=False)

    usuarios = db.relationship(
        "Usuario",
        back_populates="pontos"
    )