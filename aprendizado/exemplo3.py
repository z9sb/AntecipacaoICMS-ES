from typing import  NamedTuple, Dict

class Pessoa(NamedTuple):
    nome: str
    sobrenome: str
    telefone: Dict[str,str]
    ddd: int

