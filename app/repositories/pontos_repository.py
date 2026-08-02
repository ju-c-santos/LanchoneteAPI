from app.database import db
from app.models.pontos import Pontos

class PontosRepository:
    @staticmethod
    def save(pontos: Pontos):
        db.session.add(pontos)
        db.session.commit()
        return pontos

    @staticmethod
    def chase_by_id(usuario_id:int):
        return Pontos.query.filter_by(usuario_id = usuario_id).first()

    @staticmethod
    def update():
        db.session.commit()