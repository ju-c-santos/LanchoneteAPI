from app.models.perfil import Perfil
from app.models.funcionario import Funcionario
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.funcionario_repository import FuncionarioRepository

class RegisterServiceAdm:
    @staticmethod
    def admRegister(dados):
        cargo = dados['cargo'].upper()
        usuario = UsuarioRepository.chase_by_id(dados['id'])
        if usuario is None:
            raise ValueError("Usuario não encontrado")
        if cargo not in ["ADMINISTRADOR", "GERENCIA", "GESTAO"]:
            raise ValueError("Rota errada")
        
        try:
            usuario.perfil = Perfil[cargo]
        except KeyError:
            raise ValueError("Cargo inválido.")

        funcionario = Funcionario(
            usuario_id = dados['id'],
            unidade_id = dados['unidade'],
            cargo = cargo
        )
        return FuncionarioRepository.save(funcionario)
        