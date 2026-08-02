from app.database import db
from app.models.perfil import Perfil

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
        uselist = False,
        cascade = "all, delete-orphan",
        passive_deletes = True
    )

    cliente = db.relationship(
        "Cliente",
        back_populates="usuarios",
        uselist=False,
        cascade = "all, delete-orphan",
        passive_deletes = True
    )

    pedido = db.relationship(
        "Pedido",
        back_populates="usuarios",
        cascade = "all, delete-orphan",
        passive_deletes= True
    )

    pontos = db.relationship(
        "Pontos",
        back_populates="usuario",
        cascade = "all, delete-orphan",
        passive_deletes = True
    )