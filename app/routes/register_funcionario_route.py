from flask import Blueprint, request, jsonify
from app.services.funcionario_service import RegisterServiceFuncionario
from app.util.decorator_perfil import perfil_required
from flask_jwt_extended import get_jwt_identity

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


@funcionario_bp.patch('/admin/funcionarios/cargo/<int:funcionario_id>')
@perfil_required("ADMINISTRADOR")
def alterar_cargo(funcionario_id):
    try:
        usuario_id = get_jwt_identity()
        dados = request.get_json()
        funcionario = RegisterServiceFuncionario.alterar_cargo(funcionario_id, usuario_id, dados)
        return jsonify({
            "usuario_id": funcionario.usuario_id,
            "cargo": funcionario.cargo
        }), 200
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500


@funcionario_bp.patch('/admin/funcionarios/unidade/<int:funcionario_id>')
@perfil_required("ADMINISTRADOR")
def alterar_unidade(funcionario_id):
    try:
        dados = request.get_json()
        funcionario = RegisterServiceFuncionario.alterar_unidade(funcionario_id, dados)
        return jsonify({
            "usuario_id": funcionario.usuario_id,
            "unidade_id": funcionario.unidade_id
        }), 200
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500