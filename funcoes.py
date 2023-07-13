from string import punctuation
from pandas import read_excel

def aliquota(uf: str) -> float:
    #Retorna a aliquota interestadual para o estado do ES
    dicionario = {
        'AC': 12.00, 'AL': 12.00, 'AM': 12.00, 'AP': 12.00, 'BA': 12.00, 'CE': 12.00, 'DF': 12.00,
        'GO': 12.00, 'MA': 12.00, 'MT': 12.00, 'MS': 12.00, 'MG': 7.00, 'PA': 12.00, 'PB': 12.00,
        'PR': 12.00, 'PR': 7.00, 'PI': 12.00, 'RN': 12.00, 'RS': 7.00,  'RJ': 7.00, 'RO': 12.00,
        'RR': 12.00, 'SC': 7.00, 'SP': 7.00, 'SE': 12.00, 'TO': 12.00, 'IM': 4.00, 'ES': 17.00
        }
    return dicionario[uf]

#Extrai a coluna informada no arquivo codigos
def file_search_xlsx(colum):
    extraction = read_excel('codigos.xlsx')[colum]
    comparation = ([str(i).translate(str.maketrans
                            ('','', punctuation
                                )) for i in extraction if str(i) != 'nan'])
    return comparation

#Compara o NCM e CEST informados, com o que estão no arquivo
def comparation_ncm(ncm, cest):
    
    return [ncm for i in file_search_xlsx('NCM/SH') if int(i) == int(
            ncm[:len(str(i))])] and cest in file_search_xlsx('CEST')
    
#Calcula o valor do imposto e o retorna
def calculo_antecipação_icms(
    cests, alis, ncms, name_prods, v_produtos, v_ipis, v_fretes, v_descs, v_outros
    ):
    
    v_impoto = 0
    for cest, ali, ncm, name_prod, v_produto, v_ipi, v_frete, v_desc, v_outro in zip(
        cests, alis, ncms, name_prods, v_produtos, v_ipis, v_fretes, v_descs, v_outros):
        
        if comparation_ncm(ncm, cest):
            base_de_calculo_ipi = (
                float(v_produto) + float(v_ipi) + float(v_frete) + float(v_outro) - float(v_desc)
                ) * 0.17
            base_desconto_icms = (
                float(v_produto) - float(v_desc)) * (float(ali)/100)
            v_impoto += base_de_calculo_ipi - base_desconto_icms
            
    return v_impoto

