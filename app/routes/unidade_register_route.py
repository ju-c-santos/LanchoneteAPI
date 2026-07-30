from flask import Blueprint, request, jsonify
from app.services.unidade_service import ServiceUnidade
from app.util.decorator_perfil import perfil_required

unidade_bp = Blueprint('unidade', __name__)

@unidade_bp.route('/admin/register/unidade', methods=['POST'])
@perfil_required("ADMINISTRADOR")
def unidade_register():
    try:
        dados = request.get_json()
        unidade = ServiceUnidade.createUnidade(dados)
        return jsonify({
            "id": unidade.id,
            "cep": unidade.cep,
            "cidade": unidade.cidade,
            "estado": unidade.estado
        }), 201
    
    except ValueError as erro:
        return jsonify({"erro": str(erro)}),400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500