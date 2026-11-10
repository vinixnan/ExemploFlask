# Testes HTTPie (cliente separado do projeto)

Em outro terminal, com `python main.py` executando:

```bash
python -m pip install httpie
http GET http://127.0.0.1:5000/
http GET http://127.0.0.1:5000/alunos
http GET http://127.0.0.1:5000/alunos/95633
http GET 'http://127.0.0.1:5000/alunos?curso=Engenharia%20de%20Computa%C3%A7%C3%A3o'
http POST http://127.0.0.1:5000/alunos nusp:=95634 nome=Bruno email=bruno@usp.br curso=Computacao ano_ingresso:=2026
http PUT http://127.0.0.1:5000/alunos/95634 nome='Bruno Silva' email=bruno@usp.br curso=Computacao ano_ingresso:=2026
http DELETE http://127.0.0.1:5000/alunos/95634
http GET http://127.0.0.1:5000/disciplinas
http GET http://127.0.0.1:5000/matriculas
```

**Importante**: cole cada comando em **uma única linha** no PowerShell ou Bash. Em HTTPie, `campo=valor` é texto JSON; `campo:=2026` envia número JSON. O cliente HTTPie **não é exigido pelo servidor** e não está no `requirements.txt`.

Tentativas úteis:

```bash
http GET http://127.0.0.1:5000/alunos/999999
http POST http://127.0.0.1:5000/alunos nusp:=95633 nome=Outra email=outra@usp.br curso=Computacao ano_ingresso:=2026
http DELETE http://127.0.0.1:5000/alunos/95633
```

Esperado: 404, 409 (NUSP duplicado) e 409 (chave estrangeira de matrícula), respectivamente.
