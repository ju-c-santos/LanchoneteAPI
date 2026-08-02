from app.models.pedido import Pedido
from app.repositories.usuario_repository import UsuarioRepository
from app.models.status import Status
from datetime import datetime, time
from sqlalchemy import func
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
    def show_by_usuario(usuario_id:int):
        return Pedido.query.filter_by(usuario_id=usuario_id).order_by(Pedido.data_pedido.desc()).all()

    @staticmethod
    def show_today_all(unidade_id):
        inicio = datetime.combine(datetime.today(), time.min)
        fim = datetime.combine(datetime.today(), time.max)
        return (
            Pedido.query.filter(
                Pedido.data_pedido.between(inicio, fim),
                Pedido.unidade_id == unidade_id
            ).all()
        )

    @staticmethod
    def show_today(unidade_id):
        inicio = datetime.combine(datetime.today(), time.min)
        fim = datetime.combine(datetime.today(), time.max)
        return (
            Pedido.query.filter(
                Pedido.data_pedido.between(inicio, fim),
                Pedido.status != Status.FINALIZADO,
                Pedido.status != Status.CANCELADO,
                Pedido.unidade_id == unidade_id
            ).all()
        )


    @staticmethod
    def total_vendido_unidade(unidade_id):
        total = (
            db.session.query(func.sum(Pedido.total)).filter(
                Pedido.unidade_id == unidade_id,
                Pedido.status == Status.FINALIZADO
            ).scalar()
        )
        return total or 0

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
