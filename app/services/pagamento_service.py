from app.models.pagamento import Pagamento
from app.repositories.pagamento_repository import PagamentoRepository
from app.repositories.pedido_repository import PedidoRepository
from app.models.metodo_pagamento import MetodoPagamento
from app.models.status import Status
from app.util.api_error import ApiError
import random 
import uuid

class PagamentoService:

    @staticmethod
    def mock_pagamento(id_pedido, id_usuario, dados):
        pedido = PedidoRepository.chase_by_id(id_pedido)
        if pedido.usuario_id != id_usuario:
            raise ApiError(
                error="USUARIO_INVALIDO",
                message="O usuário logado não pode completar esta ação.",
                status_code=403,
                details=[{
                    "field":"usuarioId",
                    "issue":"Apenas o usuário que realizou o pedido pode completar o pagamento do mesmo."
                }]
            )
        if pedido is None:
            raise ApiError(
                error="PEDIDO_NAO_ENCONTRADO",
                message="O pedido informado não foi encontrado.",
                status_code=404,
                details=[{
                    "field":"pedidoId",
                    "issue":f"O pedido {id_pedido} não foi encontrado."
                }]
            )

        metodo = MetodoPagamento(dados["metodo"])
        #validando pedido
        if metodo == MetodoPagamento.PIX:
            aprovado = True
        elif metodo == MetodoPagamento.DINHEIRO:
            aprovado = True
        else:
            aprovado = random.choice([True, False])

        if aprovado:
            pedido.status = Status.AGUARDANDO_CONFIRMACAO
        else:
            pedido.status = Status.PAGAMENTO_RECUSADO

        pagamento = Pagamento(
            pedido_id = pedido.id,
            metodo = metodo,
            valor = pedido.total,
            aprovado = aprovado,
            codigo = str(uuid.uuid4())[:10] #gera um código único para o pagamento
        )
        PedidoRepository.update()
        return PagamentoRepository.save(pagamento)
         
        
