from app.models.pedido import Pedido
from app.models.status import Status
from app.models.metodo_pagamento import MetodoPagamento
from app.models.item_pedido import ItemPedido
from app.repositories.pedido_repository import PedidoRepository
from app.repositories.estoque_repository import EstoqueRepository
from datetime import datetime

class PedidoService:

    @staticmethod
    def criar_pedido(id, dados):
        if dados['observacao'] is None:
            dados['observacao'] = 'None'

        pedido = Pedido(
            usuario_id = id,
            unidade_id = dados['unidade_id'],
            observacao = dados['observacao'],
            data_pedido = datetime.now(),
            metodo_pagamento = MetodoPagamento[dados['metodo_pagamento']]
        )

        total = 0
        
        for item in dados['itempedido']:
            try:
                produto = EstoqueRepository.chase_by_id(item['produto_id'])
            except ValueError:
                return "Erro: Produto inexistente"
            if produto.is_active == False:
                raise ValueError('Erro: Produto indisponível') 
            
            valor_un = float(produto.preco)
            quantidade = int(item['quantidade'])
            subtotal = valor_un * quantidade

            total += subtotal

            novo_item = ItemPedido(
                estoque_id = produto.id,
                quantidade = item['quantidade'],
                preco = produto.preco,
                subtotal = subtotal
            )
            pedido.itempedido.append(novo_item)
        pedido.total = total
        return PedidoRepository.save(pedido)

