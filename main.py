from os import path
from pandas import read_excel
from xml_file import NF
from string import punctuation
    
if not path.exists('rootdir.txt'):
    rootdir = input('Informe o caminho: \n')
    with open('rootdir.txt', 'w') as f:
        f.write(rootdir)

with open('rootdir.txt', 'r') as file:
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
         
def calculo(cests, alis, ncms, name_prods, v_produtos, v_ipis):
    
    v_impoto = 0
    for cest, ali, ncm, name_prod, v_produto, v_ipi in zip(cests, alis, ncms, name_prods, v_produtos, v_ipis):
        if comparation_ncm(ncm, cest):
            base_de_calculo = (float(v_produto) + float(v_ipi))
            v_impoto += base_de_calculo * ((17.00- float(ali))/100)
            
    return v_impoto

if __name__ == '__main__':
    cests = NF(root).cest()
    alis = NF(root).ali_icms()
    ncms = NF(root).ncm()
    name_prods = NF(root).name_prod()
    v_ipis = NF(root).v_ipi()
    v_produtos = NF(root).v_prod()

    resultado = round(calculo(cests, alis, ncms, name_prods, v_produtos, v_ipis),2)
    print(resultado)