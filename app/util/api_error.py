from datetime import datetime, timezone
from uuid import uuid4
from flask import jsonify, request, g

class ApiError(Exception):
    def __init__(
            self, 
            error: str,
            message: str,
            status_code: int,
            details: list | None = None
    ):
        super().__init__(message)
        self.error = error
        self.message = message
        self.status_code = status_code
        self.details = details or []

def resposta_erro(
        error: str,
        message: str,
        status_code: int,
        details: list | None = None
):
    request_id = getattr(
        g,
        "request_id",
        str(uuid4())
    )
    resposta = {
        "error": error,
        "message": message,
        "details": details or [],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "path": request.path,
        "requestId": request_id
    }
    return jsonify(resposta), status_code