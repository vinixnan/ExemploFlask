import sqlite3
from pathlib import Path
from threading import Lock, local

from core.definitions import ARQUIVO_BANCO


class ConexaoLocal(local):
    def __init__(self):
        self.conexao = None


class BancoSQLite:
    _instancias = {}
    _trava = Lock()

    def __new__(cls, arquivo=ARQUIVO_BANCO):
        caminho = Path(arquivo).resolve()

        # Evita que duas threads criem a mesma instância simultaneamente.
        with cls._trava:
            if caminho not in cls._instancias:
                banco = super().__new__(cls)
                banco.arquivo = caminho
                banco._local = ConexaoLocal()
                cls._instancias[caminho] = banco
            return cls._instancias[caminho]

    @property
    def conexao(self):
        if self._local.conexao is None:
            self._local.conexao = sqlite3.connect(self.arquivo, timeout=30)
            self._local.conexao.row_factory = sqlite3.Row
            self._local.conexao.execute("PRAGMA foreign_keys = ON")
        return self._local.conexao

    def fechar(self):
        if self._local.conexao is not None:
            self._local.conexao.close()
            self._local.conexao = None
