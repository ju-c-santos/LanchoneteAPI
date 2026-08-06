from datetime import datetime, time
from decimal import Decimal, InvalidOperation
from app.util.api_error import ApiError

class Conversores:
    @staticmethod
    def converter_data(valor, campo, fim_do_dia=False):
        if valor is None or valor == '':
            return None
        try:
            data = datetime.strptime(valor, "%Y-%m-%d").date()
        except ValueError:
            raise ApiError(
                error="DATA_INVALIDA",
                message=f"O filtro {campo} é inválido.",
                status_code=422,
                details=[{
                    "field": campo,
                    "issue": "Utilize o formato AAAA-MM-DD."
                }]
            )
        horario = time.max if fim_do_dia else time.min
        return datetime.combine(data, horario)

    @staticmethod
    def converter_enum(valor, enum_class, campo):
        if valor is None or valor == "":
            return None
        try:
            return enum_class(valor.strip().upper())
        except (ValueError, AttributeError):
            valores_permitidos = [
                item.value
                for item in enum_class
            ]
            raise ApiError(
                error="FILTRO_INVALIDO",
                message=f"O filtro {campo} é inválido.",
                status_code=422,
                details=[{
                    "field": campo,
                    "issue": "Valoress permitidos: " + ", ".join(valores_permitidos)
                }]
            )

    @staticmethod
    def converter_id(valor, campo):
        if valor is None or valor =="":
            return None
        try:
            valor_convertido = int(valor)
        except(ValueError, TypeError):
            raise ApiError(
                error="FILTRO_INVALIDO",
                message=f"O filtro {campo} é inválido.",
                status_code=422,
                details=[{
                    "field": campo,
                    "issue":"Informe um número inteiro."
                }]
            )
        if valor_convertido <= 0:
            raise ApiError(
                error="FILTRO_INVALIDO",
                message=f"O filtro {campo} é inválido.",
                status_code=422,
                details=[{
                    "field": campo,
                    "issue":"Informe um número inteiro maior que zero."
                }]
            )
        return valor_convertido

    @staticmethod
    def converter_booleano(valor, campo):
        if valor is None:
            return None
        valor_normal = valor.strip().lower()
        if valor_normal == "true":
            return True
        elif valor_normal == "false":
            return False
        else:
            raise ApiError(
                error="FILTRO_INVALIDO",
                message=f"O filtro {campo} é inválido.",
                status_code=422,
                details=[{
                    "field": campo,
                    "issue": "Informe um valor de true ou false."
                }]
            )


    @staticmethod
    def converter_decimal(valor, campo):
            #esse método converte o valor para decimal e faz a validação já de uma vez
        if valor is None:
            return None
        try:
            valor_normalizado = str(valor).replace("," , ".")
            valor_decimal = Decimal(valor_normalizado)
        except (InvalidOperation,TypeError):
            raise ApiError (
                error="FILTRO_INVALIDO",
                message=f"O filtro {campo} é inválido.",
                status_code=422,
                details=[{
                    "field": campo,
                    "issue": "Informe um valor numérico válido."
                }]
            )
        if valor_decimal < 0: 
            raise ApiError(
                error="FILTRO_INVALIDO",
                message=f"O filtro {campo} não pode ser negativo.",
                status_code=422,
                details=[{
                    "field":campo,
                    "issue":"Informe um valor maior ou igual a zero."
                }]
            )
        return valor_decimal

    @staticmethod
    def converter_hora(valor, campo):
        if valor is None or valor == '':
            return None
        try:
            return datetime.strptime(valor, "%H:%M").time()
        except ValueError:
            raise ApiError(
                error="HORA_INVALIDA",
                message=f"O filtro {campo} é inválido.",
                status_code=422,
                details=[{
                    "field":campo,
                    "issue":"Utilize o formato HH:MM (ex: 08:30)"
                }]
            )