from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.services.usuario_service import AuthServiceUsuario
from app.util.decorator_perfil import perfil_required
from app.services.pontos_service import PontosService
from app.util.api_response import resposta_sucesso
from app.util.api_error import ApiError

usuario_bp = Blueprint('usuarios', __name__)

@usuario_bp.route('/usuario/register', methods=['POST'])
def register_user():
    dados = request.get_json()
    if not isinstance(dados, dict):
        raise ApiError(
            error="JSON_INVALIDO",
            message="O corpo da requisição deve ser um JSON válido.",
            status_code=400,
            details=[]
        ) 
    usuario = AuthServiceUsuario.userRegister(dados)
    return resposta_sucesso(
        message="Cadastro realizado com sucesso.",
        data={
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "telefone": usuario.telefone
        },
        status_code=200
    )

@usuario_bp.patch("/usuarios/alteracao/<int:usuario_id>")
@perfil_required("CLIENTE", "ADMINISTRADOR", "GESTAO")
def atualizar_cadastro(usuario_id):
    if usuario_id is None:
        raise ApiError(
            error="UNIDADE_NAO_ENCONTRADA",
            message="A unidade informada não foi encontrada.",
            status_code=404,
            details=[{
                "field":"usuarioId",
                "issue":f"O usuário com Id {usuario_id} não existe."
            }]
        )
    usuario_logado = int(get_jwt_identity())
    dados = request.get_json()
    if not isinstance(dados, dict):
        raise ApiError(
            error="JSON_INVALIDO",
            message="O corpo da requisição deve ser um JSON válido.",
            status_code=400,
            details=[]
        ) 
    if(usuario_logado != usuario_id):
        return ApiError(
            error="USUARIO_INVALIDO",
            message="O usuário logafo não possui permissão para atualizar o cadastro.",
            status_code=409,
            details=[{
                "field":"usuarioId",
                "issues":f"Apenas a administração ou o usuário {usuario_id} podem realizar esta ação.",
            }]
        )
    usuario = AuthServiceUsuario.atualizar(usuario_id, dados)
    return resposta_sucesso(
        message="Cadastro atualizado com sucesso.",
        data={
            "usuario_id": usuario_id,
            "email": usuario.email,
            "telefone": usuario.telefone,
            "cep": usuario.cep,
            "senha_hash": usuario.senha_hash
        },
        status_code=200
    )

@usuario_bp.patch("/admin/usuarios/ativar-cadastro/<int:usuario_id>")
@perfil_required("ADMINISTRADOR", "GESTAO")
def ativar_cadastro(usuario_id):
    if usuario_id is None:
        raise ApiError(
            error="UNIDADE_NAO_ENCONTRADA",
            message="A unidade informada não foi encontrada.",
            status_code=404,
            details=[{
                "field":"usuarioId",
                "issue":f"O usuário com Id {usuario_id} não existe."
            }]
        )
    AuthServiceUsuario.cadastro_ativo(usuario_id, True)
    return resposta_sucesso(
        message="Cadastro ativado com sucesso.",
        status_code=200
    )

@usuario_bp.patch("/admin/usuarios/desativar-cadastro/<int:usuario_id>")
@perfil_required("ADMINISTRADOR", "GESTAO")
def desativar_cadastro(usuario_id):
    if usuario_id is None:
        raise ApiError(
            error="UNIDADE_NAO_ENCONTRADA",
            message="A unidade informada não foi encontrada.",
            status_code=404,
            details=[{
                "field":"usuarioId",
                "issue":f"O usuário com Id {usuario_id} não existe."
            }]
        )
    AuthServiceUsuario.cadastro_ativo(usuario_id, False)
    return resposta_sucesso(
        message="Cadastro desativado com sucesso.",
        status_code=200
    )

@usuario_bp.get('/usuario/consulta/saldo')
@perfil_required("CLIENTE")
def pontos_disponiveis():
    usuario_logado = int(get_jwt_identity())
    if usuario_logado is None:
        raise ApiError(
            error="UNIDADE_NAO_ENCONTRADA",
            message="A unidade informada não foi encontrada.",
            status_code=404,
            details=[{
                "field":"usuarioId",
                "issue":f"O usuário com Id {usuario_logado} não existe."
            }]
        )
    registros = PontosService.consultar_saldo(usuario_logado)
    return resposta_sucesso(
        message="O saldo do usuário foi consultado com sucesso.",
        data= registros,
        status_code=200
    )

@usuario_bp.get('/<int:usuario_id>/consulta/saldo')
@perfil_required("CLIENTE", "GERENTE", "ADMINISTRADOR", "GESTAO")
def consultar_pontos(usuario_id):
    if usuario_id is None:
        raise ApiError(
            error="UNIDADE_NAO_ENCONTRADA",
            message="A unidade informada não foi encontrada.",
            status_code=404,
            details=[{
                "field":"usuarioId",
                "issue":f"O usuário com Id {usuario_id} não existe."
            }]
        )
    registros = PontosService.consultar_saldo(usuario_id)
    return resposta_sucesso(
        message="O saldo do usuário foi consultado com sucesso.",
        data= registros,
        status_code=200
    )

@usuario_bp.delete('/usuario/<int:usuario_id>/delete')
@perfil_required("ADMINISTRADOR", "CLIENTE", "GESTAO")
def delete_usuario(usuario_id):
    if usuario_id is None:
        raise ApiError(
            error="UNIDADE_NAO_ENCONTRADA",
            message="A unidade informada não foi encontrada.",
            status_code=404,
            details=[{
                "field":"usuarioId",
                "issue":f"O usuário com Id {usuario_id} não existe."
            }]
        )
    AuthServiceUsuario.delete_usuario(usuario_id)
    return resposta_sucesso(
        message="Usuario excluído com sucesso.",
        status_code=200
    )


        
        
        