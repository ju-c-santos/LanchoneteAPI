from app.models.pagamento import Pagamento
from app.repositories.pagamento_repository import PagamentoRepository
from app.repositories.pedido_repository import PedidoRepository
from app.models.metodo_pagamento import MetodoPagamento
from app.models.status import Status
import random 
import uuid

class PagamentoService:

    @staticmethod
    def mock_pagamento(id_pedido, dados):
        pedido = PedidoRepository.chase_by_id(id_pedido)

        if pedido is None:
            raise ValueError("Pedido inexistente")

        metodo = MetodoPagamento[dados["metodo"]]
        #validando pedido
        if metodo == MetodoPagamento.PIX:
            aprovado = True
        elif metodo == MetodoPagamento.DINHEIRO:
            aprovado = True
        else:
            aprovado = random.choice([True, False])

        if aprovado:
            pedido.status = Status.AGUARDANDO_CONFIRMAÇAO
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
        
