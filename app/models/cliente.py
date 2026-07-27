from app.database import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)

    usuarios_id = db.Column (
        db.Integer, 
        db.ForeignKey("usuarios.id", ondelete='CASCADE'),
        nullable=False
    )

    usuarios = db.relationship(
        "Usuario", 
        back_populates="cliente",
        uselist=False
    )