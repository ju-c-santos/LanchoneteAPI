from app.database import db
from app.models.unidade import Unidade  

class UnidadeRepository:
    #salvar
    @staticmethod
    def save(unidade:Unidade):
        db.session.add(unidade)
        db.session.commit()
        return unidade

    #buscando
    @staticmethod
    def chase_by_id(unidade_id: int):
        return Unidade.query.get(unidade_id)

    @staticmethod
    def chase_by_name(name:str):
        return Unidade.query.filter_by(name).first()

    #mostrar
    @staticmethod
    def show():
        return Unidade.query.all()

    #atualizar
    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def update_is_active(unidade_id, bolv):
        unidade = Unidade.query.get(unidade_id)
        unidade.is_active = bolv
        db.session.commit()
        return unidade

    #excluir
    @staticmethod
    def delete(unidade_id:int):
        unidade = db.session.get(Unidade, unidade_id)
        if unidade is None:
            return False
        db.session.delete(unidade)
        db.session.commit()
        return True