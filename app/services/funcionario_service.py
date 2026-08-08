from app.models.perfil import Perfil
from app.models.funcionario import Funcionario
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.funcionario_repository import FuncionarioRepository
from app.repositories.unidade_repository import UnidadeRepository
from app.util.api_error import ApiError

class RegisterServiceFuncionario:
    @staticmethod
    def fucionarioRegister(dados):
        cargo = dados['cargo'].upper()
        usuario = UsuarioRepository.chase_by_id(dados['id'])
        funcionario = FuncionarioRepository.chase_by_usuario(dados['id'])
        if usuario is None:
            raise ApiError(
                error="USUARIO_NAO_ENCONTRADO",
                message="O usuário informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"usuarioId",
                    "issue":f"O usuário com Id {dados["id"]} não existe."
                }]
            )
        if funcionario is not None:
            raise ApiError(
                error="FUNCIONARIO_JA_CADASTRADO",
                message="O funcionário informado já consta cadastrado.",
                status_code= 422,
                details=[{
                    "field": "usuarioId",
                    "issue": f"O usuário de Id {dados['id']} já consta cadastrado com o Id {funcionario.id}"
                }]
            )
        if cargo in ["ADMINISTRADOR", "GERENCIA"]:
            raise ApiError(
                error="ROTA_INVALIDA",
                message="Rota para cadastro inválida.",
                status_code=409,
                details=[{
                    "field":"cargo",
                    "issue":f"Cargos de administração NÃO são aceitos aqui. (ADMINISTRADOR e GERENCIA)"
                }]
            )
        try:
            usuario.perfil = Perfil[cargo]
        except KeyError:
            raise ApiError(
                error="CARGO_INVALIDO",
                message="O cargo informado é inválido.",
                status_code=422,
                details=[{
                    "field":"cargo",
                    "issue":"Valores válidos: " + ", ".join(Perfil)
                }]
            )

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
            raise ApiError(
                error="FUNCIONARIO_NAO_ENCONTRADO",
                message="O funcionário informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"funcionarioId",
                    "issue":f"O funcionário com Id {funcionario_id} não existe."
                }]
            )
        usuario = funcionario.usuario_id
        cargo = dados['novoCargo'].upper()
        if Perfil[cargo] not in Perfil:
            raise ApiError(
                error="CARGO_INVALIDO",
                message="O cargo informado é inválido.",
                status_code=422,
                details=[{
                    "field":"cargo",
                    "issue":"Valores válidos: " + ", ".join(Perfil)
                }]
            )
        FuncionarioRepository.update_cargo(funcionario_id, cargo)
        UsuarioRepository.update_perfil(usuario, Perfil[cargo])
        return funcionario


    @staticmethod
    def alterar_unidade(funcionario_id, dados):
        unidade = UnidadeRepository.chase_by_id(dados['unidadeId'])
        if unidade is None:
            raise ApiError(
                error="UNIDADE_NAO_ENCONTRADA",
                message="A unidade informada não foi encontrada.",
                status_code=404,
                details=[{
                    "field":"unidadeId",
                    "issue":f"A unidade com Id {dados['unidadeId']} não existe."
                }]
            )
        funcionario = FuncionarioRepository.updade_unidade(funcionario_id, dados['unidadeId'] )
        return funcionario

    @staticmethod
    def update_ferias(funcionario_id, bolv):
        funcionario = FuncionarioRepository.chase_by_id(funcionario_id)
        if funcionario is None:
            raise ApiError(
                error="FUNCIONARIO_NAO_ENCONTRADO",
                message="O funcionário informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"funcionarioId",
                    "issue":f"O funcionário com Id {funcionario_id} não existe."
                }]
            )
        nova_atualizacao = FuncionarioRepository.update_ferias(funcionario.id, bolv)
        return nova_atualizacao

    @staticmethod
    def deletar_funcionario(funcionario_id):
        funcionario = FuncionarioRepository.chase_by_id(funcionario_id)
        if funcionario is None:
            raise ApiError(
                error="FUNCIONARIO_NAO_ENCONTRADO",
                message="O funcionário informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"funcionarioId",
                    "issue":f"O funcionário com Id {funcionario_id} não existe."
                }]
            )
        usuario_id = funcionario.usuario_id
        UsuarioRepository.update_perfil(usuario_id, 'CLIENTE')
        return FuncionarioRepository.delete(funcionario.id)
