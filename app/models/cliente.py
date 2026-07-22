from app.database import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column (
        db.Integer, 
        db.ForeignKey("usuario.id")
    )

    usuarios = db.relationship("Usuario", back_populates="cliente")