from datetime import datetime

from app.models.consentimento import Consentimento
from app.models.fidelidade_consentimento import FidelidadeConsentimento
from app.repositories.consentimento_repository import (
    ConsentimentoRepository
)
from app.util.api_error import ApiError


class ConsentimentoService:

    @staticmethod
    def registrar_fidelidade(
        usuario_id,
        aceito,
        versao_termo
    ):

        if not isinstance(aceito, bool):
            raise ApiError(
                error="CONSENTIMENTO_INVALIDO",
                message="O consentimento informado é inválido.",
                status_code=422,
                details=[
                    {
                        "field": "aceito",
                        "issue": "O valor deve ser true ou false."
                    }
                ]
            )

        consentimento = (
            ConsentimentoRepository
            .buscar_por_usuario_e_finalidade(
                usuario_id,
                FidelidadeConsentimento.PROGRAMA_FIDELIDADE
            )
        )

        agora = datetime.now()

        if consentimento is None:

            consentimento = Consentimento(
                usuario_id=usuario_id,
                finalidade=(
                    FidelidadeConsentimento.PROGRAMA_FIDELIDADE
                ),
                aceito=aceito,
                versao_termo=versao_termo
            )

        consentimento.aceito = aceito
        consentimento.versao_termo = versao_termo

        if aceito:
            consentimento.data_consentimento = agora
            consentimento.data_revogacao = None

        else:
            consentimento.data_revogacao = agora

        ConsentimentoRepository.save(
            consentimento
        )

        return consentimento.to_dict()