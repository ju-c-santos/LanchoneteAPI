from flask import Blueprint, request, jsonify
from app.services.usuario_service import AuthServiceUsuario

usuario_bp = Blueprint('usuarios', __name__)

@usuario_bp.route('/register', methods=['POST'])
def reister_user():
    try:
        dados = request.get_json()
        usuario = AuthServiceUsuario.userRegister(dados)

        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
        }), 201
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500