from app.database import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    telefone = db.Column(db.String(20))

    usuario_id = db.Column (
        db.Integer, 
        db.ForeignKey("usuario.id")
    )

    usuario = db.relationship("Usuario")