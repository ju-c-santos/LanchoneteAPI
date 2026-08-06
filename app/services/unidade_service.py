from app.models.unidade import Unidade
from app.repositories.unidade_repository import UnidadeRepository
from app.util.api_error import ApiError

class ServiceUnidade:
    @staticmethod
    def createUnidade(dados):
        unidade = Unidade(
            endereco = dados['endereco'],
            bairro = dados['bairro'],
            cep = dados['cep'],
            cidade = dados['cidade'],
            estado = dados['estado']
        )
        return UnidadeRepository.save(unidade)

    @staticmethod
    def alterar_atividade(unidade_id, bvalue):
        unidade = UnidadeRepository.chase_by_id(unidade_id)
        if unidade is None:
            raise ApiError(
                error="UNIDADE_NAO_ENCONTRADA",
                message="A unidade informada não foi encontrada.",
                status_code=404,
                details=[{
                    "field":"unidadeId",
                    "issue":f"A unidade com Id {unidade_id} não existe."
                }]
            )
        nova_atualizacao = UnidadeRepository.update_is_active(unidade.id, bvalue)
        return nova_atualizacao

    @staticmethod
    def deletar_unidade(unidade_id):
        unidade = UnidadeRepository.chase_by_id(unidade_id)
        if unidade is None:
            raise ApiError(
                error="UNIDADE_NAO_ENCONTRADA",
                message="A unidade informada não foi encontrada.",
                status_code=404,
                details=[{
                    "field":"unidadeId",
                    "issue":f"A unidade com Id {unidade_id} não existe."
                }]
            )
        return UnidadeRepository.delete(unidade.id)