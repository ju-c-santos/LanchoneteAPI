from app.database import db
from app.models.pagamento import Pagamento

class PagamentoRepository:

    @staticmethod
    def save(pagamento:Pagamento):
        db.session.add(pagamento)
        db.session.commit()
        return pagamento

    @staticmethod
    def chase_by_pedido(pedido_id:int):
        return Pagamento.query.filter_by(pedido_id = pedido_id). first()