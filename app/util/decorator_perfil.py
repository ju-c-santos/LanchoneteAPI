from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt

def perfil_required(*perfis):
#PARA JULGAR O ACESSO DO USUARIO :)
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims["perfil"] not in perfis:
                return jsonify({
                    "erro": "Você não possui permissão"
                }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
