# dados = [
#     {
#         'nome': 'Edu',
#         'sobrenome': 'Mendes',
#         'telefone': {'residencial':'111-111','movel':'0000000'},
#         'ddd': 19,
#     },
#     {
#       'nome': 'Fausto',
#         'sobrenome': 'mago',
#         'telefone': {'residencial':'222-222','movel':'1111111'},
#         'ddd': 51,  
#     }
# ]


# from collections import namedtuple

# pessoa = namedtuple('pessoa','nome sobrenome telefone ddd')

# dados = [
#     pessoa('Edu','Mendes',{'residencial':'111-111', 'movel':'0000000'}, 11),
#     pessoa('Fausto','mago',{'residencial':'222-222', 'movel':'111111'}, 51)
# ]
# a = dados[0]
# print(a.nome)