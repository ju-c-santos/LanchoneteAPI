from flask import request, jsonify
from app.services.usuario_service import AuthServiceUsuario

class AuthControllerUsuario:
    
    @staticmethod
    def login():
        dados = request.get_json()

        token = AuthServiceUsuario.login(
            dados["email"],
            dados["senha"]
        )

        return jsonify({
            "access_token": token
        })