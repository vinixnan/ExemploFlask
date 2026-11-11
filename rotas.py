import sqlite3

from flask import Blueprint, request, url_for

from core.banco import BancoSQLite
from model.dao import AlunoDAO, DisciplinaDAO, MatriculaDAO
from model.modelos import Aluno

api = Blueprint("api", __name__)


def _validar_aluno(dados, nusp_url=None):
    if not isinstance(dados, dict):
        return None, "Corpo deve ser um objeto JSON"
    campos = ("nome", "email", "curso", "ano_ingresso")
    if any(c not in dados for c in campos):
        return None, "Faltam nome, email, curso ou ano_ingresso"
    if nusp_url is None:
        if type(dados.get("nusp")) is not int or dados["nusp"] <= 0:
            return None, "nusp deve ser inteiro positivo"
        nusp = dados["nusp"]
    else:
        if "nusp" in dados and dados["nusp"] != nusp_url:
            return None, "nusp no JSON difere da URL"
        nusp = nusp_url
    if any(
        not isinstance(dados[c], str) or not dados[c].strip()
        for c in ("nome", "email", "curso")
    ):
        return None, "nome, email e curso devem ser textos não vazios"
    if type(dados["ano_ingresso"]) is not int:
        return None, "ano_ingresso deve ser inteiro"
    return (
        Aluno(
            nusp, dados["nome"], dados["email"], dados["curso"], dados["ano_ingresso"]
        ),
        None,
    )


@api.get("/")
def inicio():
    return {
        "mensagem": "API da universidade",
        "recursos": ["/alunos", "/disciplinas", "/matriculas"],
    }


@api.get("/alunos")
def listar_alunos():
    dao = AlunoDAO()
    curso = request.args.get("curso")
    return [aluno.to_dict() for aluno in dao.listar(curso)]


@api.get("/alunos/<int:nusp>")
def buscar_aluno(nusp):
    aluno = AlunoDAO().buscar(nusp)
    if aluno is None:
        return {"erro": "Aluno não encontrado"}, 404
    return aluno.to_dict(), 200


@api.post("/alunos")
def criar_aluno():
    aluno, erro = _validar_aluno(request.get_json(silent=True))
    if erro:
        return {"erro": erro}, 400
    try:
        AlunoDAO().inserir(aluno)
    except sqlite3.IntegrityError:
        BancoSQLite().conexao.rollback()
        return {"erro": "NUSP já cadastrado"}, 409
    return (
        aluno.to_dict(),
        201,
        {"Location": url_for("api.buscar_aluno", nusp=aluno.nusp)},
    )


@api.put("/alunos/<int:nusp>")
def atualizar_aluno(nusp):
    aluno, erro = _validar_aluno(request.get_json(silent=True), nusp_url=nusp)
    if erro:
        return {"erro": erro}, 400
    if AlunoDAO().atualizar(aluno) == 0:
        return {"erro": "Aluno não encontrado"}, 404
    return aluno.to_dict(), 200


@api.delete("/alunos/<int:nusp>")
def excluir_aluno(nusp):
    try:
        removidos = AlunoDAO().excluir(nusp)
    except sqlite3.IntegrityError:
        BancoSQLite().conexao.rollback()
        return {"erro": "Aluno possui matrículas vinculadas"}, 409
    if removidos == 0:
        return {"erro": "Aluno não encontrado"}, 404
    return "", 204


@api.get("/disciplinas")
def listar_disciplinas():
    return [d.to_dict() for d in DisciplinaDAO().listar()]


@api.get("/matriculas")
def listar_matriculas():
    return [m.to_dict() for m in MatriculaDAO().listar()]


@api.get("/matriculas/<int:id_matricula>")
def buscar_matricula(id_matricula):
    m = MatriculaDAO().buscar(id_matricula)
    if m is None:
        return {"erro": "Matrícula não encontrada"}, 404
    return m.to_dict(), 200
