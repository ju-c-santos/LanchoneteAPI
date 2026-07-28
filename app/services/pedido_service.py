from app.models.pedido import Pedido
from app.models.status import Status
from app.models.item_pedido import ItemPedido
from app.repositories.pedido_repository import PedidoRepository
from app.repositories.itempedido_repository import ItemPedidoRepository
from app.repositories.estoque_repository import EstoqueRepository
from datetime import datetime

class PedidoService:

    @staticmethod
    def criar_pedido(id, dados):
        data = datetime.now()
        data_agora = data.strftime("%d/%m/%Y %H:%M:%S")

        if dados['observacao'] is None:
            dados['observacao'] = 'None'

        pedido = Pedido(
            usuario_id = id,
            unidade_id = dados['unidade_id'],
            status = Pedido.status,
            data_pedido = data_agora,
            observacao = dados['observacao']
        )

        total = 0
        
        for item in dados['itens']:
            try:
                produto = EstoqueRepository.chase_by_id(dados['produto_id'])
            except ValueError:
                return "Erro: Produto inexistente"
            if produto.is_active == False:
                raise ValueError('Erro: Produto indisponível') 
            
            valor_un = produto.preco
            subtotal = valor_un * item['quantidade']

            total += subtotal

            itempedido = ItemPedido(
                id_pedido = produto.id,
                id_estoque = dados['produto_id'],
                quantidade = dados['quantidade'],
                preco = produto.preco,
                subtotal = subtotal
            )
            pedido.itens.append(itempedido)
        pedido.total = total
        return PedidoRepository.save(pedido)

