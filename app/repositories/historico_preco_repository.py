from app.database import db
from app.models.historico_preco import HistoricoPreco


class HistoricoPrecoRepository:

    @staticmethod
    def save(registro):
        db.session.add(registro)
        return registro

    #listar alterações de preco do dia
    @staticmethod
    def listar_recentes():
        return(HistoricoPreco.query.order_by(HistoricoPreco.data_alteracao.desc()).all())