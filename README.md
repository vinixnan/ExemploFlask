# Universidade: Flask + DAO + SQLite

Exemplo didático que continua o notebook **OO_SQLite_Exemplo_Atualizado(1).ipynb**. Objetos e tabelas seguem o domínio Aluno–Disciplina–Matricula, e o DAO continua usando SQL explícito com `sqlite3`, sem ORM.

## Arquivos

- `modelos.py`: classes Pessoa, Aluno, Disciplina e Matricula.
- `banco.py`: conexão SQLite, `row_factory`, chaves estrangeiras e ciclo de vida por requisição.
- `dao.py`: AlunoDAO, DisciplinaDAO e MatriculaDAO com `?` e `commit()`.
- `criar_banco.py`: DDL das três tabelas + três registros de demonstração.
- `rotas.py`: métodos HTTP, JSON, status, validação e DAOs; Blueprint.
- `main.py`: criação e execução da aplicação Flask.
- `requirements.txt`: Flask apenas (sqlite3 já vem no Python).
- `COMANDOS_HTTPie.md`: roteiro do cliente de terminal.

## Como executar

Na pasta do projeto:

**Windows PowerShell**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python criar_banco.py
python main.py
```

**Linux/macOS**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python criar_banco.py
python main.py
```

A API roda em `http://127.0.0.1:5000/`. Use outro terminal para executar HTTPie. O banco gerado é `universidade.db` **dentro desta pasta**. Não copie o banco do notebook para cá sem desejar migrar os dados.

## Endpoints do exemplo

| Método | Caminho | Resultado |
| --- | --- | --- |
| GET | `/` | apresentação da API |
| GET | `/alunos` | lista de alunos, filtro opcional `?curso=` |
| GET | `/alunos/<nusp>` | aluno (ou 404) |
| POST | `/alunos` | cadastro (201 / 400 / 409) |
| PUT | `/alunos/<nusp>` | substituição completa (200 / 400 / 404) |
| DELETE | `/alunos/<nusp>` | exclusão (204 / 404 / 409) |
| GET | `/disciplinas` | disciplinas |
| GET | `/matriculas` | matrículas (inclui `aprovado`, calculado) |
| GET | `/matriculas/<id>` | matrícula |

Para `POST`, envie `nusp` (inteiro), `nome`, `email`, `curso` (strings) e `ano_ingresso` (inteiro). Para `PUT`, envie os quatro campos descritivos completos; o NUSP vem da URL.

## Conexão: cuidado didático

No notebook, `BancoSQLite` era um **Singleton** para uma execução sequencial. Na API, conexões SQLite são **por contexto de requisição** (`flask.g`) e são fechadas no fim desse contexto (`teardown_appcontext`). A lógica SQL dos DAOs permanece, mas seus construtores agora recebem uma conexão (`AlunoDAO(conexao)`). Isso evita reutilizar a mesma conexão em threads diferentes.

## Escopo

Não há SQLAlchemy, Flask-SQLAlchemy, Flask-Admin, autenticação, migrações ou servidor de produção. O foco é conectar as camadas **HTTP → rota → DAO → SQL → SQLite**. O servidor com `debug=True` é exclusivo para desenvolvimento local.
