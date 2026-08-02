from app.models.pedido import Pedido
from app.repositories.usuario_repository import UsuarioRepository
from app.models.status import Status
from app.database import db

class PedidoRepository:

    @staticmethod
    def save(pedido: Pedido):
        db.session.add(pedido)
        db.session.commit()
        return pedido

    @staticmethod
    def chase_by_id(pedido_id: int):
        return Pedido.query.get(pedido_id)

    @staticmethod
    def show():
        return Pedido.query.all()

    @staticmethod
    def show_by_date(data_pedido:str):
        return Pedido.query.filter_by(data_pedido=data_pedido).all()

    @staticmethod
    def show_by_metodopg(metodo_pagamento:str):
        return Pedido.query.filter_by(metodo_pagamento=metodo_pagamento).all()

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def update_status(pedido_id:int, statusnew):
        pedido = Pedido.query.get(pedido_id)
        if statusnew not in Status:
            return False
        pedido.status = statusnew
        db.session.commit()
        return True

    @staticmethod
    def delete(pedido_id:int):
        pedido = db.session.get(Pedido, pedido_id)
        if pedido is None:
            return False
        db.session.delete(pedido)
        db.session.commit()
        return True
