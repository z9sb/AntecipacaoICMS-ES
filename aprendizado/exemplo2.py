from collections import namedtuple

pessoa = namedtuple('pessoa','nome sobrenome telefone ddd')

dados = [
    pessoa('Edu','Mendes',{'residencial':'111-111', 'movel':'0000000'}, 11),
    pessoa('Fausto','mago',{'residencial':'222-222', 'movel':'111111'}, 51)
]
a = dados[0]
print(a.nome)