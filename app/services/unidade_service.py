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