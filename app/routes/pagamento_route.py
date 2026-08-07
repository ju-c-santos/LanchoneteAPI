from flask import Blueprint, request,jsonify
from app.services.pagamento_service import PagamentoService
from app.models.metodo_pagamento import MetodoPagamento
from app.util.api_error import ApiError
from app.util.decorator_perfil import perfil_required
from flask_jwt_extended import get_jwt_identity
from app.util.api_response import resposta_sucesso

pagamento_bp = Blueprint("pagamento", __name__)

@pagamento_bp.route("/login/pedidos/<int:id_pedido>", methods=['POST'])
@perfil_required("CLIENTE")
def pagamento(id_pedido):
    id_usuario = int(get_jwt_identity())
    dados = request.get_json()
    metodo = dados['metodo'].strip().upper()
    if metodo not in MetodoPagamento:
        raise ApiError(
            error="METODO_INVALIDO",
            message="O método de pagamento inserido é inválido.",
            status_code=422,
            details=[{
                "field":"metodo",
                "issue": f"Métodos de pagamento aceitos:" + ",".join(MetodoPagamento[MetodoPagamento])
            }]
        ) 
    pagamento = PagamentoService.mock_pagamento(id_pedido, id_usuario, dados)
    return resposta_sucesso(
        message="Item do pedido foi alterado com sucesso!",
        status_code=201,
        data={
            "usuarioId": id_usuario,
            "pedidoId": id_pedido,
            "metodoPagamento": pagamento.metodo.value,
            "aprovado": pagamento.aprovado,
            "codigo": pagamento.codigo,
        }
    )
 
