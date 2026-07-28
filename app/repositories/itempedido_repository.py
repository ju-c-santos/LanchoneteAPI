from app.database import db
from app.models.item_pedido import ItemPedido

class ItemPedidoRepository:

    @staticmethod
    def save(item: ItemPedido):
        db.session.add(item)
        db.session.commit()
        return item

    @staticmethod
    def chase_by_id(itempedido_id: int):
        return ItemPedido.query.get(itempedido_id)

    @staticmethod
    def chase_in_estoque(estoque_id:int):
        return ItemPedido.query.filter_by(estoque_id=estoque_id).first()

    @staticmethod
    def show():
        return ItemPedido.query.all()

    @staticmethod
    def show_by_pedido(id_pedido: int):
        return ItemPedido.query.filter_by(id_pedido=id_pedido).all()

    @staticmethod
    def update_quantity(itempedido_id:int, qtd):
        item = ItemPedido.query.get(itempedido_id)
        item.quantidade = qtd
        db.session.commit()
        return "Quantidade atualizada com sucesso!"

    @staticmethod
    def update_price(itempedido_id:int, preco):
        item = ItemPedido.query.get(itempedido_id)
        item.preco = preco
        db.session.commit()
        return "Preço alterado com sucesso!"
    
    @staticmethod
    def delete(itempedido_id:int):
        item = db.session.get(ItemPedido, itempedido_id)
        if item is None:
            return False
        db.session.delete(item)
        db.session.commit()
        return True

    
