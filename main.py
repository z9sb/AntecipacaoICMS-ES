from os import path
from pandas import read_excel
from xml_file import NF
from string import punctuation
import cProfile

if not path.exists('rootdir.txt'):
    rootdir = input('Informe o caminho: \n')
    with open('rootdir.txt', 'w') as f:
        f.write(rootdir)

with open('rootdir.txt') as file:
    root = file.readline()
    
def cst_file():
    cest_extraction = read_excel('codigos.xlsx')['CEST']
    cest_comp = ([str(i).translate(str.maketrans
                            ('','', punctuation
                                )) for i in cest_extraction])
    return cest_comp

def ncm_file():
    ncm_extra = read_excel('codigos.xlsx')['NCM/SH']
    ncm_comp = ([int(str(i).translate(str.maketrans
                            ('','', punctuation
                                ))) for i in ncm_extra if str(i) != 'nan'])
    return ncm_comp

def comparation_ncm(ncm, cest):
    return [ncm for i in ncm_file() if int(i) == int(
            ncm[:len(str(i))])] and cest in cst_file()
         
def calculo(cests, alis, ncms, name_prods, v_produtos, v_ipis, v_fretes):
    
    v_impoto = 0
    for cest, ali, ncm, name_prod, v_produto, v_ipi, v_frete in zip(cests, alis, ncms, name_prods, v_produtos, v_ipis, v_fretes):
        if comparation_ncm(ncm, cest):
            base_de_calculo_ipi = (float(v_produto) + float(v_ipi) + float(v_frete)) * 0.17
            base_desconto_icms = float(v_produto) * (float(ali)/100)
            v_impoto += base_de_calculo_ipi - base_desconto_icms
            
    return v_impoto

if __name__ == '__main__':
    cests = NF(root).cest()
    alis = NF(root).ali_icms()
    ncms = NF(root).ncm()
    name_prods = NF(root).name_prod()
    v_ipis = NF(root).v_ipi()
    v_produtos = NF(root).v_prod()
    v_fretes = NF(root).v_frete()

    resultado = round(calculo(cests, alis, ncms, name_prods, v_produtos, v_ipis, v_fretes),2)
    print(resultado)