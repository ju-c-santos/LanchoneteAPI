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
    def update_cargo(funcionario_id:int, newcargo:str):
        funcionario = Funcionario.query.get(funcionario_id)
        if funcionario is None:
            raise ValueError("Funcinario inexistente")
        funcionario.cargo = newcargo
        db.session.commit()
        return funcionario 

    @staticmethod
    def updade_unidade(funcionario_id: int, unidade_id:int):
        funcionario = Funcionario.query.get(funcionario_id)
        if funcionario is None:
            raise ValueError("Funcinario inexistente")
        funcionario.unidade_id = unidade_id
        db.session.commit()
        return funcionario
        
    #excluir
    @staticmethod
    def delete(funcionario_id: int):
        funcionario = db.session.get(Funcionario, funcionario_id)
        if funcionario is None:
            return False
        db.session.delete(funcionario)
        db.session.commit()
        return True
    

