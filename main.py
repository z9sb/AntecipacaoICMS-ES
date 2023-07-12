from os import path
from xml_file import NF
from funcoes import calculo
from pathlib import Path

if not path.exists('rootdir.txt'):
    rootdir = input('Informe o caminho: \n')
    with open('rootdir.txt', 'w') as f:
        f.write(rootdir)

with open('rootdir.txt') as file:
    root = Path(file.readline())
 
if __name__ == '__main__':
    xml = NF(root)
    cests = xml.cest()
    alis = xml.ali_icms()
    ncms = xml.ncm()
    name_prods = xml.name_prod()
    v_ipis = xml.v_ipi()
    v_produtos = xml.v_prod()
    v_fretes = xml.v_frete()
    v_descs = xml.v_desc()
    v_outros = xml.v_outros()
    
    resultado = round(calculo(
        cests, alis, ncms, name_prods, v_produtos, v_ipis, v_fretes, v_descs, v_outros
        ),2)
    print(resultado)