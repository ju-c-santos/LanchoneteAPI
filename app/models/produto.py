from app.database import db

class Produto(db.Model):
    __tablename__= "produtos"

    id = db.Column(db.Integer, primary_key= True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable= False) #quantidade de caracteres ilimitado 
    preco = db.Column(db.Float, nullable= False) #o preço vai ser o mesmo para todas as unidades
    categoria = db.Column (db.String(150), nullable= False)

    #pode ter mais de um produto em um mesmo estoque 
    estoque = db.relationship(
        "Estoque",
        back_populates= "produtos",
        cascade = "all, delete-orphan",
        passive_deletes = True
    )
    historico_preco = db.relationship(
            "HistoricoPreco",
            back_populates= "produtos",
            cascade = "all, delete-orphan",
            passive_deletes = True
        )