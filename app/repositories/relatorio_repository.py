from sqlalchemy import func
from app.database import db
from app.models.item_pedido import ItemPedido
from app.models.pedido import Pedido
from app.models.estoque import Estoque
from app.models.produto import Produto
from app.models.status import Status

class RelatorioRepository:
    @staticmethod
    def produto_mais_vendido_unidade(unidade_id):
         return (
            db.session.query(
                Produto.id,
                Produto.nome,
                func.sum(ItemPedido.quantidade).label("total_vendido")
            )
            .join(Estoque, Estoque.id_produto == Produto.id)
            .join(ItemPedido, ItemPedido.estoque_id == Estoque.id)
            .join(Pedido, Pedido.id == ItemPedido.id_pedido)
            .filter(
                Pedido.unidade_id == unidade_id,
                Pedido.status == Status.FINALIZADO
            )
            .group_by(Produto.id, Produto.nome)
            .order_by(func.sum(ItemPedido.quantidade).desc())
            .first()
        )