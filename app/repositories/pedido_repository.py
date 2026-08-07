from app.models.pedido import Pedido
from app.repositories.usuario_repository import UsuarioRepository
from app.models.status import Status
from datetime import datetime, time
from sqlalchemy import func, cast, Time
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
    def chase_by_id_user(pedido_id, usuario_id):
        return Pedido.query.filter(Pedido.id == pedido_id, Pedido.usuario_id == usuario_id)

    @staticmethod
    def show_by_usuario(
        usuario_id, pedido_id=None, unidade_id=None, status=None, canal_pedido=None, 
        entrega=None, data_inicio=None, data_fim=None, valor_min=None, valor_max=None,
        ordenar="pedidoId_desc", page=1, limit=20
    ):
        query = Pedido.query.filter(Pedido.usuario_id == usuario_id)
        if pedido_id is not None:
            query = query.filter(Pedido.id == pedido_id)
        if unidade_id is not None:
            query = query.filter(Pedido.unidade_id == unidade_id)
        if status is not None:
            query = query.filter(Pedido.status == status)
        if canal_pedido is not None:
            query = query.filter(Pedido.local_pedido == canal_pedido)
        if entrega is not None:
            query = query.filter(Pedido.entrega == entrega)
        if data_inicio is not None:
            query = query.filter(Pedido.data_pedido >= data_inicio)
        if data_fim is not None:
            query = query.filter(Pedido.data_pedido <= data_fim)
        if valor_min is not None:
            query = query.filter(Pedido.total >= valor_min)
        if valor_max is not None:
            query = query.filter(Pedido.total <= valor_max)
        ordenacoes = {
            "pedidoId_desc":Pedido.id.desc(),
            "pedidoId_asc":Pedido.id.asc(),
            "data_desc":Pedido.data_pedido.desc(),
            "data_asc":Pedido.data_pedido.asc(),
            "valor_desc":Pedido.total.desc(),
            "valor_asc":Pedido.total.asc(),
        }
        query = query.order_by(ordenacoes[ordenar])
        return query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )

    @staticmethod
    def show_today_all(
        unidade_id, 
        usuario_id=None, 
        pedido_id=None, 
        status=None, 
        canal_pedido=None, 
        entrega=None, 
        hora_inicio=None, 
        hora_fim=None, 
        valor_min=None, 
        valor_max=None, 
        ordenar="pedidoId_desc", 
        page=1, 
        limit=20
        ):
        inicio = datetime.combine(datetime.today(), time.min)
        fim = datetime.combine(datetime.today(), time.max)
        query = Pedido.query.filter(
                Pedido.data_pedido.between(inicio, fim),
                Pedido.unidade_id == unidade_id
            )
        if usuario_id is not None:
            query = query.filter(Pedido.usuario_id == usuario_id)
        if pedido_id is not None:
            query = query.filter(Pedido.id == pedido_id)
        if status is not None:
            query = query.filter(Pedido.status == status)
        if canal_pedido is not None:
            query = query.filter(Pedido.local_pedido == canal_pedido)
        if entrega is not None:
            query = query.filter(Pedido.entrega == entrega)
        if hora_inicio is not None:
            query = query.filter(cast(Pedido.data_pedido, Time) >= hora_inicio)
        if hora_fim is not None:
            query = query.filter(cast(Pedido.data_pedido, Time) <= hora_fim)
        if valor_min is not None:
            query = query.filter(Pedido.total >= valor_min)
        if valor_max is not None:
            query = query.filter(Pedido.total <= valor_max)
        ordenacoes = {
            "pedidoId_desc": Pedido.id.desc(),
            "pedidoId_asc": Pedido.id.asc(),
            "valor_desc": Pedido.total.desc(),
            "valor_asc": Pedido.total.asc()
        }
        query = query.order_by(ordenacoes[ordenar])
        return query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )

    
    @staticmethod
    def show_today(
        unidade_id, status,usuario_id=None, hora_inicio=None, hora_fim=None,
        entrega=None, canal_pedido=None, valor_min=None, valor_max=None,
        ordenar = "pedidoId_desc", page = 1, limit = 20):
        inicio = datetime.combine(datetime.today(), time.min)
        fim = datetime.combine(datetime.today(), time.max)
        query = Pedido.query.filter(
                Pedido.data_pedido.between(inicio, fim),
                Pedido.unidade_id == unidade_id,
                Pedido.status.notin_([Status.FINALIZADO, Status.CANCELADO])
            )
        if usuario_id is not None:
            query = query.filter(Pedido.usuario_id == usuario_id)
        if hora_inicio is not None:
            query = query.filter(cast(Pedido.data_pedido, Time) >= hora_inicio)
        if hora_fim is not None:
            query = query.filter(cast(Pedido.data_pedido, Time) <= hora_fim)
        if entrega is not None:
            query = query.filter(Pedido.entrega == entrega)
        if canal_pedido is not None:
            query = query.filter(Pedido.local_pedido == canal_pedido)
        if valor_min is not None:
            query = query.filter(Pedido.total >= valor_min)
        if valor_max is not None:
            query = query.filter(Pedido.total <= valor_max)
        ordenacoes = {
            "pedidoId_desc": Pedido.id.desc(),
            "pedidoId_asc": Pedido.id.asc(),
            "valor_desc": Pedido.total.desc(),
            "valor_desc": Pedido.total.asc()
        }
        query = query.order_by(ordenacoes[ordenar])
        return query.paginate (
            page=page,
            per_page=limit,
            error_out=False
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