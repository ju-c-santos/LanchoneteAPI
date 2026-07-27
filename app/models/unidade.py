from app.database import db

class Unidade(db.Model):
    __tablename__ = 'unidade'

    id = db.Column(db.Integer, primary_key= True)
    endereco = db.Column(db.String(150), nullable = False)
    bairro = db.Column(db.String(150), nullable = False)
    cep = db.Column(db.String(9), nullable= False)
    cidade = db.Column(db.String(50), nullable = False)
    estado = db.Column(db.String(2), nullable = False)

    funcionarios = db.relationship(
        "Funcionario", 
        back_populates = "unidade",
        cascade = "all, delete-orphan",
        passive_deletes = True
        #relacionamento 1 - * -> uselist = True
    )
    
    estoque = db.relationship(
        "Estoque",
        back_populates="unidade",
        uselist=False,
        cascade = "all, delete-orphan",
        passive_deletes = True
    )
    
    