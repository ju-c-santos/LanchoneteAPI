from flask import request, jsonify
from app.services.usuario_service import AuthServiceUsuario
from app.util.api_response import resposta_sucesso

class AuthControllerUsuario:
    
    @staticmethod
    def login():
        dados = request.get_json()
        token = AuthServiceUsuario.login(
            dados["user"],
            dados["senha"]
        )
        return resposta_sucesso(
        message="Usuário logado com sucesso!",
        status_code=201,
        data={
            "AccessToken": token
        }
    )
 