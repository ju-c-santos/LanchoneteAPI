from datetime import datetime

from app.database import db
from app.models.fidelidade_consentimento import FidelidadeConsentimento


class Consentimento(db.Model):
    __tablename__ = "consentimentos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "usuarios.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    finalidade = db.Column(
        db.Enum(FidelidadeConsentimento),
        nullable=False
    )

    aceito = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    versao_termo = db.Column(
        db.String(20),
        nullable=False
    )

    data_consentimento = db.Column(
        db.DateTime,
        nullable=True
    )

    data_revogacao = db.Column(
        db.DateTime,
        nullable=True
    )

    usuario = db.relationship(
        "Usuario",
        back_populates="consentimentos"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "usuario_id",
            "finalidade",
            name="uq_usuario_finalidade_consentimento"
        ),
    )

    def to_dict(self):
        return {
            "consentimentoId": self.id,
            "finalidade": self.finalidade.value,
            "aceito": self.aceito,
            "versaoTermo": self.versao_termo,
            "dataConsentimento": (
                self.data_consentimento.isoformat()
                if self.data_consentimento
                else None
            ),
            "dataRevogacao": (
                self.data_revogacao.isoformat()
                if self.data_revogacao
                else None
            )
        }