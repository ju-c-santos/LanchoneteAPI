from flask import jsonify

def resposta_sucesso(data=None, message="Operação realizada com sucesso!",
        status_code=200, meta=None,
):
    resposta = {
        "message":message,
        "data":data
    }
    if meta is not None:
        resposta['meta'] = meta
    return jsonify(resposta, status_code)