from flask import Blueprint, request, jsonify
from app.services.funcionario_service import RegisterServiceFuncionario

funcionario_bp = Blueprint('funcionarios', __name__)

@funcionario_bp.route('/register/funcionarios', methods=['POST'])
def reigster_funcionario():
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