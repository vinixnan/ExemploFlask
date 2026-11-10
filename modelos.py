"""Objetos do domínio reaproveitados da aula de OO e DAO."""
from abc import ABC, abstractmethod


class Pessoa(ABC):
    def __init__(self, nusp: int, nome: str, email: str):
        self._nusp = nusp
        self.nome = nome
        self.email = email

    @property
    def nusp(self) -> int:
        return self._nusp

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError


class Aluno(Pessoa):
    def __init__(self, nusp: int, nome: str, email: str, curso: str, ano_ingresso: int):
        super().__init__(nusp, nome, email)
        self.curso = curso
        self._ano_ingresso = ano_ingresso

    @property
    def ano_ingresso(self) -> int:
        return self._ano_ingresso

    def to_dict(self) -> dict:
        return {
            "nusp": self.nusp,
            "nome": self.nome,
            "email": self.email,
            "curso": self.curso,
            "ano_ingresso": self.ano_ingresso,
        }


class Disciplina:
    def __init__(self, codigo: str, nome: str):
        self._codigo = codigo
        self.nome = nome

    @property
    def codigo(self) -> str:
        return self._codigo

    def to_dict(self) -> dict:
        return {"codigo_disciplina": self.codigo, "nome_disciplina": self.nome}


class Matricula:
    def __init__(self, id_matricula: int, aluno: Aluno, disciplina: Disciplina,
                 periodo: str, nota: float, frequencia: float):
        self._id_matricula = id_matricula
        self.aluno = aluno
        self.disciplina = disciplina
        self.periodo = periodo
        self.nota = nota
        self.frequencia = frequencia

    @property
    def id_matricula(self) -> int:
        return self._id_matricula

    @property
    def aprovado(self) -> bool:
        return self.nota >= 5.0 and self.frequencia >= 70.0

    def to_dict(self) -> dict:
        return {
            "id_matricula": self.id_matricula,
            "nusp": self.aluno.nusp,
            "codigo_disciplina": self.disciplina.codigo,
            "periodo": self.periodo,
            "nota": self.nota,
            "frequencia": self.frequencia,
            "aprovado": self.aprovado,
        }
