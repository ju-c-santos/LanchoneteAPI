from app.database import db
from app.models.perfil import Perfil
from app.models.funcionario import Funcionario

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(120), nullable = False)
    cpf = db.Column(db.String(11), unique = True)
    email = db.Column(db.String(150), unique = True)
    telefone = db.Column(db.String(15), nullable = False)
    cep = db.Column(db.String(10))
    senha_hash = db.Column(db.String(225))
    perfil = db.Column(db.Enum(Perfil), nullable=False, default=Perfil.CLIENTE)

    funcionarios = db.relationship(
        "Funcionario", 
        back_populates = "usuarios",
        uselist = False
    )
