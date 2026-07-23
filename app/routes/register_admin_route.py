from flask import Blueprint, request, jsonify
from app.services.funcionario_service import RegisterServiceFuncionario
from flask_jwt_extended import jwt_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/register/funcionarios/admin', methods=['POST'])
@jwt_required("ADMINISTRADOR")
def reigster_admin():
    try:
        dados = request.get_json()
        funcionario = RegisterServiceFuncionario.fucionarioRegister(dados)
        return jsonify({
            "id": funcionario.id,
            "usuario_id": funcionario.usuario_id,
            "unidade_id": funcionario.unidade_id,
            "cargo": funcionario.cargo
         }), 201
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500