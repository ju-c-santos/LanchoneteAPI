from app.models.funcionario import Funcionario
from app.database import db

class FuncionarioRepository:
    #salvando 
    @staticmethod
    def save(funcionario: Funcionario):
        db.session.add(funcionario)
        db.session.commit()
        return funcionario
    
    #buscando
    @staticmethod
    def chase_by_id(funcionario_id: int):
        return Funcionario.query.get(funcionario_id)
    
    #mostrando
    @staticmethod
    def show():
        return Funcionario.query.all()
    
    #atualizar
    @staticmethod
    def update():
        db.session.commit()

    #excluir
    @staticmethod
    def delete(funcionario_id: int):
        funcionario = db.session.get(Funcionario, funcionario_id)
        if funcionario is None:
            return False
        db.session.delete(funcionario)
        db.session.commit()
        return True
    

