from datetime import datetime
from app.database import db
from sqlalchemy import func
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
    def listar_promocao_filtrada(
        promocao_id=None,
        nome_promocao=None,
        produto_id=None,
        tipo_promocao=None,
        data_inicio=None,
        data_fim=None,
        valor_min=None,
        valor_max=None,
        ativa=None,
        ordenacao="promocaoId_desc",
        page=1,
        limit=20
    ):
        query = Promocao.query
        if promocao_id is not None:
            query = query.filter(Promocao.id == promocao_id)
        if nome_promocao is not None:
            query = query.filter(Promocao.nome.ilike(f"%{nome_promocao}%"))
        if produto_id is not None:
            query = query.filter(Promocao.produto_id == produto_id)
        if tipo_promocao is not None:
            query = query.filter(Promocao.tipo_desconto == tipo_promocao)
        if data_inicio is not None:
            query = query.filter(Promocao.data_fim >= data_inicio)
        if data_fim is not None:
            query = query.filter(Promocao.data_inicio <= data_fim)
        if valor_min is not None:
            query = query.filter(Promocao.valor_desconto >= valor_min)
        if valor_max is not None:
            query = query.filter(Promocao.valor_desconto <= valor_max)
        if ativa is not None:
            query = query.filter(Promocao.ativa.is_(ativa))
        ordenacoes = {
            "promocaoId_asc": Promocao.id.asc(),
            "promocaoId_desc": Promocao.id.desc(),
            "nomePromo_asc": func.lower(Promocao.nome).asc(),
            "nomePromo_desc": func.lower(Promocao.nome).desc(),
            "dataPromo_asc": Promocao.data_inicio.asc(),
            "dataPromo_desc": Promocao.data_inicio.desc()
        }
        query = query.order_by(ordenacoes[ordenacao], Promocao.id.desc())
        return query.paginate(
            page=page,
            per_page=limit,
            error_out=False
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