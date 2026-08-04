from datetime import datetime
from app.database import db
from app.models.promocao import Promocao

class PromocaoRepository:

    @staticmethod
    def save(promocao:Promocao):
        db.session.add(promocao)
        db.session.commit()
        return promocao

    @staticmethod
    def chase_by_id(promocao_id):
        return db.session.get(Promocao, promocao_id)

    @staticmethod
    def listar_ativas():
        agora = datetime.now()

        return (
            Promocao.query
            .filter(
                Promocao.ativa.is_(True),
                Promocao.data_inicio <= agora,
                Promocao.data_fim >= agora
            )
            .all()
        )

    @staticmethod
    def chase_by_produto(produto_id, unidade_id):
        agora = datetime.now()

        return (
            Promocao.query
            .filter(
                Promocao.produto_id == produto_id,
                Promocao.ativa.is_(True),
                Promocao.data_inicio <= agora,
                Promocao.data_fim >= agora,
                db.or_(
                    Promocao.unidade_id == unidade_id,
                    Promocao.unidade_id.is_(None)
                )
            )
            .order_by(Promocao.valor_desconto.desc())
            .first()
        )

    @staticmethod
    def update_activity(promocao_id, bolv):
        promo = Promocao.query.get(promocao_id)
        promo.ativa = bolv
        db.session.commit()
        return promo    

     #excluir 
    @staticmethod
    def delete(promocao_id: int):
        promo = db.session.get(Promocao, promocao_id)
        if promo is None:
            return False
        db.session.delete(promo)
        db.session.commit()
        return True