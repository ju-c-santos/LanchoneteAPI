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
        db.ForeignKey("unidades.id")
        nullable - False
    )

    cargo = db.Column(db.String(30), nullable=False)


    unidade = db.relationship("Unidade")

