from app.models.unidade import Unidade
from app.repositories.unidade_repository import UnidadeRepository

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
            raise ValueError("Unidade inexistente")
        nova_atualizacao = UnidadeRepository.update_is_active(unidade.id, bvalue)
        return nova_atualizacao

    @staticmethod
    def deletar_unidade(unidade_id):
        unidade = UnidadeRepository.chase_by_id(unidade_id)
        if unidade is None:
            raise ValueError("Unidade inválida")
        return UnidadeRepository.delete(unidade.id)