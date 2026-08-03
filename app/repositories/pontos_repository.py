from app.database import db
from app.models.pontos import Pontos
from app.repositories.usuario_repository import UsuarioRepository

class PontosRepository:
    @staticmethod
    def save(movimentacao: Pontos):
        db.session.add(movimentacao)
        return movimentacao

    @staticmethod
    def chase_by_usuario_id(usuario_id:int):
        return (Pontos.query
                .filter_by(usuario_id = usuario_id)
                .order_by(Pontos.data_movimentacao.desc())
                .all()
            )

    @staticmethod
    def chase_by_pedido(pedido_id:int):
        return Pontos.query.filter_by(pedido_id=pedido_id).first()

    @staticmethod
    def update():
        db.session.commit()