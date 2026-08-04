from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.services.usuario_service import AuthServiceUsuario
from app.util.decorator_perfil import perfil_required
from app.services.pontos_service import PontosService

usuario_bp = Blueprint('usuarios', __name__)

@usuario_bp.route('/usuario/register', methods=['POST'])
def register_user():
    try:
        dados = request.get_json()
        usuario = AuthServiceUsuario.userRegister(dados)

        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "telefone": usuario.telefone
        }), 201
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@usuario_bp.patch("/usuarios/alteracao/<int:usuario_id>")
@perfil_required("CLIENTE", "ADMINISTRADOR")
def atualizar_cadastro(usuario_id):
    try:
        usuario_logado = int(get_jwt_identity())
        dados = request.get_json()
        if(usuario_logado != usuario_id):
            return jsonify({"erro":"Acesso negado"}), 403
        usuario = AuthServiceUsuario.atualizar(usuario_id, dados)
        return jsonify({
            "usuario_id": usuario_id,
            "email": usuario.email,
            "telefone": usuario.telefone,
            "cep": usuario.cep,
            "senha_hash": usuario.senha_hash
        }), 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400

@usuario_bp.patch("/admin/usuarios/ativar-cadastro/<int:usuario_id>")
@perfil_required("ADMINISTRADOR")
def ativar_cadastro(usuario_id):
    try:
        AuthServiceUsuario.cadastro_ativo(usuario_id, True)
        return jsonify({
            "mensagem":"cadastro ativo"
        }), 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400 

@usuario_bp.patch("/admin/usuarios/desativar-cadastro/<int:usuario_id>")
@perfil_required("ADMINISTRADOR")
def desativar_cadastro(usuario_id):
    try:
        AuthServiceUsuario.cadastro_ativo(usuario_id, False)
        return jsonify({
            "mensagem":"cadastro ativo"
        }), 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400 

@usuario_bp.get('/usuario/consulta/saldo')
@perfil_required("CLIENTE")
def pontos_disponiveis():
    usuario_logado = int(get_jwt_identity())
    try:
        registros = PontosService.consultar_saldo(usuario_logado)
        return registros, 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400 


@usuario_bp.get('/<int:usuario_id>/consulta/saldo')
@perfil_required("CLIENTE", "GERENTE", "ADMINISTRADOR")
def consultar_pontos(usuario_id):
    try:
        registros = PontosService.consultar_saldo(usuario_id)
        return registros, 200
    except Exception as e:
        return jsonify({"erro":str(e)}), 400 


@usuario_bp.delete('/<int:usuario_id>/delete')
@perfil_required("ADMINISTRADOR", "CLIENTE")
def delete_usuario(usuario_id):
    try:
        AuthServiceUsuario.deletar(usuario_id)
        return jsonify({
            "mensagem": "Usuario excluído com sucesso."
        }), 200

    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 404

    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500   

        
        
        