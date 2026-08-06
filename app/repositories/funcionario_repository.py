from app.models.funcionario import Funcionario
from app.util.api_error import ApiError
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

    @staticmethod
    def chase_by_usuario(usuario_id:int):
        return Funcionario.query.filter_by(usuario_id=usuario_id).first()
    
    #atualizar
    @staticmethod
    def update_cargo(funcionario_id:int, newcargo:str):
        funcionario = Funcionario.query.get(funcionario_id)
        if funcionario is None:
            raise ApiError(
                error="FUNCIONARIO_NAO_ENCONTRADO",
                message="O funcionário informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"funcionarioId",
                    "issue":f"O funcionário de Id {funcionario_id} não existe."
                }]
            )
        funcionario.cargo = newcargo
        db.session.commit()
        return funcionario 

    @staticmethod
    def updade_unidade(funcionario_id: int, unidade_id:int):
        funcionario = Funcionario.query.get(funcionario_id)
        if funcionario is None:
            raise ApiError(
                error="FUNCIONARIO_NAO_ENCONTRADO",
                message="O funcionário informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"funcionarioId",
                    "issue":f"O funcionário de Id {funcionario_id} não existe."
                }]
            )   
        funcionario.unidade_id = unidade_id
        db.session.commit()
        return funcionario

    @staticmethod  
    def update_ferias(funcionario_id, bolv):
        funcionario = Funcionario.query.get(funcionario_id)
        funcionario.ferias = bolv
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
    

