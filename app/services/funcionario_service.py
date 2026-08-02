from app.models.perfil import Perfil
from app.models.funcionario import Funcionario
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.funcionario_repository import FuncionarioRepository
from app.repositories.unidade_repository import UnidadeRepository

class RegisterServiceFuncionario:
    @staticmethod
    def fucionarioRegister(dados):
        cargo = dados['cargo'].upper()
        usuario = UsuarioRepository.chase_by_id(dados['id'])
        if usuario is None:
            raise ValueError("Usuario não encontrado")
        if cargo in ["ADMINISTRADOR", "GERENCIA"]:
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


    @staticmethod
    def alterar_cargo(funcionario_id, dados):
        funcionario = FuncionarioRepository.chase_by_id(funcionario_id)
        if funcionario is None:
            raise ValueError("Funcionário não encontrado")
        usuario = funcionario.usuario_id
        cargo = dados['novo_cargo'].upper()
        if Perfil[cargo] not in Perfil:
            raise ValueError("Cargo inexistente")
        FuncionarioRepository.update_cargo(funcionario_id, cargo)
        UsuarioRepository.update_perfil(usuario, Perfil[cargo])
        return funcionario

    @staticmethod
    def alterar_unidade(funcionario_id, dados):
        unidade = UnidadeRepository.chase_by_id(dados['unidade_id'])
        if unidade is None:
            raise ValueError("Unidade não encontrada")
        funcionario = FuncionarioRepository.updade_unidade(funcionario_id, dados['unidade_id'] )
        return funcionario
