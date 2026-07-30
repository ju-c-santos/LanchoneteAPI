from flask import Blueprint, request, jsonify
from app.services.funcionario_service import RegisterServiceFuncionario
from app.util.decorator_perfil import perfil_required

funcionario_bp = Blueprint('funcionarios', __name__)

@funcionario_bp.route('/admin/register/funcionarios', methods=['POST'])
@perfil_required("GERENCIA", "ADMINISTRADOR")
def register_funcionario():
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