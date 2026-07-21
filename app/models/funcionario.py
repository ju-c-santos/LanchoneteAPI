from app.database import db

class Funcionario(db.Model):
    __tablename__ = 'funcionarios'

    id = db.Column(db.Integer, primary_key= True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable = False,
        unique = True
    )

    unidade_id = db.Column(
        db.Integer, 
        db.ForeignKey("unidade.id"),
        nullable = False
    )

    cargo = db.Column(db.String(30), nullable=False)


    usuarios = db.relationship("Usuario", back_populates = "funcionarios")
    unidade = db.relationship("Unidade", back_populates = "funcionarios")

