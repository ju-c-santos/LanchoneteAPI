import os

from flask import (
    Blueprint,
    send_from_directory
)


docs_bp = Blueprint("docs", __name__)


BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

DOCS_DIR = os.path.join(BASE_DIR,"docs")

@docs_bp.get("/docs/")
def swagger():
    return send_from_directory(
        DOCS_DIR,
        "index.html"
    )

@docs_bp.get("/docs/openapi.yaml")
def openapi():
    return send_from_directory(
        DOCS_DIR,
        "openapi.yaml"
    )