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

    #alterar a disponibilidade do produto em determinada unidade
    @staticmethod
    def update_activity(estoque_id: int, bolvalue):
        item = Estoque.query.get(estoque_id)
        item.is_active = bolvalue
        db.session.commit()
        return item

    @staticmethod
    def update_quantity(estoque_id:int, qtd):
    #serão informados o id do item em estoque e a quantidade a ser RETIRADA    
        item = Estoque.query.get(estoque_id)
        item.quantidade -= qtd
        if item.quantidade < 0:
            item.is_active = False
        db.session.commit()
        return True

    @staticmethod
    def delete(estoque_id:int):
        estoque = db.session.get(Estoque, estoque_id)
        if estoque is None:
            return False
        db.session.delete(estoque)
        db.session.commit()
        return True