from app.models.estoque import Estoque
from app.database import db

class EstoqueRepository:
    @staticmethod
    def save(estoque: Estoque):
        db.session.add(estoque)
        db.session.commit()
        return estoque

    @staticmethod
    def chase_by_id(estoque_id: int):
        return Estoque.query.get(estoque_id)

    @staticmethod
    def show():
        return Estoque.query.all()

    @staticmethod
    def show_by_category(categoria:str):
        return Estoque.query.filter_by(categoria=categoria).all()

    @staticmethod
    def show_by_unidade(unidade: int):
        return Estoque.query.filter_by(unidade)

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(estoque_id:int):
        estoque = db.session.get(Estoque, estoque_id)
        if estoque is None:
            return False
        db.session.delete(estoque)
        db.session.commit()
        return True