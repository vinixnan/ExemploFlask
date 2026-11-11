from flask import Flask

from core.banco import BancoSQLite
from core.definitions import DEBUG
from rotas import api


def criar_app():
    app = Flask(__name__)
    app.register_blueprint(api)

    @app.teardown_appcontext
    def fechar_banco(erro=None):
        BancoSQLite().fechar()

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=DEBUG, threaded=True, use_reloader=False)
