"""Execute UMA VEZ (ou novamente, sem duplicar os dados de exemplo)."""
from banco import CAMINHO_BANCO, abrir_arquivo


def criar_tabelas():
    conexao = abrir_arquivo()
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
        conexao.execute("""
            INSERT OR IGNORE INTO alunos (nusp,nome,email,curso,ano_ingresso)
            VALUES (95633,'Ana Souza','ana@usp.br','Engenharia de Computação',2026)
        """)
        conexao.execute("""
            INSERT OR IGNORE INTO disciplinas (codigo_disciplina,nome_disciplina)
            VALUES ('COMP301','Inteligência Artificial')
        """)
        conexao.execute("""
            INSERT OR IGNORE INTO matriculas
              (id_matricula,nusp,codigo_disciplina,periodo,nota,frequencia)
            VALUES (1,95633,'COMP301','2026-2',8.0,90.0)
        """)
        conexao.commit()
    finally:
        conexao.close()
    print(f"Banco preparado: {CAMINHO_BANCO}")


if __name__ == "__main__":
    criar_tabelas()
