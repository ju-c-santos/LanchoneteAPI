from flask import Blueprint, request, jsonify
from app.services.administrador_service import RegisterServiceAdm
from flask_jwt_extended import jwt_required
from app.util.api_response import resposta_sucesso
from app.util.api_error import ApiError

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/register', methods=['POST'])
@jwt_required("GESTAO")
def reigster_admin():
    dados = request.get_json()
    if not isinstance(dados, dict):
            raise ApiError(
                error="JSON_INVALIDO",
                message="O corpo da requisição deve ser um JSON válido.",
                status_code=400,
                details=[]
            )
    funcionario = RegisterServiceAdm.admRegister(dados)
    return resposta_sucesso(
          message="O funcionário administrativo foi cadastrado com sucesso.",
          data={
            "id": funcionario.id,
            "usuario_id": funcionario.usuario_id,
            "unidade_id": funcionario.unidade_id,
            "cargo": funcionario.cargo                
          },
          status_code=201
    )