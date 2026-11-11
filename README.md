# Universidade — Flask, DAO e SQLite

Projeto didático baseado no notebook de Python e SQLite. Utiliza `Aluno`, `Disciplina` e `Matricula`, classes DAO com SQL explícito e `BancoSQLite` Singleton, sem ORM.

## Estrutura

```text
.
├── COMANDOS_HTTPie.txt
├── core
│   ├── banco.py
│   └── definitions.py
├── criar_e_popular.sh
├── data
│   ├── criar_banco.py
│   └── popular_banco.py
├── main.py
├── model
│   ├── dao.py
│   └── modelos.py
├── README.md
├── requirements.txt
└── rotas.py
```

## Instalação

Na raiz do projeto, com Python 3.10 ou superior:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Criar e popular o banco

Execute o script que reúne as duas etapas:

```bash
bash criar_e_popular.sh
```

Ele executa a criação das tabelas e a população com dados fictícios usando Faker. A geração utiliza semente 42 e cria 60 alunos, 6 disciplinas e suas matrículas. A população pode ser executada novamente sem duplicar os registros existentes.

> Execute o comando a partir da raiz do projeto. Como `data/criar_banco.py` e `data/popular_banco.py` importam `core` e `model`, o script deve assegurar que a raiz do projeto esteja no caminho de importação do Python.

## Executar a API

```bash
python main.py
```

Por padrão, a aplicação estará disponível em `http://127.0.0.1:5000`.

As configurações `NOME_BANCO`, `ARQUIVO_BANCO` e `DEBUG` estão em `core/definitions.py`.

## Rotas

| Método | URL | Operação |
| --- | --- | --- |
| GET | `/` | Informações da API |
| GET | `/alunos` | Listar alunos (aceita `?curso=`) |
| GET | `/alunos/<nusp>` | Consultar aluno |
| POST | `/alunos` | Cadastrar aluno |
| PUT | `/alunos/<nusp>` | Atualizar aluno |
| DELETE | `/alunos/<nusp>` | Excluir aluno |
| GET | `/disciplinas` | Listar disciplinas |
| GET | `/matriculas` | Listar matrículas |
| GET | `/matriculas/<id>` | Consultar matrícula |

## Testes com HTTPie

Consulte o arquivo `COMANDOS_HTTPie.txt` para os comandos de teste. HTTPie é opcional e não faz parte das dependências do servidor.

