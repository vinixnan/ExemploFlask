"""Conexão SQLite: mantém o SQL da aula; usa conexão por requisição no Flask.

No notebook anterior, BancoSQLite era um Singleton. Em um servidor Web, uma
conexão SQLite não deve ser compartilhada indiscriminadamente entre threads.
O objeto `g` guarda uma conexão POR CONTEXTO de requisição.
"""
import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parent / "universidade.db"


def abrir_arquivo(caminho=CAMINHO_BANCO):
    conexao = sqlite3.connect(caminho)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def obter_conexao():
    from flask import current_app, g
    if "conexao" not in g:
        g.conexao = abrir_arquivo(current_app.config["BANCO"])
    return g.conexao


def fechar_conexao(erro=None):
    from flask import g
    conexao = g.pop("conexao", None)
    if conexao is not None:
        conexao.close()
