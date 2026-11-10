"""Ponto de entrada da API REST. Executar com `python main.py`."""
from flask import Flask
from banco import CAMINHO_BANCO, fechar_conexao
from rotas import api


def criar_app():
    app = Flask(__name__)
    app.config["BANCO"] = CAMINHO_BANCO
    app.teardown_appcontext(fechar_conexao)
    app.register_blueprint(api)
    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)  # servidor de DESENVOLVIMENTO
