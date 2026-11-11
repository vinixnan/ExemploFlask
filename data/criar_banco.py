from core.banco import BancoSQLite
from core.definitions import ARQUIVO_BANCO


def criar_tabelas():
    banco = BancoSQLite()
    conexao = banco.conexao
    try:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                nusp INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                curso TEXT NOT NULL,
                ano_ingresso INTEGER NOT NULL
            )
        """)
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS disciplinas (
                codigo_disciplina TEXT PRIMARY KEY,
                nome_disciplina TEXT NOT NULL
            )
        """)
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS matriculas (
                id_matricula INTEGER PRIMARY KEY,
                nusp INTEGER NOT NULL,
                codigo_disciplina TEXT NOT NULL,
                periodo TEXT NOT NULL,
                nota REAL NOT NULL,
                frequencia REAL NOT NULL,
                FOREIGN KEY (nusp) REFERENCES alunos(nusp),
                FOREIGN KEY (codigo_disciplina) REFERENCES disciplinas(codigo_disciplina)
            )
        """)
        conexao.commit()
    finally:
        banco.fechar()
    print(f"Tabelas criadas em: {ARQUIVO_BANCO}")


if __name__ == "__main__":
    criar_tabelas()
