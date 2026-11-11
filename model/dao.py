from core.banco import BancoSQLite
from model.modelos import Aluno, Disciplina, Matricula


class AlunoDAO:
    def __init__(self):
        self.banco = BancoSQLite()

    @property
    def conexao(self):
        return self.banco.conexao

    @staticmethod
    def _da_linha(linha):
        return Aluno(
            linha["nusp"],
            linha["nome"],
            linha["email"],
            linha["curso"],
            linha["ano_ingresso"],
        )

    def listar(self, curso=None):
        if curso:
            sql = "SELECT * FROM alunos WHERE curso = ? ORDER BY nome"
            linhas = self.conexao.execute(sql, (curso,)).fetchall()
        else:
            linhas = self.conexao.execute(
                "SELECT * FROM alunos ORDER BY nusp"
            ).fetchall()
        return [self._da_linha(linha) for linha in linhas]

    def buscar(self, nusp):
        linha = self.conexao.execute(
            "SELECT * FROM alunos WHERE nusp = ?", (nusp,)
        ).fetchone()
        return None if linha is None else self._da_linha(linha)

    def inserir(self, aluno):
        sql = """INSERT INTO alunos (nusp, nome, email, curso, ano_ingresso)
                 VALUES (?, ?, ?, ?, ?)"""
        self.conexao.execute(
            sql, (aluno.nusp, aluno.nome, aluno.email, aluno.curso, aluno.ano_ingresso)
        )
        self.conexao.commit()

    def atualizar(self, aluno):
        sql = """UPDATE alunos SET nome = ?, email = ?, curso = ?, ano_ingresso = ?
                 WHERE nusp = ?"""
        cursor = self.conexao.execute(
            sql, (aluno.nome, aluno.email, aluno.curso, aluno.ano_ingresso, aluno.nusp)
        )
        self.conexao.commit()
        return cursor.rowcount

    def excluir(self, nusp):
        cursor = self.conexao.execute("DELETE FROM alunos WHERE nusp = ?", (nusp,))
        self.conexao.commit()
        return cursor.rowcount


class DisciplinaDAO:
    def __init__(self):
        self.banco = BancoSQLite()

    @property
    def conexao(self):
        return self.banco.conexao

    @staticmethod
    def _da_linha(linha):
        return Disciplina(linha["codigo_disciplina"], linha["nome_disciplina"])

    def listar(self):
        linhas = self.conexao.execute(
            "SELECT * FROM disciplinas ORDER BY codigo_disciplina"
        ).fetchall()
        return [self._da_linha(linha) for linha in linhas]

    def buscar(self, codigo):
        linha = self.conexao.execute(
            "SELECT * FROM disciplinas WHERE codigo_disciplina = ?", (codigo,)
        ).fetchone()
        return None if linha is None else self._da_linha(linha)

    def inserir(self, disciplina):
        self.conexao.execute(
            "INSERT INTO disciplinas (codigo_disciplina, nome_disciplina) VALUES (?, ?)",
            (disciplina.codigo, disciplina.nome),
        )
        self.conexao.commit()

    def atualizar(self, disciplina):
        cursor = self.conexao.execute(
            "UPDATE disciplinas SET nome_disciplina = ? WHERE codigo_disciplina = ?",
            (disciplina.nome, disciplina.codigo),
        )
        self.conexao.commit()
        return cursor.rowcount

    def excluir(self, codigo):
        cursor = self.conexao.execute(
            "DELETE FROM disciplinas WHERE codigo_disciplina = ?", (codigo,)
        )
        self.conexao.commit()
        return cursor.rowcount


class MatriculaDAO:
    def __init__(self):
        self.banco = BancoSQLite()

    @property
    def conexao(self):
        return self.banco.conexao

    def _da_linha(self, linha):
        aluno = AlunoDAO().buscar(linha["nusp"])
        disciplina = DisciplinaDAO().buscar(linha["codigo_disciplina"])
        return Matricula(
            linha["id_matricula"],
            aluno,
            disciplina,
            linha["periodo"],
            linha["nota"],
            linha["frequencia"],
        )

    def listar(self):
        linhas = self.conexao.execute(
            "SELECT * FROM matriculas ORDER BY id_matricula"
        ).fetchall()
        return [self._da_linha(linha) for linha in linhas]

    def buscar(self, id_matricula):
        linha = self.conexao.execute(
            "SELECT * FROM matriculas WHERE id_matricula = ?", (id_matricula,)
        ).fetchone()
        return None if linha is None else self._da_linha(linha)

    def inserir(self, matricula):
        sql = """INSERT INTO matriculas
                 (id_matricula, nusp, codigo_disciplina, periodo, nota, frequencia)
                 VALUES (?, ?, ?, ?, ?, ?)"""
        self.conexao.execute(
            sql,
            (
                matricula.id_matricula,
                matricula.aluno.nusp,
                matricula.disciplina.codigo,
                matricula.periodo,
                matricula.nota,
                matricula.frequencia,
            ),
        )
        self.conexao.commit()

    def atualizar(self, matricula):
        sql = """UPDATE matriculas SET periodo = ?, nota = ?, frequencia = ?
                 WHERE id_matricula = ?"""
        cursor = self.conexao.execute(
            sql,
            (
                matricula.periodo,
                matricula.nota,
                matricula.frequencia,
                matricula.id_matricula,
            ),
        )
        self.conexao.commit()
        return cursor.rowcount

    def excluir(self, id_matricula):
        cursor = self.conexao.execute(
            "DELETE FROM matriculas WHERE id_matricula = ?", (id_matricula,)
        )
        self.conexao.commit()
        return cursor.rowcount
