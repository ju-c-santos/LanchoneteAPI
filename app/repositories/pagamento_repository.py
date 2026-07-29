from app.database import db
from app.models.pagamento import Pagamento

class PagamentoRepository:

    @staticmethod
    def save(pagamento:Pagamento):
        db.session.add(pagamento)
        db.session.commit()
        return pagamento