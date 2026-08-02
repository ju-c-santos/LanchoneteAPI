from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.services.usuario_service import AuthServiceUsuario
from app.util.decorator_perfil import perfil_required

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
        
        