from app.database import db
from app.models.consentimento import Consentimento


class ConsentimentoRepository:

    @staticmethod
    def chase_by_usuario_fidelidade(
        usuario_id,
        finalidade
    ):
        return Consentimento.query.filter_by(
            usuario_id=usuario_id,
            finalidade=finalidade
        ).first()

    @staticmethod
    def save(consentimento):
        db.session.add(consentimento)
        db.session.commit()

        return consentimento