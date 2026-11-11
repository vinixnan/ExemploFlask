import random

from faker import Faker

from core.banco import BancoSQLite
from model.dao import AlunoDAO, DisciplinaDAO, MatriculaDAO
from model.modelos import Aluno, Disciplina, Matricula

SEED = 42
N_ALUNOS = 60

CURSOS = [
    "Engenharia de Computação",
    "Engenharia Elétrica",
    "Ciência da Computação",
    "Sistemas de Informação",
    "Engenharia de Sistemas Digitais",
]

CATALOGO = [
    ("COMP101", "Programação em Python"),
    ("COMP102", "Algoritmos e Estruturas de Dados"),
    ("COMP201", "Banco de Dados"),
    ("COMP301", "Inteligência Artificial"),
    ("MAT101", "Matemática Discreta"),
    ("ENG201", "Engenharia de Software"),
]

ANOS = [2023, 2024, 2025, 2026]


def gerar_dados(n_alunos=60):
    fake = Faker("pt_BR")
    fake.seed_instance(SEED)
    rng = random.Random(SEED)

    disciplinas = [Disciplina(codigo, nome) for codigo, nome in CATALOGO]

    alunos = []
    for i in range(n_alunos):
        nusp = 95633 + i
        nome = fake.name()
        partes = nome.lower().split()
        email = f"{partes[0][0]}{partes[-1]}@usp.br"
        alunos.append(
            Aluno(
                nusp=nusp,
                nome=nome,
                email=email,
                curso=rng.choice(CURSOS),
                ano_ingresso=rng.choice(ANOS),
            )
        )

    matriculas = []
    proximo_id = 1
    for aluno in alunos:
        disciplinas_sorteadas = rng.sample(disciplinas, k=rng.randint(2, 4))
        for disciplina in disciplinas_sorteadas:
            matriculas.append(
                Matricula(
                    id_matricula=proximo_id,
                    aluno=aluno,
                    disciplina=disciplina,
                    periodo="2026-2",
                    nota=round(rng.uniform(2.0, 10.0), 1),
                    frequencia=round(rng.uniform(55.0, 100.0), 1),
                )
            )
            proximo_id += 1

    return alunos, disciplinas, matriculas


def popular_banco():
    banco = BancoSQLite()
    try:
        aluno_dao = AlunoDAO()
        disciplina_dao = DisciplinaDAO()
        matricula_dao = MatriculaDAO()

        alunos, disciplinas, matriculas = gerar_dados(N_ALUNOS)
        inseridos = {"alunos": 0, "disciplinas": 0, "matriculas": 0}

        for disciplina in disciplinas:
            if disciplina_dao.buscar(disciplina.codigo) is None:
                disciplina_dao.inserir(disciplina)
                inseridos["disciplinas"] += 1

        for aluno in alunos:
            if aluno_dao.buscar(aluno.nusp) is None:
                aluno_dao.inserir(aluno)
                inseridos["alunos"] += 1

        for matricula in matriculas:
            if matricula_dao.buscar(matricula.id_matricula) is None:
                matricula_dao.inserir(matricula)
                inseridos["matriculas"] += 1

        print("Registros adicionados:", inseridos)
        print(
            "Total no banco:",
            {
                tabela: banco.conexao.execute(
                    f"SELECT COUNT(*) FROM {tabela}"
                ).fetchone()[0]
                for tabela in ("alunos", "disciplinas", "matriculas")
            },
        )
    finally:
        banco.fechar()


if __name__ == "__main__":
    popular_banco()
