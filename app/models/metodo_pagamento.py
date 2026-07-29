import enum

class MetodoPagamento(enum.Enum):
    DINHEIRO = "DINHEIRO"
    DEBITO = "DEBITO"
    CREDITO= "CREDITO"
    PIX = "PIX"
    VALE = "VALE"