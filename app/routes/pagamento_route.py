from flask import Blueprint, request,jsonify
from app.services.pagamento_service import PagamentoService
from app.util.decorator_perfil import perfil_required
from flask_jwt_extended import get_jwt_identity

pagamento_bp = Blueprint("pagamento", __name__)

@pagamento_bp.route("/login/pedidos/<int:id_pedido>", methods=['POST'])
@perfil_required('CLIENTE')
def pagamento(id_pedido):
    try:
        dados = request.get_json()
        pagamento = PagamentoService.mock_pagamento(id_pedido, dados)
        return jsonify ({
            "pedido": id_pedido,
            "aprovado": pagamento.aprovado,
            "codigo": pagamento.codigo
        }), 201
        
    except ValueError as erro:
        return jsonify({"erro":str(erro)}), 400
    except Exception as e:
        return jsonify({"erro":str(e)}), 500
