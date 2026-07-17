from app.database import db

class Unidade(db.Model):
    __tablename__ = 'unidade'

    id = db.Column(db.Integer, primary_key= True)
    localidade = db.Column(db.String(150), nullable = False)
    estado = db.Column(db.String(2), nullable = False)

    funcionarios = db.relationship("Funcionario", back_populates = "unidade")
    